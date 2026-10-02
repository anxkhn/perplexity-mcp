"""Checks for the bundled current-picker catalog."""

from perplexity import config


def test_api_endpoints_structure():
    assert config.ENDPOINT_MODEL_CONFIG == "https://www.perplexity.ai/rest/models/config/v2"
    assert config.ENDPOINT_SSE_ASK.startswith(config.API_BASE_URL)


def test_catalog_contains_every_picker_id_and_no_legacy_models():
    picker_ids = set()
    for entries, fields in (
        (config.SEARCH_MODEL_CONFIG, ("non_reasoning_model", "reasoning_model")),
        (config.COMPUTER_MODEL_CONFIG, ("model", "fast_model")),
    ):
        for entry in entries:
            picker_ids.update(entry[field] for field in fields if entry.get(field))
    assert set(config.MODEL_CATALOG) == picker_ids | {
        "pplx_alpha",
        "pplx_agentic_research",
        "pplx_study",
    }
    assert len(picker_ids) == 31
    assert "gpt56_sol_thinking" not in config.MODEL_CATALOG
    assert "claude50sonnetthinking" not in config.MODEL_CATALOG
    assert "pplx_pro" not in config.MODEL_CATALOG
    assert "turbo" not in config.MODEL_CATALOG
    assert config.MODEL_MAPPINGS["reasoning"][None] == "gpt6_1_sol_thinking"
    assert config.MODEL_MAPPINGS["pro"]["gpt-6.1-sol-thinking"] == "gpt6_1_sol_thinking"
    assert "pplx_asi_astra" not in config.MODEL_MAPPINGS["pro"]
    assert set(config.MODEL_ALIASES.values()) <= set(config.MODEL_CATALOG)
    assert all("non_reasoning_model" in entry for entry in config.MODEL_SELECTOR_CONFIG)
