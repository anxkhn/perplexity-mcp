"""Discovery, account access, cache fallback, and search routing regression tests."""

import json
from copy import deepcopy
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from curl_cffi.requests.exceptions import RequestException

from perplexity.client import Client
from perplexity.config import ENDPOINT_AUTH_SESSION, MODEL_CONFIG, MODEL_MAPPINGS
from perplexity.models import REFRESH_SECONDS, ModelRegistry, subscription_tier


def make_client(data, tier="pro"):
    auth = {"user": {"subscription_tier": tier, "subscription_status": "trialing"}}

    def get(url, **kwargs):
        response = Mock()
        response.json.return_value = auth if url == ENDPOINT_AUTH_SESSION else data
        return response

    return SimpleNamespace(
        auth_session=auth,
        session=SimpleNamespace(
            get=Mock(side_effect=get),
            cookies=SimpleNamespace(
                get_dict=lambda: {"__Host-pplx-last-active-account": "account"}
            ),
        ),
        model_mappings=MODEL_MAPPINGS,
    )


def live_config():
    data = deepcopy(MODEL_CONFIG)
    data["models"]["gpt6_2_sol_thinking"] = {
        "label": "GPT-6.2 Sol Thinking",
        "mode": "search",
        "provider": "OPENAI",
    }
    data["models"]["old_hidden_model"] = {"label": "Old model", "mode": "search"}
    data["search_config"].insert(
        0,
        {
            "label": "GPT-6.2 Sol",
            "reasoning_model": "gpt6_2_sol_thinking",
            "subscription_tier": "pro",
        },
    )
    return data


@pytest.mark.parametrize(
    "tier, default",
    [
        ("pro", "gpt6_1_sol_thinking"),
        ("max", "gpt6_astra_thinking"),
        ("free", None),
        ("unknown", None),
    ],
)
def test_tier_aware_defaults_and_no_automatic_routing(tmp_path, tier, default):
    client = make_client(MODEL_CONFIG, tier)
    registry = ModelRegistry(client, tmp_path / "models.json")
    assert registry.default_model == default
    for mode in ("pro", "reasoning"):
        assert not {"turbo", "pplx_pro", "pplx_reasoning"} & set(
            client.model_mappings[mode].values()
        )
        assert "pplx_asi_astra" not in client.model_mappings[mode]
        assert "comet_browser_agent_sonnet" not in client.model_mappings[mode]
    if default:
        assert registry.resolve_model() == default
    else:
        with pytest.raises(ValueError, match="available search model"):
            registry.resolve_model()
    if tier == "pro":
        with pytest.raises(ValueError):
            registry.resolve_model("gpt6_astra_thinking")
        assert registry.resolve_model("claude-5.5-sonnet-thinking") == "claude55sonnetthinking"


def test_refresh_discovers_picker_models_without_changing_other_clients(tmp_path, monkeypatch):
    now = 1000000
    monkeypatch.setattr("perplexity.models.time.time", lambda: now)
    data = live_config()
    client = make_client(data)
    registry = ModelRegistry(client, tmp_path / "models.json")
    registry.refresh()
    assert registry.resolve_model() == "gpt6_2_sol_thinking"
    assert "gpt6_2_sol_thinking" not in MODEL_MAPPINGS["reasoning"]
    assert "old_hidden_model" not in registry.config["models"]
    assert registry.changes["added"] == ["gpt6_2_sol_thinking"]
    assert registry.source == "live"
    assert json.loads(registry.cache_path.read_text())["config"] == registry.config
    call = client.session.get.call_args_list[0]
    assert call.kwargs["params"] == {"version": "2.18", "source": "default"}
    assert call.kwargs["headers"]["x-pplx-account"] == "account"
    registry.refresh()
    assert client.session.get.call_count == 2
    now += REFRESH_SECONDS + 1
    registry.refresh()
    assert client.session.get.call_count == 4


def test_cache_does_not_leak_max_access_to_pro_account(tmp_path):
    path = tmp_path / "models.json"
    ModelRegistry(make_client(MODEL_CONFIG, "max"), path).refresh()
    client = make_client(MODEL_CONFIG, "pro")
    registry = ModelRegistry(client, path)
    result = registry.list_models()
    assert result["source"] == "cache"
    client.session.get.assert_not_called()
    assert result["subscription_tier"] == "pro"
    assert result["default_reasoning_model"] == "gpt6_1_sol_thinking"
    assert "gpt6_astra_thinking" not in result["available_search_models"]


def test_force_refresh_reports_removed_models(tmp_path):
    data = live_config()
    client = make_client(data)
    registry = ModelRegistry(client, tmp_path / "models.json")
    registry.refresh()
    data["search_config"] = data["search_config"][1:]
    result = registry.list_models("gpt6_2_sol_thinking", refresh=True)
    assert result["changes"]["removed"] == ["gpt6_2_sol_thinking"]
    assert result["default_reasoning_model_available"] is False
    assert registry.resolve_model() == "gpt6_1_sol_thinking"


@pytest.mark.parametrize("failure", [RequestException("offline"), ValueError("not JSON")])
def test_refresh_failure_keeps_cache_and_throttles_retries(tmp_path, monkeypatch, failure):
    now = 1000000
    monkeypatch.setattr("perplexity.models.time.time", lambda: now)
    path = tmp_path / "models.json"
    ModelRegistry(make_client(live_config()), path).refresh()
    now += REFRESH_SECONDS + 1
    client = make_client(None)
    client.session.get.side_effect = failure
    registry = ModelRegistry(client, path)
    result = registry.list_models()
    assert result["source"] == "cache"
    assert result["stale"] is True
    assert result["refresh_error"] == type(failure).__name__
    assert registry.resolve_model() == "gpt6_2_sol_thinking"
    registry.refresh()
    assert client.session.get.call_count == 1


def test_invalid_response_does_not_replace_cache(tmp_path):
    data = live_config()
    path = tmp_path / "models.json"
    registry = ModelRegistry(make_client(data), path)
    registry.refresh()
    before = path.read_text()
    data["search_config"][0]["reasoning_model"] = "missing"
    registry.refresh(force=True)
    assert registry.refresh_error == "ValueError"
    assert path.read_text() == before


def test_corrupt_cache_and_failed_fetch_use_bundled_default(tmp_path):
    path = tmp_path / "models.json"
    path.write_text("not JSON")
    registry = ModelRegistry(make_client({}), path)
    result = registry.list_models()
    assert result["source"] == "bundled"
    assert result["refresh_error"] == "ValueError"
    assert registry.resolve_model() == "gpt6_1_sol_thinking"


def test_unwritable_cache_does_not_discard_live_config(tmp_path):
    parent = tmp_path / "file"
    parent.write_text("not a directory")
    registry = ModelRegistry(make_client(live_config()), parent / "models.json")
    registry.refresh()
    assert registry.source == "live"
    assert registry.resolve_model() == "gpt6_2_sol_thinking"


def test_discovered_id_reaches_search_payload(tmp_path):
    fake = make_client(live_config())
    client = Client.__new__(Client)
    client.session = fake.session
    client.auth_session = fake.auth_session
    client.own = True
    client.copilot = float("inf")
    client.file_upload = float("inf")
    response = Mock()
    response.iter_lines.return_value = []
    client.session.post = Mock(return_value=response)
    registry = ModelRegistry(client, tmp_path / "models.json")
    registry.refresh()
    client.search("question", mode="reasoning", model=registry.resolve_model())
    payload = client.session.post.call_args.kwargs["json"]
    assert payload["params"]["model_preference"] == "gpt6_2_sol_thinking"


@pytest.mark.parametrize(
    "session, expected",
    [
        ({}, "unknown"),
        ({"user": {"subscription_tier": "monthly", "subscription_status": "active"}}, "unknown"),
        ({"user": {"subscription_tier": "max", "subscription_status": "canceled"}}, "free"),
        ({"user": {"subscription_tier": "max", "subscription_status": "active"}}, "max"),
    ],
)
def test_subscription_detection(session, expected):
    assert subscription_tier(session) == expected


def test_newest_model_selection_ignores_picker_order(tmp_path):
    data = live_config()
    data["search_config"].append(data["search_config"].pop(0))
    registry = ModelRegistry(make_client(data), tmp_path / "models.json")
    registry.refresh()
    assert registry.resolve_model() == "gpt6_2_sol_thinking"


def test_organization_policy_does_not_allow_unverified_models(tmp_path):
    data = deepcopy(MODEL_CONFIG)
    data["organization_model_policy"] = {"restricted": True}
    registry = ModelRegistry(make_client(data), tmp_path / "models.json")
    registry.refresh()
    with pytest.raises(ValueError):
        registry.resolve_model("gpt6_1_sol_thinking")


def test_unknown_session_recovers_even_with_fresh_cache(tmp_path):
    path = tmp_path / "models.json"
    ModelRegistry(make_client(MODEL_CONFIG), path).refresh()
    client = make_client(MODEL_CONFIG)
    client.auth_session = {}
    registry = ModelRegistry(client, path)
    registry.refresh()
    assert registry.tier == "pro"
    assert registry.resolve_model() == "gpt6_1_sol_thinking"


@pytest.mark.parametrize("invalid", ["bad_tier", "empty_picker", "bad_id"])
def test_invalid_picker_keeps_previous_mappings(tmp_path, invalid):
    data = deepcopy(MODEL_CONFIG)
    registry = ModelRegistry(make_client(data), tmp_path / "models.json")
    if invalid == "bad_tier":
        data["search_config"][0]["subscription_tier"] = []
    elif invalid == "bad_id":
        data["search_config"][0]["non_reasoning_model"] = []
    else:
        data["search_config"] = []
    registry.refresh()
    assert registry.refresh_error == "ValueError"
    assert registry.source == "bundled"
    assert registry.resolve_model() == "gpt6_1_sol_thinking"


def test_live_router_ids_are_not_selectable(tmp_path):
    data = deepcopy(MODEL_CONFIG)
    for model in ("turbo", "pplx_pro", "pplx_pro_upgraded", "pplx_reasoning"):
        data["models"][model] = {"label": "Automatic", "mode": "search"}
        data["search_config"].append(
            {
                "label": "Automatic",
                "non_reasoning_model": model,
                "subscription_tier": "pro",
            }
        )
    registry = ModelRegistry(make_client(data), tmp_path / "models.json")
    registry.refresh()
    for model in ("turbo", "pplx_pro", "pplx_pro_upgraded", "pplx_reasoning"):
        with pytest.raises(ValueError):
            registry.resolve_model(model)
