"""Stateless streamed Responses requests authorised by a ChatGPT plan."""
from __future__ import annotations

import json
import re
import threading
from urllib import error, request

from core import SYSTEM_PROMPT, check_cancel
from chatgpt_auth import RESOURCE


def plan_error(code, status=None):
    messages = {
        "subscription_sharing_usage_limit_exceeded": "Your ChatGPT plan allowance or this app's usage cap was reached. Open Manage usage; wait for its reset or adjust the app's cap.",
        "subscription_sharing_usage_unavailable": "ChatGPT plan usage is temporarily unavailable. Open Manage usage and retry later.",
        "subscription_sharing_user_not_eligible": "This ChatGPT account or workspace is not eligible. Reconnect using your eligible personal Plus or Pro account.",
        "subscription_sharing_not_enabled": "Plan usage was not enabled. Reconnect and allow Use your ChatGPT plan.",
        "rate_limit_exceeded": "ChatGPT requests were temporarily limited. Wait before trying again.",
        "slow_down": "ChatGPT requests were temporarily limited. Wait before trying again.",
        "credit_balance_exhausted": "The selected connection returned an API billing error. Reconnect through Continue with ChatGPT; this app will not switch to paid API access.",
        "insufficient_quota": "The selected connection returned a quota error. Check Manage usage and reconnect through Continue with ChatGPT.",
    }
    if code in messages:
        return messages[code]
    if status == 401:
        return "Your ChatGPT connection needs renewal. Select Continue with ChatGPT again."
    if status == 403:
        return "ChatGPT did not allow this request. Reconnect and check the selected account, plan permission and model."
    if status == 429:
        return "Your ChatGPT plan or request limit was reached. Open Manage usage and check the reset time before retrying."
    suffix = f" ({code})" if isinstance(code, str) and re.fullmatch(r"[a-z0-9_]{1,90}", code) else ""
    return "ChatGPT could not finish this request" + suffix + ". Try a shorter task or reconnect."


def read_stream(response, cancel):
    """Return only a completed response; partial text never authorises a tool."""
    data, size = [], 0
    for line in response:
        check_cancel(cancel)
        size += len(line)
        if size > 10_000_000:
            raise RuntimeError("ChatGPT response exceeded the app's size limit. Try a shorter task.")
        line = line.decode("utf-8").rstrip("\r\n") if isinstance(line, bytes) else line.rstrip("\r\n")
        if line.startswith("data:"):
            data.append(line[5:].lstrip())
        elif not line and data:
            raw, data = "\n".join(data), []
            if raw == "[DONE]":
                continue
            try:
                event = json.loads(raw)
            except ValueError:
                raise RuntimeError("ChatGPT returned an unreadable stream. No further actions were run.") from None
            kind = event.get("type")
            body = event.get("response", {})
            if kind == "response.completed":
                if body.get("status") != "completed":
                    raise RuntimeError("ChatGPT did not complete this response. No further actions were run.")
                return body
            if kind in {"response.failed", "response.incomplete", "error"}:
                detail = body.get("error") or event.get("error") or event
                raise RuntimeError(plan_error(detail.get("code")))
    raise RuntimeError("The ChatGPT stream ended before completion. No further actions were run.")


class ChatGPTClient:
    def __init__(self, session, model, cancel=None):
        if not model:
            raise ValueError("Connect ChatGPT and choose an available model first.")
        self.session, self.model = session, model
        self.cancel = cancel or threading.Event()

    def response(self, items, tools):
        token = self.session.access_token()
        check_cancel(self.cancel)
        payload = {"model": self.model, "instructions": SYSTEM_PROMPT, "input": items,
                   "store": False, "stream": True, "include": ["reasoning.encrypted_content"],
                   "parallel_tool_calls": False}
        if tools:
            payload["tools"] = [{"type": "namespace", "name": "assistant",
                                 "description": "Approved local website, Windows app and note tools.", "tools": tools}]
        req = request.Request(RESOURCE + "/responses", data=json.dumps(payload, ensure_ascii=False).encode(),
                              headers={"Authorization": "Bearer " + token, "Content-Type": "application/json", "Accept": "text/event-stream"})
        try:
            with request.urlopen(req, timeout=60) as response:
                return read_stream(response, self.cancel)
        except error.HTTPError as exc:
            code = None
            try:
                code = json.loads(exc.read(12_000)).get("error", {}).get("code")
            except (ValueError, AttributeError):
                pass
            raise RuntimeError(plan_error(code, exc.code)) from None
        except (error.URLError, TimeoutError):
            raise RuntimeError("Could not reach ChatGPT. Check your connection and try again.") from None
