"""Tests for MCP environment handling."""

import json
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from perplexity.mcp import load_cookies_from_env, resolve_default_search_kwargs
from perplexity import mcp as server


def test_default_mcp_mode_resolves_to_search() -> None:
    print("console.log -> validating default MCP ask mode")
    assert resolve_default_search_kwargs() == {"mode": "pro", "sources": ["web"]}


def test_default_mcp_mode_supports_reasoning_and_research() -> None:
    print("console.log -> validating explicit MCP ask modes")
    assert resolve_default_search_kwargs("reasoning")["mode"] == "reasoning"
    assert resolve_default_search_kwargs("deep research") == {"mode": "deep research"}


def test_load_cookies_prefers_json_cookie_env(monkeypatch) -> None:
    print("console.log -> validating PERPLEXITY_COOKIES support")
    monkeypatch.setenv("PERPLEXITY_COOKIES", json.dumps({"custom": "cookie"}))
    monkeypatch.setenv("PERPLEXITY_SESSION_TOKEN", "session")
    monkeypatch.setenv("PERPLEXITY_CSRF_TOKEN", "csrf")

    assert load_cookies_from_env() == {"custom": "cookie"}


def test_load_cookies_builds_nextauth_cookie_names(monkeypatch) -> None:
    print("console.log -> validating session/csrf env cookie support")
    monkeypatch.delenv("PERPLEXITY_COOKIES", raising=False)
    monkeypatch.setenv("PERPLEXITY_SESSION_TOKEN", "session")
    monkeypatch.setenv("PERPLEXITY_CSRF_TOKEN", "csrf")

    cookies = load_cookies_from_env()

    assert cookies["next-auth.session-token"] == "session"
    assert cookies["__Secure-next-auth.session-token"] == "session"
    assert cookies["next-auth.csrf-token"] == "csrf"
    assert cookies["__Host-next-auth.csrf-token"] == "csrf"


def test_load_cookies_exits_on_invalid_json(monkeypatch) -> None:
    print("console.log -> validating invalid cookie JSON fails")
    monkeypatch.setenv("PERPLEXITY_COOKIES", "not-json")

    with pytest.raises(SystemExit):
        load_cookies_from_env()


def test_tools_refresh_and_forward_model_overrides(monkeypatch):
    client = SimpleNamespace(own=True, search=Mock(return_value={"answer": "answer"}))
    models = Mock()
    models.resolve_model.side_effect = lambda model=None: model or "gpt6_1_sol_thinking"
    monkeypatch.setattr(server, "client", client, raising=False)
    monkeypatch.setattr(server, "models", models, raising=False)
    monkeypatch.setattr(server, "DEFAULT_MODEL", "gpt6_1_sol_thinking")

    assert server.perplexity_reason("question") == "answer"
    client.search.assert_called_with("question", mode="reasoning", model="gpt6_1_sol_thinking")
    server.perplexity_reason("question", model="claude55sonnetthinking")
    client.search.assert_called_with("question", mode="reasoning", model="claude55sonnetthinking")
    server.perplexity_search("question", model="gpt6_1_sol")
    client.search.assert_called_with("question", mode="pro", model="gpt6_1_sol", sources=["web"])
    server.perplexity_ask("question", model="gemini38flash")
    client.search.assert_called_with("question", mode="pro", model="gemini38flash", sources=["web"])
    server.perplexity_research("question")
    assert models.refresh.call_count == 5
    server.perplexity_models(refresh=True)
    models.list_models.assert_called_once_with("gpt6_1_sol_thinking", refresh=True)


def test_authenticated_auto_mode_is_rejected():
    with pytest.raises(ValueError, match="auto is disabled"):
        resolve_default_search_kwargs("auto")


def test_anonymous_ask_rejects_model_selection(monkeypatch):
    client = SimpleNamespace(own=False, search=Mock(return_value={"answer": "answer"}))
    monkeypatch.setattr(server, "client", client, raising=False)
    assert server.perplexity_ask("question") == "answer"
    client.search.assert_called_once_with("question", mode="auto")
    with pytest.raises(ValueError, match="authentication"):
        server.perplexity_ask("question", model="gpt6_1_sol")


@pytest.mark.parametrize("mode", ["search", "reasoning"])
def test_ask_uses_environment_override_and_account_default(monkeypatch, mode):
    client = SimpleNamespace(own=True, search=Mock(return_value={"answer": "answer"}))
    models = Mock()
    models.resolve_model.side_effect = lambda model=None: model or "gpt6_astra_thinking"
    monkeypatch.setattr(server, "client", client, raising=False)
    monkeypatch.setattr(server, "models", models, raising=False)
    monkeypatch.setattr(
        server, "resolve_default_search_kwargs", lambda: resolve_default_search_kwargs(mode)
    )
    monkeypatch.setattr(server, "DEFAULT_MODEL", None)
    server.perplexity_ask("question")
    assert client.search.call_args.kwargs["model"] == "gpt6_astra_thinking"
    monkeypatch.setattr(server, "DEFAULT_MODEL", "gpt6_1_sol_thinking")
    server.perplexity_ask("question")
    assert client.search.call_args.kwargs["model"] == "gpt6_1_sol_thinking"
