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
export PERPLEXITY_REASON_MODEL="claude-5-sonnet-thinking"
```

`PERPLEXITY_MCP_MODE` defaults to `search`, which maps to Perplexity Pro web search for authenticated requests. Set it to `reasoning` or `deep research` only when that behavior is explicitly desired.

`PERPLEXITY_REASON_MODEL` controls the model used by the reasoning tool. It defaults to Claude Sonnet 5 Thinking (`claude50sonnetthinking`). Any supported alias from `perplexity.config.MODEL_MAPPINGS` can be used.

You can alternatively provide full cookie JSON:

```bash
export PERPLEXITY_COOKIES='{"next-auth.session-token":"...","next-auth.csrf-token":"..."}'
```

## Tools

| Tool | Mode | Auth Required | Description |
|------|------|---------------|-------------|
| `perplexity_ask` | `search` when authenticated, `auto` when anonymous | No | General question answering |
| `perplexity_reason` | `reasoning` | Yes | Reasoning with `PERPLEXITY_REASON_MODEL` |
| `perplexity_research` | `deep research` | Yes | Long-form Perplexity research. Use only when needed; prefer smaller focused questions over one huge research query. |
| `perplexity_search` | `pro` + web sources | Yes | Web search with Pro mode |

Without cookies, only `perplexity_ask` is registered.

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
        "PERPLEXITY_MCP_MODE": "search",
        "PERPLEXITY_REASON_MODEL": "claude-5-sonnet-thinking"
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
  --env PERPLEXITY_REASON_MODEL="claude-5-sonnet-thinking" \
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
  -e PERPLEXITY_REASON_MODEL="claude-5-sonnet-thinking" \
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
        "PERPLEXITY_MCP_MODE": "search",
        "PERPLEXITY_REASON_MODEL": "claude-5-sonnet-thinking"
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
        "PERPLEXITY_MCP_MODE": "search",
        "PERPLEXITY_REASON_MODEL": "claude-5-sonnet-thinking"
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
PERPLEXITY_REASON_MODEL = "claude-5-sonnet-thinking"
```

## HTTP Transport

For a persistent HTTP MCP endpoint:

```bash
MCP_TRANSPORT=http MCP_HOST=127.0.0.1 MCP_PORT=8000 perplexity-mcp
```

The endpoint will be available at `http://127.0.0.1:8000/mcp`.

## Supported Models

The full model catalog lives in `perplexity.config.MODEL_CONFIG`, mirroring Perplexity's `v2` model config. It includes:

- `models`: backend model IDs, labels, providers, and modes
- `search_config`: model picker metadata for search
- `computer_config`: model picker metadata for Computer mode
- `config`: flat model picker view kept for backwards compatibility
- `default_models`: defaults by Perplexity product mode
- `agentic_research_compare_models`: comparison defaults

Common aliases include:

```python
"claude-5-sonnet" -> "claude50sonnet"
"claude-5-sonnet-thinking" -> "claude50sonnetthinking"
"claude-5-opus" -> "claude50opus"
"claude-5-opus-thinking" -> "claude50opusthinking"
"gpt-5.6-sol" -> "gpt56_sol"
"gpt-5.6-sol-thinking" -> "gpt56_sol_thinking"
"gemini-3.5-flash-thinking" -> "gemini35flash_high"
"grok-4.5-thinking" -> "grok45medium"
"kimi-k3" -> "kimik3thinking"
```

## Development

Run tests:

```bash
python -m pytest
```

Format Python files:

```bash
python -m black perplexity tests
```

## Security

Do not commit real Perplexity cookies. Use environment variables or local MCP client config files outside the repository.

## License

MIT
