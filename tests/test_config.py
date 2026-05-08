"""Smoke tests for perplexity.config with console-style output."""

from perplexity import config


def test_api_endpoints_structure() -> None:
    print("console.log -> validating API endpoints and versions")
    assert config.API_BASE_URL.startswith("https://")
    assert config.API_VERSION.count(".") >= 1
    assert config.ENDPOINT_SSE_ASK.startswith(config.API_BASE_URL)
    assert config.EMAILNATOR_BASE_URL in config.EMAILNATOR_GENERATE_ENDPOINT


def test_search_modes_and_models() -> None:
    print("console.log -> checking search modes and model mappings")
    assert set(config.SEARCH_MODES) >= {"auto", "pro", "reasoning"}
    assert config.MODEL_CONFIG_SCHEMA == "v1"
    assert config.DEFAULT_MODELS["search"] == "pplx_pro"
    pro_models = config.MODEL_MAPPINGS["pro"]
    assert None in pro_models
    assert "sonar" in pro_models
    assert "gpt-5.5" in pro_models
    assert pro_models["gpt-5.5"] == "gpt55"
    assert "claude-4.7-opus-thinking" in config.MODEL_MAPPINGS["reasoning"]
    assert config.MODEL_MAPPINGS["reasoning"]["claude47opusthinking"] == "claude47opusthinking"
    assert config.MODEL_CATALOG["kimik26thinking"]["label"] == "Kimi K2.6 Thinking"
    assert config.DEFAULT_MODELS["browser_agent"] == "comet_browser_agent"
    assert config.AGENTIC_RESEARCH_COMPARE_MODELS == [
        "gpt55_thinking",
        "claude47opusthinking",
        "gemini31pro_high",
    ]
    assert "deep research" in config.MODEL_MAPPINGS
