import json
import os
import sys
from importlib.metadata import version

from mcp.server import MCPServer

from perplexity import Client
from perplexity.config import DEFAULT_REASONING_MODEL
from perplexity.logger import setup_logger

logger = setup_logger("mcp")

DEFAULT_MODE = os.environ.get("PERPLEXITY_MCP_MODE", "search")
DEFAULT_MODEL = os.environ.get(
    "PERPLEXITY_REASON_MODEL",
    os.environ.get("PERPLEXITY_MCP_MODEL", DEFAULT_REASONING_MODEL),
)

mcp = MCPServer("perplexity", version=version("perplexity-mcp"))


def perplexity_ask(query: str) -> str:
    """Ask Perplexity a question and get a concise AI-generated answer.

    Uses Perplexity search by default when authenticated, and auto mode when
    anonymous. This is the default general-purpose tool. Use it for factual
    questions, explanations, summaries, and most everyday queries.

    Limitations:
    - Does not support follow-up context, file uploads, or source filtering.
    - Returns plain text only (no citations, images, or structured results).
    - Answers may not reflect the very latest real-time information.
    """
    if client.own:
        return client.search(query, **resolve_default_search_kwargs()).get("answer", "")
    return client.search(query, mode="auto").get("answer", "")


def perplexity_research(query: str) -> str:
    """Conduct deep, multi-step research on a topic using Perplexity.

    Uses Perplexity's deep research mode, which autonomously breaks the query
    into sub-questions, searches broadly, and synthesizes a comprehensive report.
    Only use this when the task genuinely needs deep synthesis across many
    sources. Prefer asking smaller, focused research questions instead of one
    huge query whenever possible.

    Limitations:
    - Significantly slower than other tools (may take 30–120 seconds).
    - Does not support follow-up context, file uploads, or source filtering.
    - Returns plain text only (no citations, images, or structured results).
    - Only one model is available in this mode (cannot select a specific model).
    """
    return client.search(query, mode="deep research").get("answer", "")


def perplexity_reason(query: str) -> str:
    """Ask Perplexity to reason step-by-step through a complex problem.

    Uses Perplexity's reasoning mode, which applies chain-of-thought reasoning
    before producing an answer. Best for logic puzzles, math problems, multi-step
    analysis, coding questions, and decisions requiring structured thinking.

    Limitations:
    - Slower than auto mode due to the reasoning step.
    - Does not support follow-up context, file uploads, or source filtering.
    - Returns plain text only (no citations, images, or structured results).
    """
    return client.search(query, mode="reasoning", model=DEFAULT_MODEL).get("answer", "")


def perplexity_search(query: str) -> str:
    """Search the web using Perplexity and get an AI-synthesized answer.

    Uses Perplexity's Pro mode with web sources, providing a more thorough
    web search than auto mode. This is the default authenticated path for
    unspecified MCP asks. Best for current events, recent developments, and
    queries where up-to-date web results are important.

    Limitations:
    - Only searches the web (no academic/scholar or social sources).
    - Does not support follow-up context or file uploads.
    - Returns plain text only (no citations, images, or structured results).
    """
    return client.search(query, mode="pro", sources=["web"]).get("answer", "")


def resolve_default_search_kwargs(mode: str = DEFAULT_MODE) -> dict:
    """Resolve the configured default MCP ask mode to Client.search kwargs."""
    normalized_mode = mode.strip().lower().replace("_", "-")

    if normalized_mode in {"search", "pro"}:
        return {"mode": "pro", "sources": ["web"]}

    if normalized_mode == "reasoning":
        return {"mode": "reasoning", "model": DEFAULT_MODEL}

    if normalized_mode in {"research", "deep-research", "deep research"}:
        return {"mode": "deep research"}

    if normalized_mode == "auto":
        return {"mode": "auto"}

    raise ValueError(
        "PERPLEXITY_MCP_MODE must be one of: search, pro, reasoning, deep research, auto"
    )


def load_cookies_from_env() -> dict:
    """Load Perplexity auth cookies from supported environment variables."""
    cookies_env = os.environ.get("PERPLEXITY_COOKIES")
    if cookies_env:
        try:
            return json.loads(cookies_env)
        except json.JSONDecodeError:
            sys.exit("ERROR: PERPLEXITY_COOKIES is not valid JSON.")

    cookies = {}
    session_token = os.environ.get("PERPLEXITY_SESSION_TOKEN")
    csrf_token = os.environ.get("PERPLEXITY_CSRF_TOKEN")

    if session_token:
        cookies["next-auth.session-token"] = session_token
        cookies["__Secure-next-auth.session-token"] = session_token

    if csrf_token:
        cookies["next-auth.csrf-token"] = csrf_token
        cookies["__Host-next-auth.csrf-token"] = csrf_token

    return cookies


USAGE = """\
usage: perplexity-mcp [--help] [--version]

Perplexity MCP server. Runs on stdio by default; set MCP_TRANSPORT=http for
streamable HTTP.

Environment:
  PERPLEXITY_SESSION_TOKEN  next-auth session token from perplexity.ai
  PERPLEXITY_CSRF_TOKEN     next-auth CSRF token from perplexity.ai
  PERPLEXITY_COOKIES        full cookie JSON (takes precedence over the above)
  PERPLEXITY_MCP_MODE       search (default), reasoning, deep research, auto
  PERPLEXITY_REASON_MODEL   model alias for perplexity_reason (default: {model})
  MCP_TRANSPORT             stdio (default) or http
  MCP_HOST                  HTTP bind host (default: 127.0.0.1)
  MCP_PORT                  HTTP bind port (default: 8000)
""".format(model=DEFAULT_REASONING_MODEL)


def main():
    global client

    if "--help" in sys.argv[1:] or "-h" in sys.argv[1:]:
        print(USAGE, end="")
        return

    if "--version" in sys.argv[1:]:
        print(version("perplexity-mcp"))
        return

    client = Client(load_cookies_from_env())

    mcp.tool()(perplexity_ask)

    if client.own:
        logger.info("Authenticated - all 4 tools available.")
        mcp.tool()(perplexity_research)
        mcp.tool()(perplexity_reason)
        mcp.tool()(perplexity_search)
    else:
        logger.warning(
            "No PERPLEXITY_COOKIES set - running anonymously. "
            "Only perplexity_ask is available. "
            "Set PERPLEXITY_SESSION_TOKEN and PERPLEXITY_CSRF_TOKEN, or PERPLEXITY_COOKIES, "
            "to enable perplexity_search, perplexity_reason, and perplexity_research."
        )

    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    if transport not in ("stdio", "http"):
        sys.exit("ERROR: MCP_TRANSPORT must be 'stdio' or 'http'")

    if transport == "stdio":
        mcp.run()
    else:
        mcp.run(
            transport="streamable-http",
            host=os.environ.get("MCP_HOST", "127.0.0.1"),
            port=int(os.environ.get("MCP_PORT", "8000")),
        )


if __name__ == "__main__":
    main()
