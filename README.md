# Perplexity MCP

Use Perplexity as an MCP server in coding agents with your Perplexity web auth cookies. No paid Perplexity API key is required.

This server exposes Perplexity search, reasoning, research, and web search tools over MCP for OpenCode, Codex CLI, Claude Code, and other MCP clients.

## Features

- MCP stdio server via `perplexity-mcp`
- Optional HTTP transport for remote MCP clients
- Cookie-based Perplexity auth through `PERPLEXITY_SESSION_TOKEN` and `PERPLEXITY_CSRF_TOKEN`
- Optional `PERPLEXITY_COOKIES` JSON support for advanced cookie setups
- Authenticated tools for Pro, reasoning, and deep research modes
- No Perplexity API token pricing or API-key setup

## Install

From this repository:

```bash
uv pip install . --system
```

From GitHub:

```bash
uv pip install "perplexity-mcp @ git+https://github.com/anxkhn/perplexity-mcp.git" --system
```

Verify the CLI:

```bash
perplexity-mcp --help
```

## Environment

Copy `.env.example` and fill in your own Perplexity cookies:

```bash
export PERPLEXITY_SESSION_TOKEN="your-next-auth-session-token"
export PERPLEXITY_CSRF_TOKEN="your-next-auth-csrf-token"
export PERPLEXITY_REASON_MODEL="claude-4.6-sonnet-thinking"
```

`PERPLEXITY_REASON_MODEL` controls the model used by the reasoning tool and authenticated default ask path. Any supported alias from `perplexity.config.MODEL_MAPPINGS` can be used.

You can alternatively provide full cookie JSON:

```bash
export PERPLEXITY_COOKIES='{"next-auth.session-token":"...","next-auth.csrf-token":"..."}'
```

## Tools

| Tool | Mode | Auth Required | Description |
|------|------|---------------|-------------|
| `perplexity_ask` | `auto` or configured default | No | General question answering |
| `perplexity_reason` | `reasoning` | Yes | Reasoning with `PERPLEXITY_REASON_MODEL` |
| `perplexity_research` | `deep research` | Yes | Long-form Perplexity research |
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
        "PERPLEXITY_REASON_MODEL": "claude-4.6-sonnet-thinking"
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
  --env PERPLEXITY_REASON_MODEL="claude-4.6-sonnet-thinking" \
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
  -e PERPLEXITY_REASON_MODEL="claude-4.6-sonnet-thinking" \
  -- perplexity-mcp
```

Verify:

```bash
claude mcp list
```

## HTTP Transport

For a persistent HTTP MCP endpoint:

```bash
MCP_TRANSPORT=http MCP_HOST=127.0.0.1 MCP_PORT=8000 perplexity-mcp
```

The endpoint will be available at `http://127.0.0.1:8000/mcp`.

## Supported Models

The full model catalog lives in `perplexity.config.MODEL_CONFIG`. It includes:

- `models`: backend model IDs, labels, providers, and modes
- `config`: model picker metadata from Perplexity's `v1` config
- `default_models`: defaults by Perplexity product mode
- `agentic_research_compare_models`: comparison defaults

Common aliases include:

```python
"gpt-5.5" -> "gpt55"
"gpt-5.5-thinking" -> "gpt55_thinking"
"claude-4.7-opus" -> "claude47opus"
"claude-4.7-opus-thinking" -> "claude47opusthinking"
"claude-4.6-sonnet-thinking" -> "claude46sonnetthinking"
"kimi-k2.6" -> "kimik26instant"
"kimi-k2.6-thinking" -> "kimik26thinking"
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
