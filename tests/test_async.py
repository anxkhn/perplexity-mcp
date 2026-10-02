"""Check awaitable construction without opening network sessions."""

import pytest

from perplexity_async.client import Client
from perplexity_async.emailnator import AsyncMixin, Emailnator
from perplexity_async.labs import LabsClient


@pytest.mark.parametrize("client_class", [Client, Emailnator, LabsClient])
async def test_async_clients_share_awaitable_initialization(client_class, monkeypatch):
    calls = []

    async def initialize(self, value):
        calls.append(value)

    monkeypatch.setattr(client_class, "__ainit__", initialize)
    instance = client_class("argument")
    assert isinstance(instance, AsyncMixin)
    assert await instance is instance
    assert calls == ["argument"]
    with pytest.raises(AssertionError):
        await instance
