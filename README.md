# Perplexity MCP

Use Perplexity as an MCP server in coding agents with your Perplexity web auth cookies. No paid Perplexity API key is required.

This server exposes Perplexity search, reasoning, research, and web search tools over MCP for OpenCode, Claude Code, Codex CLI, GitHub Copilot CLI, VS Code, and other MCP clients.

## Features

- MCP stdio server via `perplexity-mcp`
- Optional HTTP transport for remote MCP clients
- Cookie-based Perplexity auth through `PERPLEXITY_SESSION_TOKEN` and `PERPLEXITY_CSRF_TOKEN`
- Optional `PERPLEXITY_COOKIES` JSON support for advanced cookie setups
- Authenticated tools for Pro, reasoning, and deep research modes
- No Perplexity API token pricing or API-key setup

## Requirements

- Python 3.10 or newer
- MCP Python SDK 2.x (installed automatically)

## Install

Install as a standalone CLI with `uv`. This keeps the server isolated from your project environments while still putting `perplexity-mcp` on `PATH`:

```bash
uv tool install "perplexity-mcp @ git+https://github.com/anxkhn/perplexity-mcp.git"
```

From a local checkout:

```bash
uv tool install --editable .
```

Verify the CLI:

```bash
perplexity-mcp --help
perplexity-mcp --version
```

## Environment

Copy `.env.example` and fill in your own Perplexity cookies:

```bash
export PERPLEXITY_SESSION_TOKEN="your-next-auth-session-token"
export PERPLEXITY_CSRF_TOKEN="your-next-auth-csrf-token"
export PERPLEXITY_MCP_MODE="search"
```

`PERPLEXITY_MCP_MODE` defaults to `search`, which maps to Perplexity Pro web search for authenticated requests. Set it to `reasoning` or `deep research` only when that behavior is explicitly desired.

Authenticated ask, search, and reasoning calls select an explicit model based on `user.subscription_tier` and `user.subscription_status` from `/api/auth/session`. Pro uses GPT-6.1 Sol Thinking, `gpt6_1_sol_thinking`. Max uses GPT-6 Astra Thinking, `gpt6_astra_thinking`. Active subscriptions and trials qualify. Models above the account's tier are rejected before sending a search.

Set `PERPLEXITY_REASON_MODEL="gpt6_1_sol_thinking"` to pin all three tools to that model. Otherwise defaults follow the current picker, preferring Astra on Max and the highest GPT version on Pro. There is no quality benchmark behind this preference. Authenticated `auto` mode is disabled. Unknown or free plans cannot use paid search models; the server reports an error instead of falling back to an automatic router.

You can alternatively provide full cookie JSON:

```bash
export PERPLEXITY_COOKIES='{"next-auth.session-token":"...","next-auth.csrf-token":"..."}'
```

For newer multi-account sessions, include `__Host-pplx-last-active-account` and the matching `__Secure-pplx.session.<account-id>` cookie in `PERPLEXITY_COOKIES`. The server sends `x-pplx-account` for that account and detects its plan.

## Tools

| Tool | Mode | Auth Required | Description |
|------|------|---------------|-------------|
| `perplexity_ask` | `search` when authenticated, `auto` when anonymous | No | General question answering |
| `perplexity_reason` | `reasoning` | Yes | Reasoning with `PERPLEXITY_REASON_MODEL` |
| `perplexity_research` | `deep research` | Yes | Long-form Perplexity research. Use only when needed; prefer smaller focused questions over one huge research query. |
| `perplexity_search` | `pro` + web sources | Yes | Web search with Pro mode |
| `perplexity_models` | Model discovery | Yes | List model IDs, picker choices, subscription tiers, and refresh status |

Without cookies, only `perplexity_ask` is registered.

`perplexity_ask`, `perplexity_search`, and `perplexity_reason` accept an optional `model` argument. `perplexity_ask` supports it when configured for search/Pro or reasoning mode. For example, call `perplexity_reason` with `{"query": "Compare these approaches", "model": "claude55sonnetthinking"}`. Without an override, all three tools use the explicit account-aware model.

## OpenCode

Add this local MCP server to `~/.config/opencode/opencode.json`:

```json
{
  "mcp": {
    "perplexity": {
      "type": "local",
      "command": ["perplexity-mcp"],
      "enabled": true,
      "environment": {
        "PERPLEXITY_SESSION_TOKEN": "your-next-auth-session-token",
        "PERPLEXITY_CSRF_TOKEN": "your-next-auth-csrf-token",
        "PERPLEXITY_MCP_MODE": "search"
      }
    }
  }
}
```

Verify:

```bash
opencode mcp list
```

## Codex CLI

```bash
codex mcp add perplexity \
  --env PERPLEXITY_SESSION_TOKEN="$PERPLEXITY_SESSION_TOKEN" \
  --env PERPLEXITY_CSRF_TOKEN="$PERPLEXITY_CSRF_TOKEN" \
  --env PERPLEXITY_MCP_MODE="search" \
  -- perplexity-mcp
```

Verify:

```bash
codex mcp list
```

## Claude Code

```bash
claude mcp add -s user perplexity \
  -e PERPLEXITY_SESSION_TOKEN="$PERPLEXITY_SESSION_TOKEN" \
  -e PERPLEXITY_CSRF_TOKEN="$PERPLEXITY_CSRF_TOKEN" \
  -e PERPLEXITY_MCP_MODE="search" \
  -- perplexity-mcp
```

Verify:

```bash
claude mcp list
```

## GitHub Copilot CLI

Add the server to `~/.copilot/mcp-config.json`:

```json
{
  "mcpServers": {
    "perplexity": {
      "type": "local",
      "command": "perplexity-mcp",
      "args": [],
      "tools": ["*"],
      "env": {
        "PERPLEXITY_SESSION_TOKEN": "your-next-auth-session-token",
        "PERPLEXITY_CSRF_TOKEN": "your-next-auth-csrf-token",
        "PERPLEXITY_MCP_MODE": "search"
      }
    }
  }
}
```

## VS Code

Add the server to your user `mcp.json` (Command Palette: `MCP: Open User Configuration`):

```json
{
  "servers": {
    "perplexity": {
      "type": "stdio",
      "command": "perplexity-mcp",
      "env": {
        "PERPLEXITY_SESSION_TOKEN": "your-next-auth-session-token",
        "PERPLEXITY_CSRF_TOKEN": "your-next-auth-csrf-token",
        "PERPLEXITY_MCP_MODE": "search"
      }
    }
  }
}
```

## Grok CLI

Add the server to `~/.grok/config.toml`:

```toml
[mcp_servers.perplexity]
command = "perplexity-mcp"
args = []
enabled = true
[mcp_servers.perplexity.env]
PERPLEXITY_SESSION_TOKEN = "your-next-auth-session-token"
PERPLEXITY_CSRF_TOKEN = "your-next-auth-csrf-token"
PERPLEXITY_MCP_MODE = "search"
```

## HTTP Transport

For a persistent HTTP MCP endpoint:

```bash
MCP_TRANSPORT=http MCP_HOST=127.0.0.1 MCP_PORT=8000 perplexity-mcp
```

The endpoint will be available at `http://127.0.0.1:8000/mcp`.

## Supported Models

The authenticated MCP server fetches Perplexity's current model config from `/rest/models/config/v2?version=2.18&source=default` on first startup. It reuses a fresh cache on subsequent startups and checks again on the first tool call after 24 hours. New backend IDs become usable immediately, without a package update.

Call `perplexity_models` with `{"refresh": true}` to check immediately. The result includes:

- `models`: the current catalog, including backend IDs and labels
- `search_config`: search/reasoning picker choices and subscription tiers
- `computer_config`: Computer picker metadata, which requires a separate workflow
- `source`, `fetched_at`, `stale`, and `refresh_error`: discovery and cache status
- `changes`: IDs added, removed, or updated during the last successful refresh
- `subscription_tier`: detected account plan, or `unknown`
- `available_search_models`: current search model IDs allowed by the plan
- `default_reasoning_model`, `default_reasoning_model_available`: effective selection and access status

The server logs catalog changes to stderr. If a refresh fails, it keeps the last cached config, or the bundled catalog if there is no valid cache. Failed automatic checks retry after 24 hours; unknown account plans retry on the next call after one minute. A forced refresh can retry sooner. Cache files live in `$XDG_CACHE_HOME/perplexity-mcp`, or `~/.cache/perplexity-mcp`, keyed by a hash of the account/session cookies. The cache stores model configuration, not cookies or account plan details.

The catalog keeps current picker choices and named research workflows. Older and hidden entries from the raw payload are discarded on every refresh. Search mappings include only account-eligible search models, excluding Computer and browser agents. If an explicit override disappears or requires a higher tier, the server reports an error. Non-null organization model policies require separate handling and disable model selection rather than bypassing a policy.

Current search choices:

| Lineup | Standard ID | Thinking ID | Plan |
|--------|-------------|-------------|------|
| GPT-6.1 Sol | `gpt6_1_sol` | `gpt6_1_sol_thinking` | Pro |
| GPT-6 Astra | `gpt6_astra` | `gpt6_astra_thinking` | Max |
| Gemini 3.8 Flash | `gemini38flash` | `gemini38flashthinking` | Pro |
| Claude Sonnet 5.5 | `claude55sonnet` | `claude55sonnetthinking` | Pro |
| Claude Opus 5.5 | `claude55opus` | `claude55opusthinking` | Max |
| Claude Fable 5.1 | `claudefable51` | `claudefable51thinking` | Max |
| Kimi K3 | None | `kimik3thinking` | Pro |
| GLM 5.3 | None | `glm_5_3_thinking` | Pro |
| Grok 4.7 | `grok47` | `grok47thinking` | Pro |
| Nemotron 3 Ultra | None | `nv_nemotron_3_ultra` | Pro |

The bundled catalog also keeps both browser picker choices and all nine Computer choices, including fast variants and DeepSeek V4 Pro. These are metadata, not executable search choices. Deep research uses the explicit `pplx_alpha` workflow; anonymous ask retains Perplexity's anonymous route.

`perplexity.config.MODEL_CONFIG` remains the bundled fallback catalog. It includes:

- `models`: backend model IDs, labels, and modes
- `search_config`: model picker metadata for search
- `computer_config`: model picker metadata for Computer mode
- `config`: flat model picker view kept for backwards compatibility
- `default_models`: defaults by Perplexity product mode
- `agentic_research_compare_models`: comparison defaults

Common aliases include:

```python
"claude-5.5-sonnet-thinking" -> "claude55sonnetthinking"
"claude-5.5-opus-thinking" -> "claude55opusthinking"
"claude-fable-5.1-thinking" -> "claudefable51thinking"
"gpt-6.1-sol" -> "gpt6_1_sol"
"gpt-6.1-sol-thinking" -> "gpt6_1_sol_thinking"
"gpt-6-astra-thinking" -> "gpt6_astra_thinking"
"gemini-3.8-flash-thinking" -> "gemini38flashthinking"
"grok-4.7-thinking" -> "grok47thinking"
"kimi-k3" -> "kimik3thinking"
```

## Development

Run tests:

```bash
uv run --extra dev python -m pytest
```

Format Python files:

```bash
uv run --extra dev python -m black perplexity tests
```

## Security

Do not commit real Perplexity cookies. Use environment variables or local MCP client config files outside the repository.

## License

MIT
