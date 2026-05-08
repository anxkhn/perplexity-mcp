"""Tests for MCP environment handling."""

import json

import pytest

from perplexity.mcp import load_cookies_from_env, resolve_default_search_kwargs


def test_default_mcp_mode_resolves_to_search() -> None:
    print("console.log -> validating default MCP ask mode")
    assert resolve_default_search_kwargs() == {"mode": "pro", "sources": ["web"]}


def test_default_mcp_mode_supports_reasoning_and_research() -> None:
    print("console.log -> validating explicit MCP ask modes")
    assert resolve_default_search_kwargs("reasoning")["mode"] == "reasoning"
    assert resolve_default_search_kwargs("deep research") == {"mode": "deep research"}


def test_load_cookies_prefers_json_cookie_env(monkeypatch) -> None:
    print("console.log -> validating PERPLEXITY_COOKIES support")
    monkeypatch.setenv("PERPLEXITY_COOKIES", json.dumps({"custom": "cookie"}))
    monkeypatch.setenv("PERPLEXITY_SESSION_TOKEN", "session")
    monkeypatch.setenv("PERPLEXITY_CSRF_TOKEN", "csrf")

    assert load_cookies_from_env() == {"custom": "cookie"}


def test_load_cookies_builds_nextauth_cookie_names(monkeypatch) -> None:
    print("console.log -> validating session/csrf env cookie support")
    monkeypatch.delenv("PERPLEXITY_COOKIES", raising=False)
    monkeypatch.setenv("PERPLEXITY_SESSION_TOKEN", "session")
    monkeypatch.setenv("PERPLEXITY_CSRF_TOKEN", "csrf")

    cookies = load_cookies_from_env()

    assert cookies["next-auth.session-token"] == "session"
    assert cookies["__Secure-next-auth.session-token"] == "session"
    assert cookies["next-auth.csrf-token"] == "csrf"
    assert cookies["__Host-next-auth.csrf-token"] == "csrf"


def test_load_cookies_exits_on_invalid_json(monkeypatch) -> None:
    print("console.log -> validating invalid cookie JSON fails")
    monkeypatch.setenv("PERPLEXITY_COOKIES", "not-json")

    with pytest.raises(SystemExit):
        load_cookies_from_env()
