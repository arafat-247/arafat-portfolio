"""Local Ollama engine and adapter for the existing approved tool loop.

The app owns a separate loopback-only Ollama process with cloud features off.
No OpenAI credentials, HTTP proxies, remote endpoints or shell commands are used.
"""
from __future__ import annotations

import http.client
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import threading
import time
import uuid

from core import SYSTEM_PROMPT, Cancelled, check_cancel
from runtime import external_program_environment

PORT = 11435
STARTER_MODELS = {"qwen3:1.7b": "Light · about 1.4 GB"}
DEFAULT_LOCAL_MODEL = "qwen3:1.7b"
DOWNLOAD_URL = "https://ollama.com/download/windows"


def valid_model(name):
    if not isinstance(name, str) or not name or len(name) > 160:
        raise ValueError("Choose an installed local model first.")
    if any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_./:-" for c in name):
        raise ValueError("Invalid local model name.")
    if "cloud" in name.lower() or "://" in name or name.startswith(("/", ".")):
        raise ValueError("Cloud models are not supported in local mode.")
    return name


class LocalTransport:
    """Bounded loopback requests; Stop interrupts a stalled read or download."""
    def __init__(self, cancel=None):
        self.cancel = cancel or threading.Event()

    def request(self, path, payload=None, progress=None, timeout=300):
        check_cancel(self.cancel)
        if path not in {"/api/version", "/api/tags", "/api/show", "/api/chat", "/api/pull"}:
            raise ValueError("Unsupported local endpoint.")
        connection = http.client.HTTPConnection("127.0.0.1", PORT, timeout=2)
        done, result = threading.Event(), {}

        def perform():
            try:
                connection.connect()
                result["socket"] = connection.sock
                connection.sock.settimeout(timeout)
                body = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
                connection.request("GET" if body is None else "POST", path, body,
                                   {"Content-Type": "application/json", "Accept": "application/json"})
                response = connection.getresponse()
                if response.status != 200:
                    # Error bodies can repeat prompts. Keep diagnostics bounded and generic.
                    if response.status == 404:
                        raise RuntimeError("The local model was not found. Open Local setup and download or choose a model.")
                    raise RuntimeError(f"Local engine returned HTTP {response.status}. Check the selected model and available memory.")
                if progress is not None:
                    finished = False
                    while True:
                        check_cancel(self.cancel)
                        line = response.readline(65_537)
                        if not line:
                            break
                        if len(line) > 65_536:
                            raise RuntimeError("Invalid local download response.")
                        value = json.loads(line)
                        if not isinstance(value, dict) or value.get("error"):
                            raise RuntimeError("The local model download failed. Check internet access and free disk space, then retry.")
                        status = str(value.get("status", ""))
                        completed, total = value.get("completed"), value.get("total")
                        if type(completed) is int and type(total) is int and total > 0:
                            status = f"Downloading model · {min(100, completed * 100 // total)}%"
                        else:
                            status = "Local model download · " + status[:120]
                        progress("Status", status)
                        if value.get("status") == "success":
                            finished = True
                    if not finished:
                        raise RuntimeError("Model download ended before completion. Retry the download; Ollama can resume it.")
                    result["value"] = {"ok": True}
                else:
                    data = response.read(4_000_001)
                    if len(data) > 4_000_000:
                        raise RuntimeError("Local response exceeded the app's size limit.")
                    value = json.loads(data)
                    if not isinstance(value, dict) or value.get("error"):
                        raise RuntimeError("The local engine could not complete the request. Check its model and memory requirements.")
                    result["value"] = value
            except Exception as exc:
                result["error"] = exc
            finally:
                connection.close()
                done.set()

        worker = threading.Thread(target=perform, name="assistant-local-request", daemon=True)
        worker.start()
        deadline = time.monotonic() + timeout
        try:
            while not done.wait(0.1):
                check_cancel(self.cancel)
                if time.monotonic() >= deadline:
                    raise RuntimeError("Local model timed out. Try the Light model or a shorter task.")
            check_cancel(self.cancel)
        finally:
            if not done.is_set():
                if result.get("socket"):
                    try:
                        result["socket"].shutdown(socket.SHUT_RDWR)
                    except OSError:
                        pass
                connection.close()
                worker.join(timeout=0.5)
        if "error" in result:
            exc = result["error"]
            if isinstance(exc, (RuntimeError, Cancelled)):
                raise exc
            if isinstance(exc, (OSError, http.client.HTTPException)):
                raise RuntimeError("Could not contact the local engine. Open Local setup and select Check local models.") from None
            raise RuntimeError("The local engine returned an unreadable response. No further actions were run.") from None
        return result["value"]


class LocalEngine:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.process = None

    def start(self, cancel):
        check_cancel(cancel)
        if self.process is not None:
            if self.process.poll() is None:
                return
            self.process = None
        program = shutil.which("ollama")
        if sys.platform == "win32":
            installed = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Ollama" / "ollama.exe"
            if installed.is_file():
                program = str(installed)
        if not program:
            raise RuntimeError("Install Ollama once using Download Ollama in Local setup. Then select Check local models. No account is needed.")
        try:
            with socket.create_connection(("127.0.0.1", PORT), timeout=0.2):
                raise RuntimeError("Local engine port 11435 is already in use. Close the other assistant or local engine before retrying.")
        except OSError:
            pass
        self.directory.mkdir(parents=True, exist_ok=True)
        env = dict(os.environ, OLLAMA_HOST=f"127.0.0.1:{PORT}", OLLAMA_NO_CLOUD="1", OLLAMA_DEBUG="0")
        with (self.directory / "local-engine.log").open("w", encoding="utf-8") as log:
            with external_program_environment():
                self.process = subprocess.Popen([program, "serve"], stdin=subprocess.DEVNULL,
                    stdout=log, stderr=subprocess.STDOUT, env=env,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0)
        deadline = time.monotonic() + 25
        try:
            while time.monotonic() < deadline:
                check_cancel(cancel)
                if self.process.poll() is not None:
                    raise RuntimeError("The local engine did not start. Check local-engine.log in the assistant's data folder.")
                try:
                    LocalTransport(cancel).request("/api/version", timeout=2)
                    return
                except RuntimeError:
                    cancel.wait(0.2)
            raise RuntimeError("The local engine did not become ready. Retry Check local models.")
        except Exception:
            self.close()
            raise

    def close(self):
        if self.process is not None:
            process, self.process = self.process, None
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=2)


def installed_models(transport):
    data = transport.request("/api/tags", timeout=20)
    models = []
    for row in data.get("models", []):
        try:
            name = valid_model(row.get("name"))
            if row.get("remote_host") or row.get("remote_model") or row.get("details", {}).get("format") != "gguf":
                continue
            size = row.get("size", 0)
            suffix = f" · {size / 1_000_000_000:.1f} GB" if type(size) is int and size > 0 else ""
            models.append({"slug": name, "display_name": name + suffix})
        except (ValueError, AttributeError):
            continue
    return models


def pull_starter(transport, model, progress):
    if model not in STARTER_MODELS:
        raise ValueError("Choose one of the offered starter models.")
    return transport.request("/api/pull", {"model": model, "stream": True}, progress, timeout=1800)


def chat_messages(items):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    call_names = {}
    for item in items:
        kind = item.get("type")
        if kind == "function_call":
            if messages[-1]["role"] != "assistant":
                messages.append({"role": "assistant", "content": "", "tool_calls": []})
            name = item["name"]
            call_names[item["call_id"]] = name
            messages[-1].setdefault("tool_calls", []).append({"function": {"name": name, "arguments": json.loads(item["arguments"])}})
        elif kind == "function_call_output":
            if item["call_id"] not in call_names:
                raise ValueError("Local tool result has no matching call.")
            # Shorten large page reads for small models; retain valid observed control IDs.
            value = json.loads(item["output"])
            result = value.get("result")
            if isinstance(result, dict):
                if isinstance(result.get("text"), str) and len(result["text"]) > 4000:
                    result["text"] = result["text"][:4000]
                    result["text_truncated"] = True
                if isinstance(result.get("controls"), list) and len(result["controls"]) > 35:
                    result["controls"] = result["controls"][:35]
                    result["local_controls_truncated"] = True
            messages.append({"role": "tool", "tool_name": call_names[item["call_id"]],
                             "content": json.dumps(value, ensure_ascii=False)})
        elif item.get("role") in {"user", "assistant"}:
            content = item.get("content", "")
            if isinstance(content, list):
                content = "\n".join(p.get("text", "") for p in content if p.get("type") in {"output_text", "input_text"})
            messages.append({"role": item["role"], "content": str(content)})
    return messages


class LocalClient:
    def __init__(self, model, cancel=None, transport=None):
        self.model = valid_model(model)
        self.cancel = cancel or threading.Event()
        self.transport = transport or LocalTransport(self.cancel)
        self.metadata = None

    def response(self, items, tools):
        check_cancel(self.cancel)
        if self.metadata is None:
            meta = self.transport.request("/api/show", {"model": self.model}, timeout=30)
            if meta.get("remote_model") or meta.get("remote_host") or meta.get("details", {}).get("format") != "gguf" or not meta.get("model_info"):
                raise RuntimeError("Choose a downloaded local GGUF model. Cloud models are disabled in this app.")
            if "tools" not in meta.get("capabilities", []):
                raise RuntimeError("This model does not support tools. Download a Qwen3 starter model in Local setup.")
            self.metadata = meta
        messages = chat_messages(items)
        local_tools = [{"type": "function", "function": {k: schema[k] for k in ("name", "description", "parameters")}} for schema in tools]
        payload = {"model": self.model, "messages": messages, "tools": local_tools, "stream": False,
                   "options": {"num_ctx": 8192, "num_predict": 1800, "temperature": 0}, "keep_alive": "5m"}
        if "thinking" in self.metadata.get("capabilities", []):
            payload["think"] = False
        if len(json.dumps(payload, ensure_ascii=False).encode("utf-8")) > 24_000:
            raise RuntimeError("This task is too long for local mode. Start a new conversation and give one shorter task.")
        data = self.transport.request("/api/chat", payload)
        if data.get("done") is not True or data.get("done_reason") not in (None, "stop"):
            raise RuntimeError("The local model did not finish. No further actions were run; try a shorter task.")
        message = data.get("message")
        if not isinstance(message, dict) or message.get("role") != "assistant":
            raise RuntimeError("Invalid local model reply. No action was run.")
        output = []
        content = message.get("content", "")
        if not isinstance(content, str):
            raise RuntimeError("Invalid local reply text.")
        if content.strip():
            output.append({"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": content.strip()}]})
        calls = message.get("tool_calls", [])
        if not isinstance(calls, list) or len(calls) > 8:
            raise RuntimeError("Invalid local tool request. No action was run.")
        known = {schema["name"]: schema for schema in tools}
        for call in calls:
            fn = call.get("function", {}) if isinstance(call, dict) else {}
            name, args = fn.get("name"), fn.get("arguments")
            if name not in known or not isinstance(args, dict):
                raise RuntimeError("The local model requested an unsupported action. No action was run.")
            props = known[name]["parameters"]["properties"]
            if set(args) != set(props):
                raise RuntimeError("The local model returned incomplete action details. No action was run.")
            for key, value in args.items():
                if (props[key]["type"] == "string" and not isinstance(value, str)) or (props[key]["type"] == "integer" and type(value) is not int):
                    raise RuntimeError("The local model returned invalid action details. No action was run.")
            output.append({"type": "function_call", "call_id": "local_" + uuid.uuid4().hex,
                           "name": name, "arguments": json.dumps(args, ensure_ascii=False)})
        check_cancel(self.cancel)
        return {"status": "completed", "output": output}
