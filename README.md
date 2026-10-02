# Perplexity MCP

Bring Perplexity web search, reasoning, and deep research into your coding agent using your existing Perplexity account. No Perplexity API key is required.

The server reads your subscription, chooses an explicit model your plan supports, and keeps its model list current. It works over MCP with OpenCode, Claude Code, Codex CLI, GitHub Copilot CLI, VS Code, and other compatible clients.

[Install](#install) · [Connect your account](#connect-your-account) · [Client setup](#client-setup) · [Model selection](#model-selection) · [Automatic refresh](#automatic-refresh)

## What you get

- Five MCP tools for questions, web search, reasoning, deep research, and model discovery.
- Account-aware model selection. The current defaults are GPT-6.1 Sol Thinking on Pro and GPT-6 Astra Thinking on Max.
- An explicit model on authenticated ask, search, and reasoning requests. The server does not send these through Perplexity's automatic model routers.
- A live model catalog with daily refresh, a local cache, and a bundled fallback.
- Per-request model overrides, including Claude, Gemini, Kimi, GLM, Grok, and Nemotron choices allowed by your plan.
- Stdio for local agents and optional streamable HTTP for remote clients.

This is an unofficial client for Perplexity's website endpoints. Your subscription limits still apply, and Perplexity can change those endpoints. The MCP answer tools return plain text; they do not expose structured citations, attachments, or follow-up conversations.

## Install

You need [uv](https://docs.astral.sh/uv/getting-started/installation/) and Python 3.10 or newer. uv can install the Python version for you.

Install from GitHub:

```bash
uv tool install --python 3.12 "git+https://github.com/anxkhn/perplexity-mcp.git"
perplexity-mcp --version
```

This installs the repository's default branch. These instructions do not assume a PyPI release.

If your shell cannot find `perplexity-mcp`, run `uv tool update-shell` and reopen the terminal.

<details>
<summary>Run without installing a persistent CLI, or install a local checkout</summary>

Run from GitHub in uv's cached tool environment:

```bash
uvx --python 3.12 --from "git+https://github.com/anxkhn/perplexity-mcp.git" perplexity-mcp --help
```

From a local checkout:

```bash
uv tool install --python 3.12 --editable .
```

You can also build an installable wheel:

```bash
uv build --wheel
uv tool install --python 3.12 ./dist/perplexity_mcp-0.3.1-py3-none-any.whl
```

</details>

### Update the installed server

```bash
uv tool upgrade perplexity-mcp
```

Restart the MCP server after updating its code. Model catalog updates happen inside the running server and do not require reinstalling the package.

## Connect your account

Sign in to Perplexity in your browser. Open Developer Tools, select Network, and inspect a request to `www.perplexity.ai`. Use the cookies from the account you want the server to use.

For sessions with named account cookies:

```bash
export PERPLEXITY_COOKIES='{
  "__Host-pplx-last-active-account": "your-account-id",
  "__Secure-pplx.session.your-account-id": "your-session-cookie"
}'
```

The account ID must match the suffix of the session cookie. The server sends it as `x-pplx-account`, so subscription detection and searches use the same account. You can include other cookies from the request if your session needs them.

<details>
<summary>Older next-auth sessions</summary>

```bash
export PERPLEXITY_SESSION_TOKEN="your-next-auth-session-token"
export PERPLEXITY_CSRF_TOKEN="your-next-auth-csrf-token"
```

The server constructs the secure and non-secure next-auth cookie names. If you set `PERPLEXITY_COOKIES`, its JSON takes precedence over these variables.

</details>

Store credentials in your MCP client's local configuration or environment. Keep them out of Git. `.env.example` lists the settings, but the server does not load `.env` files itself.

Without cookies, the server registers only `perplexity_ask` and uses Perplexity's anonymous route. Paid model selection requires a recognized Pro or Max subscription.

## Client setup

Configure the installed `perplexity-mcp` command and pass your cookies in the server's environment. GUI clients may need the absolute executable path if they do not inherit your shell's `PATH`.

### OpenCode

Add this entry to the `mcp` object in your OpenCode configuration:

```json
{
  "mcp": {
    "perplexity": {
      "type": "local",
      "command": ["perplexity-mcp"],
      "enabled": true,
      "environment": {
        "PERPLEXITY_COOKIES": "{\"__Host-pplx-last-active-account\":\"your-account-id\",\"__Secure-pplx.session.your-account-id\":\"your-session-cookie\"}"
      }
    }
  }
}
```

### Claude Code and Codex CLI

With `PERPLEXITY_COOKIES` exported in your shell:

```bash
claude mcp add -s user perplexity \
  -e PERPLEXITY_COOKIES="$PERPLEXITY_COOKIES" \
  -- perplexity-mcp
```

```bash
codex mcp add perplexity \
  --env PERPLEXITY_COOKIES="$PERPLEXITY_COOKIES" \
  -- perplexity-mcp
```

<details>
<summary>GitHub Copilot CLI</summary>

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
        "PERPLEXITY_COOKIES": "{\"__Host-pplx-last-active-account\":\"your-account-id\",\"__Secure-pplx.session.your-account-id\":\"your-session-cookie\"}"
      }
    }
  }
}
```

</details>

<details>
<summary>VS Code</summary>

Run `MCP: Open User Configuration` in the Command Palette and add:

```json
{
  "servers": {
    "perplexity": {
      "type": "stdio",
      "command": "perplexity-mcp",
      "env": {
        "PERPLEXITY_COOKIES": "{\"__Host-pplx-last-active-account\":\"your-account-id\",\"__Secure-pplx.session.your-account-id\":\"your-session-cookie\"}"
      }
    }
  }
}
```

</details>

<details>
<summary>Grok CLI</summary>

Add the server to `~/.grok/config.toml`:

```toml
[mcp_servers.perplexity]
command = "perplexity-mcp"
args = []
enabled = true

[mcp_servers.perplexity.env]
PERPLEXITY_COOKIES = '{"__Host-pplx-last-active-account":"your-account-id","__Secure-pplx.session.your-account-id":"your-session-cookie"}'
```

</details>

## Tools

| Tool | What it does | Arguments |
|------|--------------|-----------|
| `perplexity_ask` | General questions. Authenticated calls use Pro web search by default. | `query`, optional `model` |
| `perplexity_search` | Web search using an explicit model allowed by your plan. | `query`, optional `model` |
| `perplexity_reason` | Reasoning using the selected Thinking model. | `query`, optional `model` |
| `perplexity_research` | Perplexity deep research using its research workflow. | `query` |
| `perplexity_models` | Current picker choices, detected plan, selected default, and refresh status. | Optional `refresh`, defaults to `false` |

For example, pass these arguments to `perplexity_reason`:

```json
{
  "query": "Compare the failure modes of these two designs",
  "model": "claude55sonnetthinking"
}
```

Deep research can take longer than a normal query. Use it when the question needs a research report. Its workflow has its own model selection and does not accept the `model` override used by the other tools.

## Model selection

The server requests `/api/auth/session` and reads `user.subscription_tier` and `user.subscription_status`. Active and trialing subscriptions qualify. It then filters the search picker by tier and excludes automatic routers, Computer models, and browser agents.

| Account | Current default for ask, search, and reasoning |
|---------|-----------------------------------------------|
| Pro | `gpt6_1_sol_thinking` |
| Max | `gpt6_astra_thinking` |
| Free or unknown | Paid model selection fails with an explanatory error |

Selection follows a preference rule, not a benchmark. On Max, the server prefers the highest-version Astra Thinking choice in the current picker. Otherwise it selects the highest-version eligible GPT reasoning choice. It compares numeric parts of backend IDs, so a newer GPT entry can become the default after a refresh. If no eligible GPT reasoning choice exists, it asks you to choose a model explicitly.

The order of precedence is:

1. A `model` argument on the tool call.
2. `PERPLEXITY_REASON_MODEL`, or the legacy `PERPLEXITY_MCP_MODEL` variable.
3. The account-aware default.

To pin your server to GPT-6.1 Sol Thinking:

```bash
export PERPLEXITY_REASON_MODEL="gpt6_1_sol_thinking"
```

This override applies to authenticated ask, search, and reasoning. The server checks overrides against the current picker and your plan. It reports unavailable choices instead of silently switching to a cheaper automatic route.

### Current search lineup

The bundled picker snapshot is dated October 2, 2026. `perplexity_models` shows the runtime list after discovery.

| Model | Standard ID | Thinking ID | Required plan |
|-------|-------------|-------------|---------------|
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

The catalog also records both browser-agent picker choices and all nine Computer lineups, including fast variants and DeepSeek V4 Pro. These are metadata. The five MCP tools do not execute Computer or browser-agent workflows.

## Automatic refresh

On startup, the server uses a fresh account-specific cache or fetches `/rest/models/config/v2?version=2.18&source=default`. It keeps current picker IDs and named research workflows, discarding older or hidden catalog entries.

After 24 hours, the next authenticated tool call refreshes both the model configuration and account status. This is a lazy refresh; there is no background polling. Force a check at any time by calling `perplexity_models` with:

```json
{"refresh": true}
```

New picker IDs become usable without updating the package. Removed IDs leave the active mappings. Catalog changes appear in stderr logs and in the tool's `changes` field.

If fetching fails, the server keeps the previous catalog. A valid disk cache survives restarts; the bundled picker is the final fallback. Normal failed checks retry after 24 hours, while an unknown account plan retries on the next call after one minute. A forced refresh bypasses either interval.

Cache files live in `$XDG_CACHE_HOME/perplexity-mcp`, or `~/.cache/perplexity-mcp`. Filenames use a hash of account/session cookies. Files contain model configuration and a timestamp, not cookies or account plan details. The account plan comes from the session response rather than the disk cache.

<details>
<summary>Fields returned by perplexity_models</summary>

| Field | Meaning |
|-------|---------|
| `subscription_tier` | `pro`, `max`, `free`, or `unknown` |
| `available_search_models` | Backend IDs eligible for search on the detected plan |
| `default_reasoning_model` | Effective default or environment override |
| `default_reasoning_model_available` | Whether that selection is currently eligible |
| `source` | `live`, `cache`, or `bundled` |
| `fetched_at` | Unix timestamp of the last successful catalog fetch |
| `stale` | Whether the catalog is at least 24 hours old |
| `refresh_error` | Exception type from the latest failed refresh, if any |
| `changes` | IDs added, removed, or updated by the last successful refresh |
| `models` | Filtered catalog metadata |
| `search_config` | Search and browser-agent picker metadata with tier requirements |
| `computer_config` | Computer picker metadata |

</details>

## Configuration

| Variable | Default | Purpose |
|----------|---------|---------|
| `PERPLEXITY_COOKIES` | Unset | JSON object containing browser cookies |
| `PERPLEXITY_SESSION_TOKEN` | Unset | Older next-auth session token |
| `PERPLEXITY_CSRF_TOKEN` | Unset | Older next-auth CSRF token |
| `PERPLEXITY_MCP_MODE` | `search` | Ask mode: `search`, `pro`, `reasoning`, or `deep research` |
| `PERPLEXITY_REASON_MODEL` | Account-aware | Explicit model override for ask, search, and reasoning |
| `MCP_TRANSPORT` | `stdio` | `stdio` or `http` |
| `MCP_HOST` | `127.0.0.1` | HTTP bind address |
| `MCP_PORT` | `8000` | HTTP port |

Authenticated `auto` mode is disabled. Non-null organization model policies also disable search model selection until that policy has explicit support. Tier filtering does not account for every possible rollout or organization entitlement; Perplexity still decides whether a request is allowed.

### HTTP transport

```bash
MCP_TRANSPORT=http MCP_HOST=127.0.0.1 MCP_PORT=8000 perplexity-mcp
```

The streamable HTTP endpoint is `http://127.0.0.1:8000/mcp`. The server does not add an authentication layer to that endpoint. Keep it local or place access controls in front of it when using it remotely.

## Development

From the checkout:

```bash
uv sync --python 3.12 --extra dev
uv run python -m pytest
uv run python -m black --target-version py312 perplexity perplexity_async tests
uv build --wheel
```

HTTP requests use `curl_cffi` with browser impersonation. Model discovery and tier-aware defaults live in [`perplexity/models.py`](perplexity/models.py); the bundled picker and aliases live in [`perplexity/config.py`](perplexity/config.py).

The repository also includes direct sync/async Python clients and legacy Labs utilities. Account-aware discovery belongs to the MCP server; direct library calls use static mappings unless you attach a `ModelRegistry` yourself.

## License

[MIT](LICENSE)
