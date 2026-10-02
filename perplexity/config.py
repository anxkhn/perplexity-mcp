"""Configuration and the current Perplexity model-picker fallback."""

API_BASE_URL = "https://www.perplexity.ai"
API_VERSION = "2.18"
API_TIMEOUT = 30
ENDPOINT_AUTH_SESSION = f"{API_BASE_URL}/api/auth/session"
ENDPOINT_AUTH_SIGNIN = f"{API_BASE_URL}/api/auth/signin/email"
ENDPOINT_SSE_ASK = f"{API_BASE_URL}/rest/sse/perplexity_ask"
ENDPOINT_MODEL_CONFIG = f"{API_BASE_URL}/rest/models/config/v2"
ENDPOINT_UPLOAD_URL = f"{API_BASE_URL}/rest/uploads/create_upload_url"
ENDPOINT_SOCKET_IO = f"{API_BASE_URL}/socket.io/"

EMAILNATOR_BASE_URL = "https://www.emailnator.com"
EMAILNATOR_GENERATE_ENDPOINT = f"{EMAILNATOR_BASE_URL}/generate-email"
EMAILNATOR_MESSAGE_LIST_ENDPOINT = f"{EMAILNATOR_BASE_URL}/message-list"
DEFAULT_COPILOT_QUERIES = 5
DEFAULT_FILE_UPLOADS = 10
ACCOUNT_TIMEOUT = 20
SEARCH_MODES = ["auto", "pro", "reasoning", "deep research"]
SEARCH_SOURCES = ["web", "scholar", "social"]
SEARCH_LANGUAGES = ["en-US", "en-GB", "pt-BR", "es-ES", "fr-FR", "de-DE"]
MODEL_CONFIG_SCHEMA = "v2"
DEFAULT_REASONING_MODEL = "gpt6_1_sol_thinking"

# Snapshot of /rest/models/config/v2 picker choices on 2026-10-02.
SEARCH_MODEL_CONFIG = [
    {
        "label": "Claude Sonnet 5",
        "subscription_tier": "pro",
        "non_reasoning_model": "comet_browser_agent_sonnet",
        "reasoning_model": None,
    },
    {
        "label": "Claude Opus 4.8",
        "subscription_tier": "max",
        "non_reasoning_model": "comet_browser_agent_opus",
        "reasoning_model": None,
    },
    {
        "label": "GPT-6.1 Sol",
        "subscription_tier": "pro",
        "non_reasoning_model": "gpt6_1_sol",
        "reasoning_model": "gpt6_1_sol_thinking",
    },
    {
        "label": "GPT-6 Astra",
        "subscription_tier": "max",
        "non_reasoning_model": "gpt6_astra",
        "reasoning_model": "gpt6_astra_thinking",
    },
    {
        "label": "Gemini 3.8 Flash",
        "subscription_tier": "pro",
        "non_reasoning_model": "gemini38flash",
        "reasoning_model": "gemini38flashthinking",
    },
    {
        "label": "Claude Sonnet 5.5",
        "subscription_tier": "pro",
        "non_reasoning_model": "claude55sonnet",
        "reasoning_model": "claude55sonnetthinking",
    },
    {
        "label": "Claude Opus 5.5",
        "subscription_tier": "max",
        "non_reasoning_model": "claude55opus",
        "reasoning_model": "claude55opusthinking",
    },
    {
        "label": "Claude Fable 5.1",
        "subscription_tier": "max",
        "non_reasoning_model": "claudefable51",
        "reasoning_model": "claudefable51thinking",
    },
    {
        "label": "Kimi K3",
        "subscription_tier": "pro",
        "non_reasoning_model": None,
        "reasoning_model": "kimik3thinking",
    },
    {
        "label": "GLM 5.3",
        "subscription_tier": "pro",
        "non_reasoning_model": None,
        "reasoning_model": "glm_5_3_thinking",
    },
    {
        "label": "Grok 4.7",
        "subscription_tier": "pro",
        "non_reasoning_model": "grok47",
        "reasoning_model": "grok47thinking",
    },
    {
        "label": "Nemotron 3 Ultra",
        "subscription_tier": "pro",
        "non_reasoning_model": None,
        "reasoning_model": "nv_nemotron_3_ultra",
    },
]
COMPUTER_MODEL_CONFIG = [
    {
        "label": "GPT-6 Astra",
        "subscription_tier": "pro",
        "model": "pplx_asi_astra",
        "fast_model": "pplx_asi_astra_fast",
    },
    {
        "label": "GPT-6.1 Sol",
        "subscription_tier": "pro",
        "model": "pplx_asi_gpt_6_1_sol",
        "fast_model": "pplx_asi_gpt_6_1_sol_fast",
    },
    {
        "label": "Claude Fable 5.1",
        "subscription_tier": "pro",
        "model": "pplx_asi_fable_5",
        "fast_model": None,
    },
    {
        "label": "Claude Opus 5.5",
        "subscription_tier": "pro",
        "model": "pplx_asi_opus",
        "fast_model": "pplx_asi_opus_fast",
    },
    {
        "label": "Claude Sonnet 5.5",
        "subscription_tier": "pro",
        "model": "pplx_asi_sonnet",
        "fast_model": None,
    },
    {
        "label": "GLM 5.3",
        "subscription_tier": "pro",
        "model": "pplx_asi_glm_5_3",
        "fast_model": None,
    },
    {
        "label": "Kimi K3",
        "subscription_tier": "pro",
        "model": "pplx_asi_kimi_k3",
        "fast_model": None,
    },
    {"label": "Grok 4.7", "subscription_tier": "pro", "model": "pplx_asi_grok", "fast_model": None},
    {
        "label": "DeepSeek V4 Pro",
        "subscription_tier": "pro",
        "model": "pplx_asi_deepseek_v4_pro",
        "fast_model": None,
    },
]


def picker_models(data):
    """Keep picker IDs plus named research workflows, excluding old catalog entries."""
    ids = {"pplx_alpha", "pplx_agentic_research", "pplx_study", data["default_models"]["research"]}
    for section, fields in (
        ("search_config", ("non_reasoning_model", "reasoning_model")),
        ("computer_config", ("model", "fast_model")),
    ):
        for entry in data[section]:
            ids.update(entry[field] for field in fields if entry.get(field))
    return {key: value for key, value in data["models"].items() if key in ids}


MODEL_CATALOG = {}


def model_provider(model_id):
    if model_id.startswith(("gpt", "pplx_asi_gpt", "pplx_asi_astra")):
        return "OPENAI"
    if model_id.startswith(
        ("claude", "comet", "pplx_asi_fable", "pplx_asi_opus", "pplx_asi_sonnet")
    ):
        return "ANTHROPIC"
    if "gemini" in model_id:
        return "GOOGLE"
    if "kimi" in model_id:
        return "MOONSHOT_AI"
    if "glm" in model_id:
        return "ZAI"
    if "grok" in model_id:
        return "XAI"
    if "nemotron" in model_id:
        return "NVIDIA"
    if "deepseek" in model_id:
        return "DEEPSEEK"
    return "PERPLEXITY"


for entry in SEARCH_MODEL_CONFIG:
    for field in ("non_reasoning_model", "reasoning_model"):
        model_id = entry[field]
        if model_id:
            MODEL_CATALOG[model_id] = {
                "label": entry["label"] + (" Thinking" if field == "reasoning_model" else ""),
                "mode": "browser_agent" if model_id.startswith("comet_") else "search",
                "provider": model_provider(model_id),
            }
for entry in COMPUTER_MODEL_CONFIG:
    for field in ("model", "fast_model"):
        if entry[field]:
            MODEL_CATALOG[entry[field]] = {
                "label": entry["label"] + (" Fast" if field == "fast_model" else ""),
                "mode": "asi",
                "provider": model_provider(entry[field]),
            }
MODEL_CATALOG.update(
    {
        "pplx_alpha": {"label": "Deep research", "mode": "research"},
        "pplx_agentic_research": {"label": "Agentic research", "mode": "agentic_research"},
        "pplx_study": {"label": "Study", "mode": "study"},
    }
)
DEFAULT_MODELS = {"search": DEFAULT_REASONING_MODEL, "research": "pplx_alpha"}
AGENTIC_RESEARCH_COMPARE_MODELS = ["gpt6_1_sol_thinking", "gemini38flashthinking"]
MODEL_SELECTOR_CONFIG = SEARCH_MODEL_CONFIG + [
    {
        **entry,
        "non_reasoning_model": entry["model"],
        "reasoning_model": None,
    }
    for entry in COMPUTER_MODEL_CONFIG
]
MODEL_CONFIG = {
    "config_schema": MODEL_CONFIG_SCHEMA,
    "models": MODEL_CATALOG,
    "config": MODEL_SELECTOR_CONFIG,
    "search_config": SEARCH_MODEL_CONFIG,
    "computer_config": COMPUTER_MODEL_CONFIG,
    "default_models": DEFAULT_MODELS,
    "agentic_research_compare_models": AGENTIC_RESEARCH_COMPARE_MODELS,
}
MODEL_ALIASES = {
    "gpt-6.1-sol": "gpt6_1_sol",
    "gpt-6.1-sol-thinking": "gpt6_1_sol_thinking",
    "gpt-6-astra": "gpt6_astra",
    "gpt-6-astra-thinking": "gpt6_astra_thinking",
    "gemini-3.8-flash": "gemini38flash",
    "gemini-3.8-flash-thinking": "gemini38flashthinking",
    "claude-5.5-sonnet": "claude55sonnet",
    "claude-5.5-sonnet-thinking": "claude55sonnetthinking",
    "claude-5.5-opus": "claude55opus",
    "claude-5.5-opus-thinking": "claude55opusthinking",
    "claude-fable-5.1": "claudefable51",
    "claude-fable-5.1-thinking": "claudefable51thinking",
    "kimi-k3": "kimik3thinking",
    "glm-5.3": "glm_5_3_thinking",
    "grok-4.7": "grok47",
    "grok-4.7-thinking": "grok47thinking",
    "nemotron-3-ultra": "nv_nemotron_3_ultra",
    "browser-agent-sonnet": "comet_browser_agent_sonnet",
    "browser-agent-opus": "comet_browser_agent_opus",
    "computer-astra": "pplx_asi_astra",
    "computer-astra-fast": "pplx_asi_astra_fast",
    "computer-gpt-6.1-sol": "pplx_asi_gpt_6_1_sol",
    "computer-gpt-6.1-sol-fast": "pplx_asi_gpt_6_1_sol_fast",
    "computer-fable-5.1": "pplx_asi_fable_5",
    "computer-opus": "pplx_asi_opus",
    "computer-opus-fast": "pplx_asi_opus_fast",
    "computer-sonnet": "pplx_asi_sonnet",
    "computer-glm-5.3": "pplx_asi_glm_5_3",
    "computer-kimi-k3": "pplx_asi_kimi_k3",
    "computer-grok-4.7": "pplx_asi_grok",
    "computer-deepseek-v4-pro": "pplx_asi_deepseek_v4_pro",
    "deep-research": "pplx_alpha",
    "agentic-research": "pplx_agentic_research",
    "study": "pplx_study",
}
RAW_MODEL_IDS = set(MODEL_CATALOG)
NON_AUTO_MODEL_MAPPINGS = {
    key: key for key, value in MODEL_CATALOG.items() if value["mode"] == "search"
}
NON_AUTO_MODEL_MAPPINGS.update(
    {alias: target for alias, target in MODEL_ALIASES.items() if target in NON_AUTO_MODEL_MAPPINGS}
)
MODEL_MAPPINGS = {
    "auto": {None: "turbo", "turbo": "turbo"},
    "pro": {None: DEFAULT_REASONING_MODEL, **NON_AUTO_MODEL_MAPPINGS},
    "reasoning": {None: DEFAULT_REASONING_MODEL, **NON_AUTO_MODEL_MAPPINGS},
    "deep research": {
        None: "pplx_alpha",
        "pplx_alpha": "pplx_alpha",
        "deep-research": "pplx_alpha",
    },
}
LABS_MODELS = ["r1-1776", "sonar-pro", "sonar", "sonar-reasoning-pro", "sonar-reasoning"]

DEFAULT_HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",  # noqa: E501
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "dnt": "1",
    "priority": "u=0, i",
    "sec-ch-ua": '"Not;A=Brand";v="24", "Chromium";v="128"',
    "sec-ch-ua-arch": '"x86"',
    "sec-ch-ua-bitness": '"64"',
    "sec-ch-ua-full-version": '"128.0.6613.120"',
    "sec-ch-ua-full-version-list": '"Not;A=Brand";v="24.0.0.0", "Chromium";v="128.0.6613.120"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": '""',
    "sec-ch-ua-platform": '"Windows"',
    "sec-ch-ua-platform-version": '"19.0.0"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",  # noqa: E501
}
EMAILNATOR_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "dnt": "1",
    "origin": EMAILNATOR_BASE_URL,
    "priority": "u=1, i",
    "referer": f"{EMAILNATOR_BASE_URL}/",
    "sec-ch-ua": '"Not;A=Brand";v="24", "Chromium";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-ch-ua-arch": '"x86"',
    "sec-ch-ua-bitness": '"64"',
    "sec-ch-ua-full-version": '"128.0.6613.120"',
    "sec-ch-ua-full-version-list": '"Not;A=Brand";v="24.0.0.0", "Chromium";v="128.0.6613.120"',
    "sec-ch-ua-model": '""',
    "sec-ch-ua-platform-version": '"19.0.0"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": DEFAULT_HEADERS["user-agent"],
    "x-requested-with": "XMLHttpRequest",
}
RETRY_MAX_ATTEMPTS = 3
RETRY_BACKOFF_FACTOR = 2
RETRY_EXCEPTIONS = (ConnectionError, TimeoutError)
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"
LOG_FILE = None
RATE_LIMIT_MIN_DELAY = 1.0
RATE_LIMIT_MAX_DELAY = 3.0
RATE_LIMIT_ENABLED = True
EMAIL_SUBJECT_PATTERN = "Sign in to Perplexity"
SIGNIN_URL_PATTERN = r'"(https://www\.perplexity\.ai/api/auth/callback/email\?callbackUrl=.*?)"'
