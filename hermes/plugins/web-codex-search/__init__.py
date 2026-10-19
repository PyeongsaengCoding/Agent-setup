"""GPT web search relay (``web.search_backend: codex-search``).

Sends the query to the openai-codex Responses endpoint with OpenAI's server-side
``web_search`` tool and returns normal Hermes search rows. Works with any main-model
provider because the search is a separate client-side call.

Optional config ``web.codex_search``: ``model`` (default gpt-6-luna),
``reasoning_effort`` (default low), ``timeout`` seconds (default 90).
"""
from __future__ import annotations

import json
import logging
from typing import Any

from plugins.web._common import BaseWebSearchProvider, search_fail, search_ok, setup_schema
from plugins.web.openai_native.provider import has_codex_credentials
from plugins.web.xai.provider import XAIWebSearchProvider

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "gpt-6-luna"
DEFAULT_EFFORT = "low"
DEFAULT_TIMEOUT = 90.0
_INSTRUCTIONS = (
    "You are a web search backend. Always call the web_search tool, then reply with ONLY one JSON object "
    '(no prose, no markdown fences, no inline citations): {"results": [{"title": "string", "url": "string", '
    '"description": "1-2 sentence summary"}]}. Use absolute https:// URLs ordered by relevance; '
    'return {"results": []} when nothing usable is found.'
)


def _cfg() -> dict[str, Any]:
    try:
        from hermes_cli.config import load_config
        web = load_config().get("web") or {}
        cfg = web.get("codex_search") if isinstance(web, dict) else None
        return cfg if isinstance(cfg, dict) else {}
    except Exception as exc:  # config read failure falls back to defaults
        logger.debug("web.codex_search config unreadable: %s", exc)
        return {}


def _credentials(force_refresh: bool = False) -> tuple[str, str]:
    from hermes_cli.auth_codex import resolve_codex_runtime_credentials
    creds = resolve_codex_runtime_credentials(force_refresh=force_refresh)
    token = str(creds.get("api_key") or "").strip()
    base = str(creds.get("base_url") or "https://chatgpt.com/backend-api/codex").strip().rstrip("/")
    return token, base


class CodexWebSearchProvider(BaseWebSearchProvider):
    NAME = "codex-search"
    DISPLAY_NAME = "GPT Web Search relay (openai-codex)"

    def is_available(self) -> bool:
        return has_codex_credentials()

    def search(self, query: str, limit: int = 5) -> dict[str, Any]:
        try:
            limit = max(1, min(int(limit), 20))
        except (TypeError, ValueError):
            limit = 5
        cfg = _cfg()
        model = str(cfg.get("model") or DEFAULT_MODEL).strip()
        effort = str(cfg.get("reasoning_effort") or DEFAULT_EFFORT).strip()
        try:
            timeout = float(cfg.get("timeout") or DEFAULT_TIMEOUT)
        except (TypeError, ValueError):
            timeout = DEFAULT_TIMEOUT
        payload = {
            "model": model,
            "instructions": _INSTRUCTIONS,
            "input": [{"role": "user", "content": [
                {"type": "input_text", "text": f"Return at most {limit} results.\n\nQuery: {query}"}]}],
            "tools": [{"type": "web_search"}],
            "reasoning": {"effort": effort},
            "store": False,
            "stream": True,
        }
        try:
            token, base = _credentials()
        except Exception as exc:
            return search_fail(f"openai-codex sign-in unavailable for codex-search: {exc}")
        if not token:
            return search_fail("No openai-codex login. Run `hermes auth add openai-codex`.")
        logger.info("codex-search: %r (limit=%d, model=%s)", query, limit, model)
        response, error = self._post(base, token, payload, timeout)
        if error and error.startswith("HTTP 401"):
            try:
                token, base = _credentials(force_refresh=True)
                response, error = self._post(base, token, payload, timeout)
            except Exception as exc:
                error = f"{error}; refresh failed: {exc}"
        if error:
            return search_fail(f"codex-search failed: {error}")
        return search_ok(XAIWebSearchProvider._extract_results(response, limit=limit))

    @staticmethod
    def _post(base: str, token: str, payload: dict[str, Any], timeout: float) -> tuple[dict[str, Any], str]:
        import httpx
        from agent.codex_headers import codex_cloudflare_headers
        headers = codex_cloudflare_headers(token, base_url=base)
        headers.update({"Authorization": f"Bearer {token}", "Content-Type": "application/json",
                        "Accept": "text/event-stream"})
        final: dict[str, Any] = {}
        text = ""
        try:
            with httpx.stream("POST", f"{base}/responses", headers=headers, json=payload, timeout=timeout) as resp:
                if resp.status_code != 200:
                    return {}, f"HTTP {resp.status_code}: {resp.read()[:300].decode('utf-8', 'replace')}"
                for line in resp.iter_lines():
                    if not line.startswith("data:"):
                        continue
                    raw = line[5:].strip()
                    if raw == "[DONE]":
                        break
                    try:
                        event = json.loads(raw)
                    except ValueError:
                        continue
                    kind = event.get("type")
                    if kind == "response.output_text.delta":
                        text += event.get("delta") or ""
                    elif kind == "response.completed":
                        final = event.get("response") or {}
                    elif kind in ("response.failed", "response.incomplete", "error"):
                        detail = (event.get("response") or {}).get("error") or event.get("error") or kind
                        return {}, f"{kind}: {json.dumps(detail)[:300]}"
        except httpx.HTTPError as exc:
            return {}, f"request error: {exc}"
        if not final.get("output") and text:
            final = {"output": [{"type": "message", "content": [{"type": "output_text", "text": text}]}]}
        if not final:
            return {}, "empty response stream"
        return final, ""

    def get_setup_schema(self) -> dict[str, Any]:
        return setup_schema(self.DISPLAY_NAME, "native",
                            "Relays search to the openai-codex login's server-side web_search; works under any main model.",
                            "")


def register(ctx) -> None:
    ctx.register_web_search_provider(CodexWebSearchProvider())
