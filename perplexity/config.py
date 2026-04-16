"""
Configuration constants for Perplexity AI API.

This module contains all configurable constants used throughout the library.
Modify these values to customize behavior without changing core code.
"""

from typing import Dict

# API Configuration
API_BASE_URL = "https://www.perplexity.ai"
API_VERSION = "2.18"
API_TIMEOUT = 30

# Endpoints
ENDPOINT_AUTH_SESSION = f"{API_BASE_URL}/api/auth/session"
ENDPOINT_AUTH_SIGNIN = f"{API_BASE_URL}/api/auth/signin/email"
ENDPOINT_SSE_ASK = f"{API_BASE_URL}/rest/sse/perplexity_ask"
ENDPOINT_UPLOAD_URL = f"{API_BASE_URL}/rest/uploads/create_upload_url"
ENDPOINT_SOCKET_IO = f"{API_BASE_URL}/socket.io/"

# Emailnator Configuration
EMAILNATOR_BASE_URL = "https://www.emailnator.com"
EMAILNATOR_GENERATE_ENDPOINT = f"{EMAILNATOR_BASE_URL}/generate-email"
EMAILNATOR_MESSAGE_LIST_ENDPOINT = f"{EMAILNATOR_BASE_URL}/message-list"

# Account Limits
DEFAULT_COPILOT_QUERIES = 5
DEFAULT_FILE_UPLOADS = 10
ACCOUNT_TIMEOUT = 20  # seconds to wait for email

# Search Modes
SEARCH_MODES = ["auto", "pro", "reasoning", "deep research"]
SEARCH_SOURCES = ["web", "scholar", "social"]
SEARCH_LANGUAGES = ["en-US", "en-GB", "pt-BR", "es-ES", "fr-FR", "de-DE"]

# Model Mappings
#
# Authenticated queries route through the same search endpoint with a backend
# model preference. We keep the external API stable by accepting both the
# user-facing names (for example ``claude-4.6-sonnet-thinking``) and the raw
# backend identifiers emitted by Perplexity (for example
# ``claude46sonnetthinking``).
RAW_MODEL_IDS = {
    "turbo",
    "pplx_pro",
    "pplx_pro_upgraded",
    "experimental",
    "gpt4o",
    "gpt41",
    "gpt5",
    "gpt5_thinking",
    "gpt51",
    "gpt51_thinking",
    "gpt51_low_thinking",
    "gpt5_mini",
    "gpt5_nano",
    "gpt5_pro",
    "chatgpt_tools",
    "gpt52",
    "gpt52_thinking",
    "gpt52_pro",
    "gpt54",
    "gpt54_thinking",
    "claude2",
    "claude37sonnetthinking",
    "claude40sonnetthinking",
    "gemini25pro",
    "gemini30pro",
    "gemini30flash",
    "gemini30flash_high",
    "gemini31pro_low",
    "gemini31pro_high",
    "grok",
    "claude40opus",
    "claude40opusthinking",
    "claude41opus",
    "claude41opusthinking",
    "claude45opus",
    "claude45opusthinking",
    "claude46opus",
    "claude46opusthinking",
    "claude45sonnet",
    "claude45sonnetthinking",
    "claude46sonnet",
    "claude46sonnetthinking",
    "claude45haiku",
    "claude45haikuthinking",
    "kimik2thinking",
    "kimik25thinking",
    "grok4",
    "grok4nonthinking",
    "grok41reasoning",
    "grok41nonreasoning",
    "nv_nemotron_3_super",
    "o4mini",
    "o3pro",
    "pplx_sonar_internal_testing",
    "pplx_sonar_internal_testing_v2",
    "pplx_alpha",
    "pplx_beta",
    "pplx_study",
    "pplx_agentic_research",
    "pplx_asi",
    "pplx_asi_opus",
    "pplx_asi_opus_thinking",
    "pplx_asi_gpt54",
    "pplx_asi_kimi",
    "pplx_asi_qwen",
    "pplx_asi_sonnet",
    "pplx_asi_sonnet_thinking",
    "pplx_business_assistant",
    "pplx_document_review",
    "comet_browser_agent_sonnet",
    "comet_browser_agent_opus",
    "claudecode",
    "codex",
    "gpt53codex",
    "nanobananapro",
    "nanobanana2",
    "sora2",
    "sora2pro",
    "veo31",
    "veo31fast",
}

MODEL_ALIASES = {
    "turbo": "turbo",
    "sonar": "experimental",
    "pplx-pro": "pplx_pro",
    "pplx-pro-upgraded": "pplx_pro_upgraded",
    "gpt-4o": "gpt4o",
    "gpt-4.1": "gpt41",
    "gpt-5": "gpt5",
    "gpt-5-thinking": "gpt5_thinking",
    "gpt-5.1": "gpt51",
    "gpt-5.1-thinking": "gpt51_thinking",
    "gpt-5.1-low-thinking": "gpt51_low_thinking",
    "gpt-5-mini": "gpt5_mini",
    "gpt-5-nano": "gpt5_nano",
    "gpt-5-pro": "gpt5_pro",
    "chatgpt-tools": "chatgpt_tools",
    "gpt-5.2": "gpt52",
    "gpt-5.2-thinking": "gpt52_thinking",
    "gpt-5.2-pro": "gpt52_pro",
    "gpt-5.4": "gpt54",
    "gpt-5.4-thinking": "gpt54_thinking",
    "claude-4.0-sonnet": "claude2",
    "claude-4.0-sonnet-thinking": "claude40sonnetthinking",
    "claude-3.7-sonnet-thinking": "claude37sonnetthinking",
    "claude-4.0-opus": "claude40opus",
    "claude-4.0-opus-thinking": "claude40opusthinking",
    "claude-4.1-opus": "claude41opus",
    "claude-4.1-opus-thinking": "claude41opusthinking",
    "claude-4.5-opus": "claude45opus",
    "claude-4.5-opus-thinking": "claude45opusthinking",
    "claude-4.6-opus": "claude46opus",
    "claude-4.6-opus-thinking": "claude46opusthinking",
    "claude-4.5-sonnet": "claude45sonnet",
    "claude-4.5-sonnet-thinking": "claude45sonnetthinking",
    "claude-4.6-sonnet": "claude46sonnet",
    "claude-4.6-sonnet-thinking": "claude46sonnetthinking",
    "claude-4.5-haiku": "claude45haiku",
    "claude-4.5-haiku-thinking": "claude45haikuthinking",
    "gemini-2.5-pro": "gemini25pro",
    "gemini-3.0-pro": "gemini30pro",
    "gemini-3.0-flash": "gemini30flash",
    "gemini-3.0-flash-thinking": "gemini30flash_high",
    "gemini-3.1-pro": "gemini31pro_low",
    "gemini-3.1-pro-thinking": "gemini31pro_high",
    "grok-3-beta": "grok",
    "grok-4": "grok4nonthinking",
    "grok-4-thinking": "grok4",
    "grok-4-reasoning": "grok4",
    "grok-4.1": "grok41nonreasoning",
    "grok-4.1-thinking": "grok41reasoning",
    "grok-4.1-reasoning": "grok41reasoning",
    "kimi-k2-thinking": "kimik2thinking",
    "kimi-k2.5-thinking": "kimik25thinking",
    "nemotron-3-super": "nv_nemotron_3_super",
    "o4-mini": "o4mini",
    "o3-pro": "o3pro",
    "deep-research": "pplx_alpha",
    "study": "pplx_study",
    "studio": "pplx_beta",
    "agentic-research": "pplx_agentic_research",
    "document-review": "pplx_document_review",
    "computer": "pplx_asi",
    "computer-opus": "pplx_asi_opus",
    "computer-opus-thinking": "pplx_asi_opus_thinking",
    "computer-gpt-5.4": "pplx_asi_gpt54",
    "computer-kimi": "pplx_asi_kimi",
    "computer-qwen": "pplx_asi_qwen",
    "computer-sonnet": "pplx_asi_sonnet",
    "computer-sonnet-thinking": "pplx_asi_sonnet_thinking",
    "business-assistant": "pplx_business_assistant",
    "browser-agent-sonnet": "comet_browser_agent_sonnet",
    "browser-agent-opus": "comet_browser_agent_opus",
    "claude-code": "claudecode",
    "codex": "codex",
    "gpt-5.3-codex": "gpt53codex",
    "nano-banana-pro": "nanobananapro",
    "nano-banana-2": "nanobanana2",
    "sora-2": "sora2",
    "sora-2-pro": "sora2pro",
    "veo-3.1": "veo31",
    "veo-3.1-fast": "veo31fast",
}

NON_AUTO_MODEL_MAPPINGS: Dict[str, str] = {
    model_id: model_id for model_id in RAW_MODEL_IDS
}
NON_AUTO_MODEL_MAPPINGS.update(MODEL_ALIASES)

MODEL_MAPPINGS: Dict[str, Dict[str, str]] = {
    "auto": {None: "turbo", "turbo": "turbo"},
    "pro": {None: "pplx_pro", **NON_AUTO_MODEL_MAPPINGS},
    "reasoning": {None: "pplx_reasoning", **NON_AUTO_MODEL_MAPPINGS},
    "deep research": {
        None: "pplx_alpha",
        "pplx_alpha": "pplx_alpha",
        "deep-research": "pplx_alpha",
    },
}

# Labs Models
LABS_MODELS = [
    "r1-1776",
    "sonar-pro",
    "sonar",
    "sonar-reasoning-pro",
    "sonar-reasoning",
]

# HTTP Headers Template
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
    "sec-ch-ua-full-version-list": '"Not;A=Brand";v="24.0.0.0", "Chromium";v="128.0.6613.120"',  # noqa: E501
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

# Emailnator Headers Template
EMAILNATOR_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "dnt": "1",
    "origin": EMAILNATOR_BASE_URL,
    "priority": "u=1, i",
    "referer": f"{EMAILNATOR_BASE_URL}/",
    "sec-ch-ua": '"Not;A=Brand";v="24", "Chromium";v="128"',
    "sec-ch-ua-arch": '"x86"',
    "sec-ch-ua-bitness": '"64"',
    "sec-ch-ua-full-version": '"128.0.6613.120"',
    "sec-ch-ua-full-version-list": '"Not;A=Brand";v="24.0.0.0", "Chromium";v="128.0.6613.120"',  # noqa: E501
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": '""',
    "sec-ch-ua-platform": '"Windows"',
    "sec-ch-ua-platform-version": '"19.0.0"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",  # noqa: E501
    "x-requested-with": "XMLHttpRequest",
}

# Retry Configuration
RETRY_MAX_ATTEMPTS = 3
RETRY_BACKOFF_FACTOR = 2
RETRY_EXCEPTIONS = (ConnectionError, TimeoutError)

# Logging Configuration
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"
LOG_FILE = "perplexity.log"

# Rate Limiting
RATE_LIMIT_MIN_DELAY = 1.0  # seconds
RATE_LIMIT_MAX_DELAY = 3.0  # seconds
RATE_LIMIT_ENABLED = True

# Validation Patterns
EMAIL_SUBJECT_PATTERN = "Sign in to Perplexity"
SIGNIN_URL_PATTERN = (
    r'"(https://www\.perplexity\.ai/api/auth/callback/email\?callbackUrl=.*?)"'
)
