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
MODEL_CONFIG_SCHEMA = "v2"

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
    "glm_5_2": {
        "label": "GLM-5.2",
        "description": "Z.ai's advanced model",
        "mode": "search",
        "provider": "ZAI",
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
        "description": "OpenAI's latest model with reasoning",
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
        "description": "OpenAI's latest model with reasoning",
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
        "description": "OpenAI's latest model with reasoning",
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
        "description": "OpenAI's versatile model with reasoning",
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
        "description": "OpenAI's latest model with reasoning",
        "mode": "search",
        "provider": "OPENAI",
    },
    "gpt56_sol": {
        "label": "GPT-5.6 Sol",
        "description": "OpenAI's most powerful model",
        "mode": "search",
        "provider": "OPENAI",
    },
    "gpt56_sol_thinking": {
        "label": "GPT-5.6 Sol Thinking",
        "description": "OpenAI's most powerful model with reasoning",
        "mode": "search",
        "provider": "OPENAI",
    },
    "gpt56_terra": {
        "label": "GPT-5.6 Terra",
        "description": "OpenAI's versatile model",
        "mode": "search",
        "provider": "OPENAI",
    },
    "gpt56_terra_thinking": {
        "label": "GPT-5.6 Terra Thinking",
        "description": "OpenAI's versatile model with reasoning",
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
    "gemini35flash": {
        "label": "Gemini 3.5 Flash",
        "description": "Google's fast model",
        "mode": "search",
        "provider": "GOOGLE",
    },
    "gemini35flash_medium": {
        "label": "Gemini 3.5 Flash Medium Thinking",
        "description": "Google's fast model with medium thinking",
        "mode": "search",
        "provider": "GOOGLE",
    },
    "gemini35flash_high": {
        "label": "Gemini 3.5 Flash Thinking",
        "description": "Google's fast model with thinking",
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
        "description": "Anthropic's most advanced model with reasoning",
        "mode": "search",
        "provider": "ANTHROPIC",
    },
    "claude48opus": {
        "label": "Claude Opus 4.8",
        "description": "Anthropic's most advanced model",
        "mode": "search",
        "provider": "ANTHROPIC",
    },
    "claude48opusthinking": {
        "label": "Claude Opus 4.8 Thinking",
        "description": "Anthropic's most advanced model with reasoning",
        "mode": "search",
        "provider": "ANTHROPIC",
    },
    "claude50opus": {
        "label": "Claude Opus 5",
        "description": "Anthropic's most advanced model",
        "mode": "search",
        "provider": "ANTHROPIC",
    },
    "claude50opusthinking": {
        "label": "Claude Opus 5 Thinking",
        "description": "Anthropic's most advanced model with reasoning",
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
    "claude50sonnet": {
        "label": "Claude Sonnet 5",
        "description": "Anthropic's fast model",
        "mode": "search",
        "provider": "ANTHROPIC",
    },
    "claude50sonnetthinking": {
        "label": "Claude Sonnet 5 Thinking",
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
    "kimik3thinking": {
        "label": "Kimi K3",
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
    "grok45low": {
        "label": "Grok 4.5",
        "description": "xAI's most advanced model",
        "mode": "search",
        "provider": "XAI",
    },
    "grok45medium": {
        "label": "Grok 4.5 Thinking",
        "description": "xAI's most advanced model",
        "mode": "search",
        "provider": "XAI",
    },
    "nv_nemotron_3_super": {
        "label": "Nemotron 3 Super",
        "description": "NVIDIA's Nemotron 3 Super 120B model",
        "mode": "search",
        "provider": "NVIDIA",
    },
    "nv_nemotron_3_ultra": {
        "label": "Nemotron 3 Ultra",
        "description": "NVIDIA's Nemotron 3 Ultra 550B model",
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
        "description": "Delegate research tasks to specialised sub-agents",
        "mode": "agentic_research",
        "provider": "PERPLEXITY",
    },
    "pplx_asi": {
        "label": "Computer",
        "description": "Computer (default model)",
        "mode": "asi",
        "provider": "ANTHROPIC",
    },
    "pplx_asi_openrouter": {
        "label": "OpenRouter",
        "description": "Computer powered by OpenRouter",
        "mode": "asi",
        "provider": "PERPLEXITY",
    },
    "pplx_asi_glm": {
        "label": "Preview (GLM 5.2-based)",
        "description": "Computer powered by GLM 5.2",
        "mode": "asi",
        "provider": "PERPLEXITY",
    },
    "pplx_asi_kimi_k3": {
        "label": "Kimi K3",
        "description": "Computer powered by Kimi K3",
        "mode": "asi",
        "provider": "MOONSHOT_AI",
    },
    "pplx_asi_opus": {
        "label": "Claude Opus 5",
        "description": "Computer powered by Claude Opus 5",
        "mode": "asi",
        "provider": "ANTHROPIC",
    },
    "pplx_asi_opus_fast": {
        "label": "Claude Opus 5 Fast",
        "description": "Computer powered by Claude Opus 5 in fast mode",
        "mode": "asi",
        "provider": "ANTHROPIC",
    },
    "pplx_asi_fable_5": {
        "label": "Claude Fable 5",
        "description": "Computer powered by Claude Fable 5",
        "mode": "asi",
        "provider": "ANTHROPIC",
    },
    "pplx_asi_opus_thinking": {
        "label": "Claude Opus 4.8 Thinking",
        "description": "Computer powered by Claude Opus 4.8 with thinking",
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
    "pplx_asi_gpt_56_sol": {
        "label": "GPT-5.6 Sol",
        "description": "Computer powered by GPT-5.6 Sol",
        "mode": "asi",
        "provider": "OPENAI",
    },
    "pplx_asi_grok_45": {
        "label": "Grok 4.5",
        "description": "Computer powered by Grok 4.5",
        "mode": "asi",
        "provider": "XAI",
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
        "label": "Claude Sonnet 5",
        "description": "Computer powered by Claude Sonnet 5",
        "mode": "asi",
        "provider": "ANTHROPIC",
    },
    "pplx_asi_sonnet_thinking": {
        "label": "Claude Sonnet 5 Thinking",
        "description": "Computer powered by Claude Sonnet 5 with thinking",
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
        "label": "Claude Sonnet 5",
        "description": "Browser agent powered by Claude Sonnet 5",
        "mode": "browser_agent",
        "provider": "ANTHROPIC",
    },
    "comet_browser_agent_opus": {
        "label": "Claude Opus 4.8",
        "description": "Browser agent powered by Claude Opus 4.8",
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

SEARCH_MODEL_CONFIG: List[Dict[str, object]] = [
    {
        "label": "Sonar 2",
        "description": "Perplexity's latest in-house model.",
        "has_new_tag": False,
        "subscription_tier": "pro",
        "non_reasoning_model": "experimental",
        "reasoning_model": None,
        "text_only_model": False,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "Claude Sonnet 5",
        "description": "Browser agent powered by Claude Sonnet 5",
        "has_new_tag": False,
        "subscription_tier": "pro",
        "non_reasoning_model": "comet_browser_agent_sonnet",
        "reasoning_model": None,
        "text_only_model": False,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "Claude Opus 4.8",
        "description": "Browser agent powered by Claude Opus 4.8",
        "has_new_tag": False,
        "subscription_tier": "max",
        "non_reasoning_model": "comet_browser_agent_opus",
        "reasoning_model": None,
        "text_only_model": False,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "GPT-5.6 Terra",
        "description": "OpenAI's versatile model",
        "has_new_tag": False,
        "subscription_tier": "pro",
        "non_reasoning_model": "gpt56_terra",
        "reasoning_model": "gpt56_terra_thinking",
        "text_only_model": False,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "GPT-5.6 Sol",
        "description": "OpenAI's most powerful model",
        "has_new_tag": False,
        "subscription_tier": "max",
        "non_reasoning_model": "gpt56_sol",
        "reasoning_model": "gpt56_sol_thinking",
        "text_only_model": False,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "Gemini 3.1 Pro",
        "description": "Google's latest model",
        "has_new_tag": False,
        "subscription_tier": "pro",
        "non_reasoning_model": None,
        "reasoning_model": "gemini31pro_high",
        "text_only_model": False,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "Claude Sonnet 5",
        "description": "Anthropic's fast model",
        "has_new_tag": False,
        "subscription_tier": "pro",
        "non_reasoning_model": "claude50sonnet",
        "reasoning_model": "claude50sonnetthinking",
        "text_only_model": False,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "Claude Opus 5",
        "description": "Anthropic's most advanced model",
        "has_new_tag": False,
        "subscription_tier": "max",
        "non_reasoning_model": "claude50opus",
        "reasoning_model": "claude50opusthinking",
        "text_only_model": False,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "Kimi K3",
        "description": "Moonshot AI's latest model. Hosted in the US.",
        "has_new_tag": True,
        "subscription_tier": "pro",
        "non_reasoning_model": None,
        "reasoning_model": "kimik3thinking",
        "text_only_model": False,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "GLM 5.2",
        "description": "Z.ai's most advanced model. Hosted in the US.",
        "has_new_tag": False,
        "subscription_tier": "pro",
        "non_reasoning_model": None,
        "reasoning_model": "glm_5_2",
        "text_only_model": False,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "Grok 4.5",
        "description": "xAI's most advanced model",
        "has_new_tag": False,
        "subscription_tier": "pro",
        "non_reasoning_model": "grok45low",
        "reasoning_model": "grok45medium",
        "text_only_model": False,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "Nemotron 3 Ultra",
        "description": "NVIDIA's Nemotron 3 Ultra 550B model",
        "has_new_tag": False,
        "subscription_tier": "pro",
        "non_reasoning_model": None,
        "reasoning_model": "nv_nemotron_3_ultra",
        "text_only_model": False,
        "audience": None,
        "is_default": False,
    },
]

COMPUTER_MODEL_CONFIG: List[Dict[str, object]] = [
    {
        "label": "GPT-5.6 Sol",
        "description": "Computer powered by GPT-5.6 Sol",
        "subheading": "OpenAI's newest model for complex tasks.",
        "has_new_tag": False,
        "subscription_tier": "pro",
        "model": "pplx_asi_gpt_56_sol",
        "fast_model": None,
        "support_model_switching": False,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "Claude Fable 5",
        "description": "Computer powered by Claude Fable 5",
        "subheading": "Anthropic's most powerful model. Uses additional credits.",
        "has_new_tag": False,
        "subscription_tier": "pro",
        "model": "pplx_asi_fable_5",
        "fast_model": None,
        "support_model_switching": True,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "Claude Opus 5",
        "description": "Computer powered by Claude Opus 5",
        "subheading": "Powerful model for complex tasks.",
        "has_new_tag": False,
        "subscription_tier": "pro",
        "model": "pplx_asi_opus",
        "fast_model": "pplx_asi_opus_fast",
        "support_model_switching": True,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "Claude Sonnet 5",
        "description": "Computer powered by Claude Sonnet 5",
        "subheading": "Great for most everyday tasks. Uses fewer credits.",
        "has_new_tag": False,
        "subscription_tier": "pro",
        "model": "pplx_asi_sonnet",
        "fast_model": None,
        "support_model_switching": True,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "Preview (GLM 5.2-based)",
        "description": "Computer powered by GLM 5.2",
        "subheading": "Great for most tasks. Uses the fewest credits. US Hosted.",
        "has_new_tag": False,
        "subscription_tier": "pro",
        "model": "pplx_asi_glm",
        "fast_model": None,
        "support_model_switching": True,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "Kimi K3",
        "description": "Computer powered by Kimi K3",
        "subheading": "Moonshot AI's latest model. US hosted.",
        "has_new_tag": False,
        "subscription_tier": "pro",
        "model": "pplx_asi_kimi_k3",
        "fast_model": None,
        "support_model_switching": True,
        "audience": None,
        "is_default": False,
    },
    {
        "label": "Grok 4.5",
        "description": "Computer powered by Grok 4.5",
        "subheading": "xAI's newest model for complex tasks.",
        "has_new_tag": False,
        "subscription_tier": "pro",
        "model": "pplx_asi_grok_45",
        "fast_model": None,
        "support_model_switching": True,
        "audience": None,
        "is_default": False,
    },
]

# Flat model-picker view kept for backwards compatibility with the v1 ``config`` list.
MODEL_SELECTOR_CONFIG: List[Dict[str, object]] = [
    {"subheading": None, **entry} for entry in SEARCH_MODEL_CONFIG
] + [
    {
        "label": entry["label"],
        "description": entry["description"],
        "subheading": entry["subheading"],
        "has_new_tag": entry["has_new_tag"],
        "subscription_tier": entry["subscription_tier"],
        "non_reasoning_model": entry["model"],
        "reasoning_model": None,
        "text_only_model": False,
        "audience": entry["audience"],
        "is_default": entry["is_default"],
    }
    for entry in COMPUTER_MODEL_CONFIG
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
    "gpt56_sol_thinking",
    "claude50opusthinking",
    "gemini31pro_high",
]

# Backend model used by the MCP reasoning tool unless overridden by the environment.
DEFAULT_REASONING_MODEL = "claude50sonnetthinking"

MODEL_CONFIG: Dict[str, object] = {
    "config_schema": MODEL_CONFIG_SCHEMA,
    "models": MODEL_CATALOG,
    "config": MODEL_SELECTOR_CONFIG,
    "search_config": SEARCH_MODEL_CONFIG,
    "computer_config": COMPUTER_MODEL_CONFIG,
    "default_models": DEFAULT_MODELS,
    "agentic_research_compare_models": AGENTIC_RESEARCH_COMPARE_MODELS,
}

RAW_MODEL_IDS = set(MODEL_CATALOG)

MODEL_ALIASES = {
    "turbo": "turbo",
    "sonar": "experimental",
    "glm-5.2": "glm_5_2",
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
    "gpt-5.6-terra": "gpt56_terra",
    "gpt-5.6-terra-thinking": "gpt56_terra_thinking",
    "gpt-5.6-sol": "gpt56_sol",
    "gpt-5.6-sol-thinking": "gpt56_sol_thinking",
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
    "claude-4.8-opus": "claude48opus",
    "claude-4.8-opus-thinking": "claude48opusthinking",
    "claude-5-opus": "claude50opus",
    "claude-5-opus-thinking": "claude50opusthinking",
    "claude-4.5-sonnet": "claude45sonnet",
    "claude-4.5-sonnet-thinking": "claude45sonnetthinking",
    "claude-4.6-sonnet": "claude46sonnet",
    "claude-4.6-sonnet-thinking": "claude46sonnetthinking",
    "claude-5-sonnet": "claude50sonnet",
    "claude-5-sonnet-thinking": "claude50sonnetthinking",
    "claude-4.5-haiku": "claude45haiku",
    "claude-4.5-haiku-thinking": "claude45haikuthinking",
    "gemini-2.5-pro": "gemini25pro",
    "gemini-3.0-pro": "gemini30pro",
    "gemini-3.0-flash": "gemini30flash",
    "gemini-3.0-flash-thinking": "gemini30flash_high",
    "gemini-3.1-pro": "gemini31pro_low",
    "gemini-3.1-pro-thinking": "gemini31pro_high",
    "gemini-3.5-flash": "gemini35flash",
    "gemini-3.5-flash-medium-thinking": "gemini35flash_medium",
    "gemini-3.5-flash-thinking": "gemini35flash_high",
    "grok-3-beta": "grok",
    "grok-4": "grok4nonthinking",
    "grok-4-thinking": "grok4",
    "grok-4-reasoning": "grok4",
    "grok-4.1": "grok41nonreasoning",
    "grok-4.1-thinking": "grok41reasoning",
    "grok-4.1-reasoning": "grok41reasoning",
    "grok-4.5": "grok45low",
    "grok-4.5-thinking": "grok45medium",
    "grok-4.5-reasoning": "grok45medium",
    "kimi-k2-thinking": "kimik2thinking",
    "kimi-k2.5-thinking": "kimik25thinking",
    "kimi-k2.6": "kimik26instant",
    "kimi-k2.6-thinking": "kimik26thinking",
    "kimi-k3": "kimik3thinking",
    "nemotron-3-super": "nv_nemotron_3_super",
    "nemotron-3-ultra": "nv_nemotron_3_ultra",
    "o4-mini": "o4mini",
    "o3-pro": "o3pro",
    "deep-research": "pplx_alpha",
    "study": "pplx_study",
    "studio": "pplx_beta",
    "agentic-research": "pplx_agentic_research",
    "document-review": "pplx_document_review",
    "computer": "pplx_asi",
    "computer-openrouter": "pplx_asi_openrouter",
    "computer-glm": "pplx_asi_glm",
    "computer-fable-5": "pplx_asi_fable_5",
    "computer-opus": "pplx_asi_opus",
    "computer-opus-fast": "pplx_asi_opus_fast",
    "computer-opus-thinking": "pplx_asi_opus_thinking",
    "computer-gpt-5.4": "pplx_asi_gpt54",
    "computer-gpt-5.5": "pplx_asi_gpt_55",
    "computer-gpt-5.6-sol": "pplx_asi_gpt_56_sol",
    "computer-grok-4.5": "pplx_asi_grok_45",
    "computer-kimi": "pplx_asi_kimi",
    "computer-kimi-k3": "pplx_asi_kimi_k3",
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
