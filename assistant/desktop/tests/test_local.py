"""Real loopback protocol tests. No model or remote API is required."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import queue
import socket
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import local_client as local
from automation import Tools
from core import Agent, Cancelled, Declined, TOOL_SCHEMAS
import settings

META = {"details": {"format": "gguf"}, "model_info": {"general.architecture": "qwen3"},
        "capabilities": ["completion", "tools", "thinking"]}


def answer(text="সম্পন্ন"):
    return {"done": True, "done_reason": "stop", "message": {"role": "assistant", "content": text}}


def action(name="save_note", args=None):
    value = answer("")
    value["message"]["tool_calls"] = [{"function": {"name": name, "arguments": args if args is not None else {"filename": "বাংলা", "content": "পরীক্ষা"}}}]
    return value


class LocalTests(unittest.TestCase):
    def setUp(self):
        self.seen, self.replies = [], []
        self.meta = dict(META)
        self.delay = False
        self.started, self.release = threading.Event(), threading.Event()
        owner = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                owner.seen.append((self.path, body, dict(self.headers)))
                if self.path == "/api/show":
                    value = owner.meta
                elif self.path == "/api/chat":
                    if owner.delay:
                        owner.started.set()
                        owner.release.wait(3)
                    value = owner.replies.pop(0)
                elif self.path == "/api/pull":
                    value = {"status": "success"}
                else:
                    raise AssertionError(self.path)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                try:
                    self.wfile.write(json.dumps(value, ensure_ascii=False).encode("utf-8") + b"\n")
                except (BrokenPipeError, ConnectionResetError):
                    pass

            def do_GET(self):
                owner.seen.append((self.path, None, dict(self.headers)))
                value = {"models": [
                    {"name": "qwen3:4b", "size": 2_500_000_000, "details": {"format": "gguf"}},
                    {"name": "hidden-cloud", "details": {"format": "gguf"}},
                    {"name": "alias", "remote_model": "remote", "details": {"format": "gguf"}},
                    {"name": "unknown", "details": {}},
                ]}
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(value).encode())

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.port_patch = patch.object(local, "PORT", self.server.server_port)
        self.port_patch.start()

    def tearDown(self):
        self.release.set()
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(2)
        self.port_patch.stop()

    def test_real_loopback_tool_cycle_writes_only_after_approval_and_preserves_bangla(self):
        self.replies = [action(), answer()]
        cancel = threading.Event()
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            approvals = []
            tools = Tools(root / "browser", root / "notes", {}, lambda *args: approvals.append(args) or True, lambda *args: None)
            with patch.dict(os.environ, {"HTTP_PROXY": "http://127.0.0.1:1", "OPENAI_API_KEY": "DO_NOT_SEND"}):
                result = Agent(local.LocalClient("qwen3:4b", cancel), tools, lambda *args: None).run("বাংলায় একটি নোট লেখো", cancel)
            self.assertEqual(result, "সম্পন্ন")
            self.assertEqual(next((root / "notes").glob("*.txt")).read_text(encoding="utf-8"), "পরীক্ষা")
            self.assertEqual(len(approvals), 1)
        chat = [row for row in self.seen if row[0] == "/api/chat"]
        self.assertEqual(chat[1][1]["messages"][-1]["role"], "tool")
        self.assertEqual(chat[1][1]["messages"][-1]["tool_name"], "save_note")
        self.assertIn("পরীক্ষা", chat[1][1]["messages"][-2]["tool_calls"][0]["function"]["arguments"]["content"])
        self.assertEqual(chat[0][1]["tools"][0]["function"]["name"], "browser_open")
        self.assertFalse(chat[0][1]["think"])
        self.assertFalse(chat[0][1]["stream"])
        self.assertNotIn("DO_NOT_SEND", json.dumps(self.seen))
        self.assertFalse(any("Authorization" in row[2] for row in self.seen))

    def test_declined_local_action_stops_without_second_generation_or_file_write(self):
        self.replies = [action(), answer("must not be reached")]
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            tools = Tools(root, root / "notes", {}, lambda *args: False, lambda *args: None)
            with self.assertRaises(Declined):
                Agent(local.LocalClient("qwen3:4b"), tools, lambda *args: None).run("Save a note", threading.Event())
            self.assertFalse((root / "notes").exists())
        self.assertEqual(sum(row[0] == "/api/chat" for row in self.seen), 1)

    def test_partial_invalid_and_unknown_tool_outputs_never_become_actions(self):
        bad = [dict(action(), done=False), dict(action(), done_reason="length"),
               action("run_shell", {"command": "anything"}), action("save_note", {"filename": "x"}),
               action("window_read", {"handle": True}), action("save_note", "not an object")]
        for value in bad:
            self.replies = [value]
            with self.subTest(value=value), self.assertRaises(RuntimeError):
                local.LocalClient("qwen3:4b").response([{"role": "user", "content": "Test"}], TOOL_SCHEMAS)

    def test_cloud_alias_and_models_without_tools_are_rejected_before_inference(self):
        for meta in [dict(META, remote_host="https://example.com"), dict(META, model_info={}),
                     dict(META, capabilities=["completion"])]:
            self.meta = meta
            with self.subTest(meta=meta), self.assertRaises(RuntimeError):
                local.LocalClient("alias").response([], TOOL_SCHEMAS)
        self.assertFalse(any(row[0] == "/api/chat" for row in self.seen))
        for model in ["model:cloud", "https://example.com/model", "../model", "a\nmodel"]:
            with self.assertRaises(ValueError):
                local.LocalClient(model)

    def test_stop_interrupts_waiting_inference_without_executing_a_tool(self):
        self.delay, self.replies = True, [action()]
        cancel = threading.Event()
        errors = []
        def run():
            try:
                local.LocalClient("qwen3:4b", cancel).response([], TOOL_SCHEMAS)
            except Exception as exc:
                errors.append(exc)
        worker = threading.Thread(target=run)
        worker.start()
        self.assertTrue(self.started.wait(2))
        start = time.monotonic()
        cancel.set()
        worker.join(1.5)
        self.assertFalse(worker.is_alive())
        self.assertLess(time.monotonic() - start, 1.5)
        self.assertIsInstance(errors[0], Cancelled)

    def test_discovery_filters_remote_models_and_download_has_explicit_starter_allowlist(self):
        transport = local.LocalTransport()
        self.assertEqual([row["slug"] for row in local.installed_models(transport)], ["qwen3:4b"])
        local.pull_starter(transport, "qwen3:4b", lambda *args: None)
        with self.assertRaises(ValueError):
            local.pull_starter(transport, "other:model", lambda *args: None)


class LocalModeTests(unittest.TestCase):
    def test_fresh_config_defaults_to_local_and_existing_choice_is_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            config = settings.load_config(root)
            self.assertEqual(config["auth_mode"], "local")
            config["local_model"] = "qwen3:1.7b"
            settings.save_config(root, config)
            self.assertEqual(settings.load_config(root)["local_model"], "qwen3:1.7b")
            config["auth_mode"] = "chatgpt"
            settings.save_config(root, config)
            self.assertEqual(settings.load_config(root)["auth_mode"], "chatgpt")

    def test_engine_launch_is_owned_loopback_only_and_disables_cloud(self):
        with tempfile.TemporaryDirectory() as folder:
            process = Mock()
            process.poll.return_value = None
            engine = local.LocalEngine(folder)
            with patch("local_client.shutil.which", return_value="ollama"), \
                 patch("local_client.socket.create_connection", side_effect=ConnectionRefusedError), \
                 patch("local_client.LocalTransport.request", return_value={"version": "test"}), \
                 patch("local_client.subprocess.Popen", return_value=process) as popen:
                engine.start(threading.Event())
                env = popen.call_args.kwargs["env"]
                self.assertEqual(env["OLLAMA_NO_CLOUD"], "1")
                self.assertEqual(env["OLLAMA_HOST"], "127.0.0.1:11435")
                self.assertEqual(popen.call_args.args[0][-1], "serve")
                self.assertNotIn("shell", popen.call_args.kwargs)
                engine.close()
            process.terminate.assert_called_once()

    def test_local_worker_never_constructs_paid_or_chatgpt_clients(self):
        from app import Application
        with tempfile.TemporaryDirectory() as folder:
            application = Application.__new__(Application)
            application.directory = Path(folder)
            application.config = settings.defaults()
            application.jobs, application.events = queue.Queue(), queue.Queue()
            application.cancel = threading.Event()
            application.jobs.put({"kind": "run", "key": "", "config": application.config, "text": "Hello", "windows": False})
            application.jobs.put({"kind": "shutdown"})
            with patch("app.LocalEngine") as engine, patch("app.LocalClient") as client, \
                 patch("app.ChatGPTClient") as plan, patch("app.OpenAIClient") as paid:
                client.return_value.response.return_value = {"status": "completed", "output": [{"type": "message", "content": [{"type": "output_text", "text": "Hello"}]}]}
                application._work()
                plan.assert_not_called()
                paid.assert_not_called()
                engine.return_value.close.assert_called_once()
            self.assertIn(("log", "Assistant", "Hello"), list(application.events.queue))


if __name__ == "__main__":
    unittest.main()
