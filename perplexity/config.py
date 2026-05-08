"""
Configuration constants for Perplexity AI API.

This module contains all configurable constants used throughout the library.
Modify these values to customize behavior without changing core code.
"""

from typing import Dict, List

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
# user-facing names (for example ``claude-4.7-opus-thinking``) and the raw
# backend identifiers emitted by Perplexity (for example
# ``claude47opusthinking``).
MODEL_CONFIG_SCHEMA = "v1"

MODEL_CATALOG: Dict[str, Dict[str, object]] = {
    "turbo": {
        "label": "Best",
        "description": "Adapts to each query",
        "mode": "search",
        "provider": "PERPLEXITY",
    },
    "pplx_pro": {
        "label": "Best",
        "description": "Automatically selects the best model based on the query",
        "mode": "search",
        "provider": None,
    },
    "pplx_pro_upgraded": {
        "label": "Pro",
        "description": "Automatically selects the most responsive model based on the query",
        "mode": "search",
        "provider": "PERPLEXITY",
    },
    "experimental": {
        "label": "Sonar 2",
        "description": "Perplexity's latest in-house model.",
        "mode": "search",
        "provider": "PERPLEXITY",
    },
    "gpt4o": {
        "label": "GPT-4o",
        "description": "OpenAI's versatile model",
        "mode": "search",
        "provider": "OPENAI",
    },
    "gpt41": {
        "label": "GPT-4.1",
        "description": "OpenAI's advanced model",
        "mode": "search",
        "provider": "OPENAI",
    },
    "gpt5": {
        "label": "GPT-5",
        "description": "OpenAI's latest model",
        "mode": "search",
        "provider": "OPENAI",
    },
    "gpt5_thinking": {
        "label": "GPT-5 Thinking",
        "description": "OpenAI's latest model with thinking",
        "mode": "search",
        "provider": "OPENAI",
    },
    "gpt51": {
        "label": "GPT-5.1",
        "description": "OpenAI's latest model",
        "mode": "search",
        "provider": "OPENAI",
    },
    "gpt51_thinking": {
        "label": "GPT-5.1 Thinking",
        "description": "OpenAI's latest model with thinking",
        "mode": "search",
        "provider": "OPENAI",
    },
    "gpt51_low_thinking": {
        "label": "GPT-5.1 Low Thinking",
        "description": "OpenAI's latest model with low reasoning effort",
        "mode": "search",
        "provider": "OPENAI",
    },
    "gpt5_mini": {
        "label": "GPT-5 Mini",
        "description": "OpenAI's compact model",
        "mode": "search",
        "provider": "OPENAI",
    },
    "gpt5_nano": {
        "label": "GPT-5 Nano",
        "description": "OpenAI's smallest model",
        "mode": "search",
        "provider": "OPENAI",
    },
    "gpt5_pro": {
        "label": "GPT-5 Pro",
        "description": "OpenAI's latest, most powerful reasoning model",
        "mode": "search",
        "provider": "OPENAI",
    },
    "chatgpt_tools": {
        "label": "ChatGPT Tools",
        "description": "OpenAI's tool-enabled model",
        "mode": "search",
        "provider": "OPENAI",
    },
    "gpt52": {
        "label": "GPT-5.2",
        "description": "OpenAI's latest model",
        "mode": "search",
        "provider": "OPENAI",
    },
    "gpt52_thinking": {
        "label": "GPT-5.2 Thinking",
        "description": "OpenAI's latest model with thinking",
        "mode": "search",
        "provider": "OPENAI",
    },
    "gpt52_pro": {
        "label": "GPT-5.2 Pro",
        "description": "OpenAI's most powerful reasoning model",
        "mode": "search",
        "provider": "OPENAI",
    },
    "gpt54": {
        "label": "GPT-5.4",
        "description": "OpenAI's versatile model",
        "mode": "search",
        "provider": "OPENAI",
    },
    "gpt54_thinking": {
        "label": "GPT-5.4 Thinking",
        "description": "OpenAI's versatile model with thinking",
        "mode": "search",
        "provider": "OPENAI",
    },
    "gpt55": {
        "label": "GPT-5.5",
        "description": "OpenAI's latest model",
        "mode": "search",
        "provider": "OPENAI",
    },
    "gpt55_thinking": {
        "label": "GPT-5.5 Thinking",
        "description": "OpenAI's latest model with thinking",
        "mode": "search",
        "provider": "OPENAI",
    },
    "claude2": {
        "label": "Claude Sonnet 4.0",
        "description": "Anthropic's advanced model",
        "mode": "search",
        "provider": "ANTHROPIC",
    },
    "claude37sonnetthinking": {
        "label": "Claude Sonnet 4.0 Thinking",
        "description": "Anthropic's reasoning model",
        "mode": "search",
        "provider": "ANTHROPIC",
    },
    "claude40sonnetthinking": {
        "label": "Claude Sonnet 4.0 Thinking",
        "description": "Anthropic's reasoning model",
        "mode": "search",
        "provider": "ANTHROPIC",
    },
    "gemini25pro": {
        "label": "Gemini 2.5 Pro",
        "description": "Google's latest model",
        "mode": "search",
        "provider": "GOOGLE",
    },
    "gemini30pro": {
        "label": "Gemini 3 Pro",
        "description": "Google's most advanced model",
        "mode": "search",
        "provider": "GOOGLE",
    },
    "gemini30flash": {
        "label": "Gemini 3 Flash",
        "description": "Google's fast model",
        "mode": "search",
        "provider": "GOOGLE",
    },
    "gemini30flash_high": {
        "label": "Gemini 3 Flash Thinking",
        "description": "Google's fast model",
        "mode": "search",
        "provider": "GOOGLE",
    },
    "gemini31pro_low": {
        "label": "Gemini 3.1 Pro",
        "description": "Google's latest model",
        "mode": "search",
        "provider": "GOOGLE",
    },
    "gemini31pro_high": {
        "label": "Gemini 3.1 Pro Thinking",
        "description": "Google's latest model with thinking",
        "mode": "search",
        "provider": "GOOGLE",
    },
    "grok": {
        "label": "Grok 3 Beta",
        "description": "xAI's Grok 3 model",
        "mode": "search",
        "provider": "XAI",
    },
    "claude40opus": {
        "label": "Claude Opus 4.0",
        "description": "Anthropic's Opus reasoning model",
        "mode": "search",
        "provider": "ANTHROPIC",
    },
    "claude40opusthinking": {
        "label": "Claude Opus 4.0 Thinking",
        "description": "Anthropic's Opus reasoning model with thinking",
        "mode": "search",
        "provider": "ANTHROPIC",
    },
    "claude41opus": {
        "label": "Claude Opus 4.1",
        "description": "Anthropic's Opus reasoning model",
        "mode": "search",
        "provider": "ANTHROPIC",
    },
    "claude41opusthinking": {
        "label": "Claude Opus 4.1 Thinking",
        "description": "Anthropic's Opus reasoning model with thinking",
        "mode": "search",
        "provider": "ANTHROPIC",
    },
    "claude45opus": {
        "label": "Claude Opus 4.5",
        "description": "Anthropic's most advanced model",
        "mode": "search",
        "provider": "ANTHROPIC",
    },
    "claude45opusthinking": {
        "label": "Claude Opus 4.5 Thinking",
        "description": "Anthropic's Opus reasoning model with thinking",
        "mode": "search",
        "provider": "ANTHROPIC",
    },
    "claude46opus": {
        "label": "Claude Opus 4.6",
        "description": "Anthropic's most advanced model",
        "mode": "search",
        "provider": "ANTHROPIC",
    },
    "claude46opusthinking": {
        "label": "Claude Opus 4.6 Thinking",
        "description": "Anthropic's Opus reasoning model with thinking",
        "mode": "search",
        "provider": "ANTHROPIC",
    },
    "claude47opus": {
        "label": "Claude Opus 4.7",
        "description": "Anthropic's most advanced model",
        "mode": "search",
        "provider": "ANTHROPIC",
    },
    "claude47opusthinking": {
        "label": "Claude Opus 4.7 Thinking",
        "description": "Anthropic's most advanced model with thinking",
        "mode": "search",
        "provider": "ANTHROPIC",
    },
    "claude45sonnet": {
        "label": "Claude Sonnet 4.5",
        "description": "Anthropic's fast model",
        "mode": "search",
        "provider": "ANTHROPIC",
    },
    "claude45sonnetthinking": {
        "label": "Claude Sonnet 4.5 Thinking",
        "description": "Anthropic's newest reasoning model",
        "mode": "search",
        "provider": "ANTHROPIC",
    },
    "claude46sonnet": {
        "label": "Claude Sonnet 4.6",
        "description": "Anthropic's fast model",
        "mode": "search",
        "provider": "ANTHROPIC",
    },
    "claude46sonnetthinking": {
        "label": "Claude Sonnet 4.6 Thinking",
        "description": "Anthropic's newest reasoning model",
        "mode": "search",
        "provider": "ANTHROPIC",
    },
    "claude45haiku": {
        "label": "Claude Haiku 4.5",
        "description": "Anthropic's compact model",
        "mode": "search",
        "provider": "ANTHROPIC",
    },
    "claude45haikuthinking": {
        "label": "Claude Haiku 4.5 Thinking",
        "description": "Anthropic's compact reasoning model",
        "mode": "search",
        "provider": "ANTHROPIC",
    },
    "kimik2thinking": {
        "label": "Kimi K2",
        "description": "Moonshot AI's latest model",
        "mode": "search",
        "provider": "MOONSHOT_AI",
    },
    "kimik25thinking": {
        "label": "Kimi K2.5 Thinking",
        "description": "Moonshot AI's latest model",
        "mode": "search",
        "provider": "MOONSHOT_AI",
    },
    "kimik26instant": {
        "label": "Kimi K2.6",
        "description": "Moonshot AI's latest model",
        "mode": "search",
        "provider": "MOONSHOT_AI",
    },
    "kimik26thinking": {
        "label": "Kimi K2.6 Thinking",
        "description": "Moonshot AI's latest model with Thinking",
        "mode": "search",
        "provider": "MOONSHOT_AI",
    },
    "grok4": {
        "label": "Grok 4",
        "description": "xAI's reasoning model",
        "mode": "search",
        "provider": "XAI",
    },
    "grok4nonthinking": {
        "label": "Grok 4",
        "description": "xAI's advanced model",
        "mode": "search",
        "provider": "XAI",
    },
    "grok41reasoning": {
        "label": "Grok 4.1",
        "description": "xAI's latest model",
        "mode": "search",
        "provider": "XAI",
    },
    "grok41nonreasoning": {
        "label": "Grok 4.1",
        "description": "xAI's latest model",
        "mode": "search",
        "provider": "XAI",
    },
    "nv_nemotron_3_super": {
        "label": "Nemotron 3 Super",
        "description": "NVIDIA's Nemotron 3 Super 120B model",
        "mode": "search",
        "provider": "NVIDIA",
    },
    "o4mini": {
        "label": "o4-mini",
        "description": "OpenAI's latest reasoning model",
        "mode": "research",
        "provider": "OPENAI",
    },
    "o3pro": {
        "label": "o3-pro",
        "description": "OpenAI's powerful reasoning model",
        "mode": "search",
        "provider": "OPENAI",
    },
    "pplx_sonar_internal_testing": {
        "label": "Sonar Testing - Alpha",
        "description": "Sonar model alpha variant",
        "mode": "search",
        "provider": "SONAR",
    },
    "pplx_sonar_internal_testing_v2": {
        "label": "Sonar Testing - Beta",
        "description": "Sonar model beta variant",
        "mode": "search",
        "provider": "SONAR",
    },
    "pplx_alpha": {
        "label": "Deep research",
        "description": "Fast and thorough for routine research",
        "mode": "research",
        "provider": "PERPLEXITY",
    },
    "pplx_beta": {
        "label": "Create files and apps",
        "description": "Multi-step tasks with advanced troubleshooting",
        "mode": "studio",
        "provider": "PERPLEXITY",
    },
    "pplx_study": {
        "label": "Study",
        "description": "Fast model for routine research",
        "mode": "study",
        "provider": "PERPLEXITY",
    },
    "pplx_agentic_research": {
        "label": "Agentic research",
        "description": "Delegate research tasks to specialized sub-agents",
        "mode": "agentic_research",
        "provider": "PERPLEXITY",
    },
    "pplx_asi": {
        "label": "Computer",
        "description": "Computer (default model)",
        "mode": "asi",
        "provider": "ANTHROPIC",
    },
    "pplx_asi_opus": {
        "label": "Claude Opus 4.7",
        "description": "Computer powered by Claude 4.7 Opus",
        "mode": "asi",
        "provider": "ANTHROPIC",
    },
    "pplx_asi_opus_thinking": {
        "label": "Claude Opus 4.7 Thinking",
        "description": "Computer powered by Claude 4.7 Opus with thinking",
        "mode": "asi",
        "provider": "ANTHROPIC",
    },
    "pplx_asi_gpt54": {
        "label": "GPT-5.4",
        "description": "Computer powered by GPT-5.4",
        "mode": "asi",
        "provider": "OPENAI",
    },
    "pplx_asi_gpt_55": {
        "label": "GPT-5.5",
        "description": "Computer powered by GPT-5.5",
        "mode": "asi",
        "provider": "OPENAI",
    },
    "pplx_asi_kimi": {
        "label": "Kimi K2.5",
        "description": "Computer powered by Kimi K2.5",
        "mode": "asi",
        "provider": "FIREWORKS",
    },
    "pplx_asi_qwen": {
        "label": "Qwen 3.6 Plus",
        "description": "Computer powered by Qwen 3.6 Plus",
        "mode": "asi",
        "provider": "FIREWORKS",
    },
    "pplx_asi_sonnet": {
        "label": "Claude Sonnet 4.6",
        "description": "Computer powered by Claude 4.6 Sonnet",
        "mode": "asi",
        "provider": "ANTHROPIC",
    },
    "pplx_asi_sonnet_thinking": {
        "label": "Claude Sonnet 4.6 Thinking",
        "description": "Computer powered by Claude 4.6 Sonnet with thinking",
        "mode": "asi",
        "provider": "ANTHROPIC",
    },
    "pplx_business_assistant": {
        "label": "Business Assistant",
        "description": "Business AI assistant",
        "mode": "asi",
        "provider": "ANTHROPIC",
    },
    "pplx_document_review": {
        "label": "Document Review",
        "description": "Comprehensive document analysis and fact-checking",
        "mode": "document_review",
        "provider": "PERPLEXITY",
    },
    "comet_browser_agent": {
        "label": "Best",
        "description": "Selects the best available browser agent model",
        "mode": "browser_agent",
        "provider": None,
    },
    "comet_browser_agent_sonnet": {
        "label": "Claude Sonnet 4.6",
        "description": "Browser agent powered by Claude 4.6 Sonnet",
        "mode": "browser_agent",
        "provider": "ANTHROPIC",
    },
    "comet_browser_agent_opus": {
        "label": "Claude Opus 4.7",
        "description": "Browser agent powered by Claude 4.7 Opus",
        "mode": "browser_agent",
        "provider": "ANTHROPIC",
    },
    "claudecode": {
        "label": "Claude Code",
        "description": "Anthropic's coding agent",
        "mode": "search",
        "provider": "ANTHROPIC",
    },
    "codex": {
        "label": "Codex",
        "description": "OpenAI's coding agent",
        "mode": "search",
        "provider": "OPENAI",
    },
    "gpt53codex": {
        "label": "GPT-5.3 Codex",
        "description": "OpenAI's coding model",
        "mode": "search",
        "provider": "OPENAI",
    },
    "nanobananapro": {
        "label": "Nano Banana Pro",
        "description": "Google's advanced image generation model",
        "mode": "search",
        "provider": "GOOGLE",
    },
    "nanobanana2": {
        "label": "Nano Banana 2",
        "description": "Google's image generation model",
        "mode": "search",
        "provider": "GOOGLE",
    },
    "sora2": {
        "label": "Sora 2",
        "description": "OpenAI's video generation model",
        "mode": "search",
        "provider": "OPENAI",
    },
    "sora2pro": {
        "label": "Sora 2 Pro",
        "description": "OpenAI's advanced video generation model",
        "mode": "search",
        "provider": "OPENAI",
    },
    "veo31": {
        "label": "Veo 3.1",
        "description": "Google's video generation model",
        "mode": "search",
        "provider": "GOOGLE",
    },
    "veo31fast": {
        "label": "Veo 3.1 Fast",
        "description": "Google's fast video generation model",
        "mode": "search",
        "provider": "GOOGLE",
    },
}

MODEL_SELECTOR_CONFIG: List[Dict[str, object]] = [
    {
        "label": "Sonar 2",
        "description": "Perplexity's latest in-house model.",
        "subheading": None,
        "has_new_tag": False,
        "subscription_tier": "pro",
        "non_reasoning_model": "experimental",
        "reasoning_model": None,
        "text_only_model": False,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "Claude Sonnet 4.6",
        "description": "Browser agent powered by Claude 4.6 Sonnet",
        "subheading": None,
        "has_new_tag": False,
        "subscription_tier": "pro",
        "non_reasoning_model": "comet_browser_agent_sonnet",
        "reasoning_model": None,
        "text_only_model": False,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "Claude Opus 4.7",
        "description": "Browser agent powered by Claude 4.7 Opus",
        "subheading": None,
        "has_new_tag": False,
        "subscription_tier": "max",
        "non_reasoning_model": "comet_browser_agent_opus",
        "reasoning_model": None,
        "text_only_model": False,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "GPT-5.4",
        "description": "OpenAI's versatile model",
        "subheading": None,
        "has_new_tag": False,
        "subscription_tier": "pro",
        "non_reasoning_model": "gpt54",
        "reasoning_model": "gpt54_thinking",
        "text_only_model": False,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "GPT-5.5",
        "description": "OpenAI's latest model",
        "subheading": None,
        "has_new_tag": True,
        "subscription_tier": "max",
        "non_reasoning_model": "gpt55",
        "reasoning_model": "gpt55_thinking",
        "text_only_model": False,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "Gemini 3.1 Pro",
        "description": "Google's latest model",
        "subheading": None,
        "has_new_tag": False,
        "subscription_tier": "pro",
        "non_reasoning_model": None,
        "reasoning_model": "gemini31pro_high",
        "text_only_model": False,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "Claude Sonnet 4.6",
        "description": "Anthropic's fast model",
        "subheading": None,
        "has_new_tag": False,
        "subscription_tier": "pro",
        "non_reasoning_model": "claude46sonnet",
        "reasoning_model": "claude46sonnetthinking",
        "text_only_model": False,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "Claude Opus 4.7",
        "description": "Anthropic's most advanced model",
        "subheading": None,
        "has_new_tag": True,
        "subscription_tier": "max",
        "non_reasoning_model": "claude47opus",
        "reasoning_model": "claude47opusthinking",
        "text_only_model": False,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "Kimi K2.6",
        "description": "Moonshot AI's latest model",
        "subheading": None,
        "has_new_tag": True,
        "subscription_tier": "pro",
        "non_reasoning_model": "kimik26instant",
        "reasoning_model": "kimik26thinking",
        "text_only_model": False,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "Nemotron 3 Super",
        "description": "NVIDIA's Nemotron 3 Super 120B model",
        "subheading": None,
        "has_new_tag": False,
        "subscription_tier": "pro",
        "non_reasoning_model": None,
        "reasoning_model": "nv_nemotron_3_super",
        "text_only_model": False,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "GPT-5.5",
        "description": "Computer powered by GPT-5.5",
        "subheading": "Newest model for complex tasks.",
        "has_new_tag": True,
        "subscription_tier": "pro",
        "non_reasoning_model": "pplx_asi_gpt_55",
        "reasoning_model": None,
        "text_only_model": False,
        "audience": None,
        "is_default": True,
    },
    {
        "label": "Claude Opus 4.7",
        "description": "Computer powered by Claude 4.7 Opus",
        "subheading": "Powerful model for complex tasks.",
        "has_new_tag": False,
        "subscription_tier": "pro",
        "non_reasoning_model": "pplx_asi_opus",
        "reasoning_model": None,
        "text_only_model": False,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "Claude Sonnet 4.6",
        "description": "Computer powered by Claude 4.6 Sonnet",
        "subheading": "Great for most everyday tasks. Uses fewer credits.",
        "has_new_tag": False,
        "subscription_tier": "pro",
        "non_reasoning_model": "pplx_asi_sonnet",
        "reasoning_model": None,
        "text_only_model": False,
        "audience": None,
        "is_default": False,
    },
]

DEFAULT_MODELS: Dict[str, str] = {
    "search": "pplx_pro",
    "research": "pplx_alpha",
    "agentic_research": "pplx_agentic_research",
    "study": "pplx_study",
    "document_review": "pplx_document_review",
    "browser_agent": "comet_browser_agent",
    "asi": "pplx_asi",
}

AGENTIC_RESEARCH_COMPARE_MODELS = [
    "gpt55_thinking",
    "claude47opusthinking",
    "gemini31pro_high",
]

MODEL_CONFIG: Dict[str, object] = {
    "config_schema": MODEL_CONFIG_SCHEMA,
    "models": MODEL_CATALOG,
    "config": MODEL_SELECTOR_CONFIG,
    "default_models": DEFAULT_MODELS,
    "agentic_research_compare_models": AGENTIC_RESEARCH_COMPARE_MODELS,
}

RAW_MODEL_IDS = set(MODEL_CATALOG)

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
    "gpt-5.5": "gpt55",
    "gpt-5.5-thinking": "gpt55_thinking",
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
    "claude-4.7-opus": "claude47opus",
    "claude-4.7-opus-thinking": "claude47opusthinking",
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
    "kimi-k2.6": "kimik26instant",
    "kimi-k2.6-thinking": "kimik26thinking",
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
    "computer-gpt-5.5": "pplx_asi_gpt_55",
    "computer-kimi": "pplx_asi_kimi",
    "computer-qwen": "pplx_asi_qwen",
    "computer-sonnet": "pplx_asi_sonnet",
    "computer-sonnet-thinking": "pplx_asi_sonnet_thinking",
    "business-assistant": "pplx_business_assistant",
    "browser-agent": "comet_browser_agent",
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

NON_AUTO_MODEL_MAPPINGS: Dict[str, str] = {model_id: model_id for model_id in RAW_MODEL_IDS}
NON_AUTO_MODEL_MAPPINGS.update(MODEL_ALIASES)

MODEL_MAPPINGS: Dict[str, Dict[str, str]] = {
    "auto": {None: "turbo", "turbo": "turbo"},
    "pro": {None: DEFAULT_MODELS["search"], **NON_AUTO_MODEL_MAPPINGS},
    "reasoning": {None: "pplx_reasoning", **NON_AUTO_MODEL_MAPPINGS},
    "deep research": {
        None: DEFAULT_MODELS["research"],
        DEFAULT_MODELS["research"]: DEFAULT_MODELS["research"],
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
LOG_FILE = None

# Rate Limiting
RATE_LIMIT_MIN_DELAY = 1.0  # seconds
RATE_LIMIT_MAX_DELAY = 3.0  # seconds
RATE_LIMIT_ENABLED = True

# Validation Patterns
EMAIL_SUBJECT_PATTERN = "Sign in to Perplexity"
SIGNIN_URL_PATTERN = r'"(https://www\.perplexity\.ai/api/auth/callback/email\?callbackUrl=.*?)"'
