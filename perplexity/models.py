"""Account-specific model discovery for the MCP server."""

import hashlib
import json
import os
import re
import tempfile
import time
from copy import deepcopy
from pathlib import Path
from threading import Lock

from curl_cffi.requests.exceptions import RequestException

from .config import (
    API_VERSION,
    ENDPOINT_AUTH_SESSION,
    ENDPOINT_MODEL_CONFIG,
    MODEL_ALIASES,
    MODEL_CONFIG,
    picker_models,
)
from .logger import setup_logger

logger = setup_logger("models")
REFRESH_SECONDS = 24 * 60 * 60
TIER_RANK = {"free": 0, "pro": 1, "max": 2}
AUTO_MODEL_IDS = {"turbo", "pplx_pro", "pplx_pro_upgraded", "pplx_reasoning"}


def subscription_tier(session):
    user = session.get("user", {}) if isinstance(session, dict) else {}
    if not isinstance(user, dict):
        return "unknown"
    tier = user.get("subscription_tier")
    status = user.get("subscription_status")
    if status not in {"active", "trialing"}:
        return "free" if status else "unknown"
    return tier if tier in TIER_RANK else "unknown"


def validate_config(data):
    if not isinstance(data, dict) or data.get("config_schema") != "v2":
        raise ValueError("Expected a v2 model config")
    models = data.get("models")
    if not isinstance(models, dict) or not models:
        raise ValueError("Model config has no models")
    for model_id, entry in models.items():
        if not isinstance(entry, dict) or not all(
            isinstance(entry.get(key), str) for key in ("label", "mode")
        ):
            raise ValueError(f"Invalid metadata for model {model_id}")
    defaults = data.get("default_models")
    if not isinstance(defaults, dict) or defaults.get("research") not in models:
        raise ValueError("Missing research default model")
    for key in ("search_config", "computer_config"):
        if not isinstance(data.get(key), list) or not all(
            isinstance(entry, dict) for entry in data[key]
        ):
            raise ValueError(f"Invalid {key}")
        for entry in data[key]:
            if (
                not isinstance(entry.get("subscription_tier"), str)
                or entry["subscription_tier"] not in TIER_RANK
            ):
                raise ValueError(f"Invalid subscription tier in {key}")
            for field in ("model", "fast_model", "non_reasoning_model", "reasoning_model"):
                if entry.get(field) is not None and (
                    not isinstance(entry[field], str) or entry[field] not in models
                ):
                    raise ValueError(f"Unknown model in {key}")
    if not any(
        entry.get(field) in models
        and models[entry[field]]["mode"] == "search"
        and entry[field] not in AUTO_MODEL_IDS
        for entry in data["search_config"]
        for field in ("non_reasoning_model", "reasoning_model")
    ):
        raise ValueError("Model config has no explicit search choices")
    return {**data, "models": picker_models(data)}


class ModelRegistry:
    def __init__(self, client, cache_path=None):
        self.client = client
        if cache_path is None:
            cookies = client.session.cookies.get_dict()
            identity = {
                key: value
                for key, value in cookies.items()
                if "session" in key or key == "__Host-pplx-last-active-account"
            }
            account = hashlib.sha256(
                json.dumps(identity or cookies, sort_keys=True).encode()
            ).hexdigest()[:16]
            cache_root = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
            cache_path = cache_root / "perplexity-mcp" / f"models-{account}.json"
        self.cache_path = Path(cache_path)
        self.config = deepcopy(MODEL_CONFIG)
        self.tier = subscription_tier(getattr(client, "auth_session", {}))
        self.source = "bundled"
        self.fetched_at = 0
        self.last_attempt = 0
        self.refresh_error = None
        self.changes = {"added": [], "removed": [], "updated": []}
        self.lock = Lock()
        try:
            cached = json.loads(self.cache_path.read_text())
            fetched_at = float(cached["fetched_at"])
            if not 0 < fetched_at <= time.time():
                raise ValueError("Invalid cache timestamp")
            self.config = validate_config(cached["config"])
            self.fetched_at = fetched_at
            self.source = "cache"
        except (OSError, ValueError, KeyError, TypeError):
            pass
        self._apply_mappings()

    def _apply_mappings(self):
        models = self.config["models"]
        self.available_search_models = set()
        for entry in self.config["search_config"]:
            if self.config.get("organization_model_policy") is not None:
                continue
            if TIER_RANK.get(self.tier, -1) < TIER_RANK.get(entry.get("subscription_tier"), 99):
                continue
            for field in ("non_reasoning_model", "reasoning_model"):
                model_id = entry.get(field)
                if (
                    model_id
                    and model_id not in AUTO_MODEL_IDS
                    and models[model_id]["mode"] == "search"
                ):
                    self.available_search_models.add(model_id)
        mappings = {model_id: model_id for model_id in self.available_search_models}
        mappings.update(
            {alias: target for alias, target in MODEL_ALIASES.items() if target in mappings}
        )
        research = self.config["default_models"]["research"]
        self.default_model = self._select_default()
        self.client.model_mappings = {
            "auto": {None: "turbo", "turbo": "turbo"},
            "pro": {**({None: self.default_model} if self.default_model else {}), **mappings},
            "reasoning": {**({None: self.default_model} if self.default_model else {}), **mappings},
            "deep research": {None: research, research: research, "deep-research": research},
        }

    def _select_default(self):
        # Prefer Astra on Max, otherwise the newest GPT reasoning picker choice.
        candidates = [
            entry["reasoning_model"]
            for entry in self.config["search_config"]
            if entry.get("reasoning_model") in self.available_search_models
        ]
        openai = [model for model in candidates if model.startswith("gpt")]
        if self.tier == "max":
            astra = [model for model in openai if "astra" in model]
            if astra:
                return max(astra, key=lambda model: tuple(map(int, re.findall(r"\d+", model))))
        if openai:
            return max(openai, key=lambda model: tuple(map(int, re.findall(r"\d+", model))))
        return None

    def resolve_model(self, model=None):
        selected = model if model is not None else self.default_model
        if selected not in self.client.model_mappings["reasoning"]:
            raise ValueError(
                f"Model {selected!r} is not an available search model for tier {self.tier!r}. "
                "Use perplexity_models to check your plan and available models."
            )
        return self.client.model_mappings["reasoning"][selected]

    def refresh(self, force=False):
        with self.lock:
            now = time.time()
            if (
                not force
                and self.tier != "unknown"
                and now - max(self.fetched_at, self.last_attempt) < REFRESH_SECONDS
            ):
                return
            if (
                not force
                and self.tier == "unknown"
                and self.last_attempt
                and now - self.last_attempt < 60
            ):
                return
            self.last_attempt = now
            try:
                headers = {"accept": "application/json", "x-app-apiversion": API_VERSION}
                account = self.client.session.cookies.get_dict().get(
                    "__Host-pplx-last-active-account"
                )
                if account:
                    headers["x-pplx-account"] = account
                response = self.client.session.get(
                    ENDPOINT_MODEL_CONFIG,
                    params={"version": API_VERSION, "source": "default"},
                    headers=headers,
                    timeout=10,
                )
                response.raise_for_status()
                data = validate_config(response.json())
                session_response = self.client.session.get(
                    ENDPOINT_AUTH_SESSION, headers=headers, timeout=10
                )
                session_response.raise_for_status()
                self.tier = subscription_tier(session_response.json())
            except (RequestException, ValueError, TypeError) as exc:
                self.refresh_error = type(exc).__name__
                logger.warning(
                    "Model refresh failed (%s); using %s config", self.refresh_error, self.source
                )
                return
            old, new = self.config["models"], data["models"]
            self.changes = {
                "added": sorted(new.keys() - old.keys()),
                "removed": sorted(old.keys() - new.keys()),
                "updated": sorted(key for key in old.keys() & new.keys() if old[key] != new[key]),
            }
            self.config = data
            self.fetched_at = now
            self.source = "live"
            self.refresh_error = None
            self._apply_mappings()
            if any(self.changes.values()):
                logger.info("Model catalog refreshed: %s", self.changes)
            try:
                self.cache_path.parent.mkdir(parents=True, exist_ok=True)
                with tempfile.NamedTemporaryFile(
                    mode="w", dir=self.cache_path.parent, delete=False
                ) as file:
                    temporary_path = Path(file.name)
                    try:
                        json.dump({"fetched_at": now, "config": data}, file)
                        file.close()
                        os.replace(temporary_path, self.cache_path)
                    finally:
                        temporary_path.unlink(missing_ok=True)
            except OSError:
                logger.warning("Could not save model cache; live models remain available")

    def list_models(self, default_model=None, refresh=False):
        self.refresh(force=refresh)
        selected = default_model or self.default_model
        return {
            "source": self.source,
            "fetched_at": self.fetched_at or None,
            "stale": time.time() - self.fetched_at >= REFRESH_SECONDS,
            "refresh_error": self.refresh_error,
            "changes": self.changes,
            "subscription_tier": self.tier,
            "available_search_models": sorted(self.available_search_models),
            "default_reasoning_model": selected,
            "default_reasoning_model_available": selected
            in self.client.model_mappings["reasoning"],
            "models": self.config["models"],
            "search_config": self.config["search_config"],
            "computer_config": self.config["computer_config"],
        }
