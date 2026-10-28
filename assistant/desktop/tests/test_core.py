import array
import io
import json
import queue
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
import wave

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from automation import Tools
from core import Agent, Cancelled, Declined, OpenAIClient, valid_url, write_note
import settings
from voice import Recorder


def message(text):
    return {"status": "completed", "output": [{"type": "message", "role": "assistant",
            "content": [{"type": "output_text", "text": text}]}]}


def call(name, args):
    return {"status": "completed", "output": [{"type": "function_call", "name": name,
            "arguments": json.dumps(args, ensure_ascii=False), "call_id": "call_1"}]}


class FakeClient:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.requests = []

    def response(self, items, tools):
        self.requests.append(list(items))
        return next(self.responses)


class CoreTests(unittest.TestCase):
    def test_rejects_unsupported_urls_and_credentials(self):
        for url in ("file:///C:/secret.txt", "javascript:alert(1)", "https://user:pass@example.com/",
                    "http://127.0.0.1/", "http://localhost/", "http://10.1.2.3/",
                    "http://[::1]/", "http://0177.0.0.1/", "http://2130706433/", "http://0x7f000001/"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                valid_url(url)
        self.assertEqual(valid_url("https://www.thedailystar.net/"), "https://www.thedailystar.net/")

    def test_notes_preserve_bangla_avoid_traversal_and_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            first = Path(write_note(folder, "../বাংলা/CON", "বাংলায় লিখুন।"))
            second = Path(write_note(folder, "../বাংলা/CON", "Second"))
            self.assertEqual(first.parent, folder)
            self.assertNotEqual(first, second)
            self.assertEqual(first.read_text(encoding="utf-8"), "বাংলায় লিখুন।")
            self.assertNotEqual(Path(write_note(folder, "CON", "x")).stem.upper(), "CON")

    def test_settings_do_not_store_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            config = settings.defaults()
            config["api_key"] = "SECRET-MUST-NOT-BE-SAVED"
            settings.save_config(directory, config)
            self.assertNotIn("SECRET", (directory / "settings.json").read_text())
            self.assertEqual(settings.load_config(directory)["model"], config["model"])

    def test_response_wire_format_uses_stateless_responses(self):
        client = OpenAIClient("dummy")
        with patch.object(client, "_post", return_value=message("হ্যাঁ")) as post:
            client.response([{"role": "user", "content": "বাংলায় বলুন"}], [])
        endpoint, data, content_type = post.call_args.args
        payload = json.loads(data)
        self.assertEqual(endpoint, "/responses")
        self.assertFalse(payload["store"])
        self.assertIn("reasoning.encrypted_content", payload["include"])
        self.assertEqual(payload["input"][0]["content"], "বাংলায় বলুন")

    def test_transcription_multipart_and_multilingual_hints(self):
        client = OpenAIClient("dummy")
        with patch.object(client, "_post", return_value={"text": "ওয়েবসাইট খুলুন"}) as post:
            text = client.transcribe(b"RIFF-audio", ["en", "bn"])
        endpoint, body, content_type = post.call_args.args
        self.assertEqual(endpoint, "/audio/transcriptions")
        self.assertEqual(body.count(b'name="languages[]"'), 2)
        self.assertNotIn(b'name="language"', body)
        self.assertIn(b"RIFF-audio", body)
        self.assertEqual(text, "ওয়েবসাইট খুলুন")

    def test_agent_executes_and_returns_real_tool_result(self):
        with tempfile.TemporaryDirectory() as tmp:
            tools = Tools(Path(tmp) / "profile", Path(tmp) / "notes", {}, lambda *args: True, lambda *args: None)
            client = FakeClient([call("save_note", {"filename": "বাংলা", "content": "পরীক্ষা"}), message("ফাইল সংরক্ষিত।")])
            agent = Agent(client, tools, lambda *args: None)
            self.assertEqual(agent.run("বাংলায় একটি ফাইল লেখো", threading.Event()), "ফাইল সংরক্ষিত।")
            tool_output = json.loads(client.requests[1][-1]["output"])
            self.assertTrue(tool_output["ok"])
            self.assertEqual(Path(tool_output["result"]["saved_path"]).read_text(encoding="utf-8"), "পরীক্ষা")

    def test_declined_action_stops_before_file_write_or_next_request(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "notes"
            tools = Tools(Path(tmp), folder, {}, lambda *args: False, lambda *args: None)
            client = FakeClient([call("save_note", {"filename": "no", "content": "no"}), message("Should not run")])
            with self.assertRaises(Declined):
                Agent(client, tools, lambda *args: None).run("Save", threading.Event())
            self.assertFalse(folder.exists())
            self.assertEqual(len(client.requests), 1)

    def test_cancel_during_request_prevents_all_tool_execution(self):
        cancel = threading.Event()
        class Client:
            def response(self, items, tools):
                cancel.set()
                return call("save_note", {"filename": "no", "content": "no"})
        class NoTools:
            def execute(self, name, args):
                raise AssertionError("Tool must not run")
        with self.assertRaises(Cancelled):
            Agent(Client(), NoTools(), lambda *args: None).run("Save", cancel)

    def test_unknown_or_extra_tool_arguments_rejected_before_side_effect(self):
        tools = Tools(Path("."), Path("."), {}, lambda *args: True, lambda *args: None)
        with self.assertRaises(ValueError):
            tools.execute("__getattribute__", {"name": "x"})
        with self.assertRaises(ValueError):
            tools.execute("save_note", {"filename": "x", "content": "x", "path": "C:\\Windows"})
        with self.assertRaises(ValueError):
            tools.execute("window_read", {"handle": True})

    def test_audio_is_wav_and_cleared_after_capture(self):
        recorder = Recorder()
        recorder.blocks = [array.array("h", [900, -900] * 8000).tobytes()]
        data = recorder.finish()
        with wave.open(io.BytesIO(data)) as wav:
            self.assertEqual(wav.getnchannels(), 1)
            self.assertEqual(wav.getframerate(), 16_000)
            self.assertEqual(wav.getnframes(), 16_000)
        self.assertEqual(recorder.blocks, [])

    def test_silence_and_capture_errors_do_not_reach_transcription(self):
        for problem in (None, "overflow"):
            recorder = Recorder()
            recorder.problem = problem
            recorder.blocks = [b"\0" * 32_000]
            with self.assertRaises(ValueError):
                recorder.finish()
            self.assertEqual(recorder.blocks, [])

    def test_loop_is_bounded(self):
        class MoreTools:
            def execute(self, name, args):
                return []
        client = FakeClient([call("apps_available", {})] * 30)
        with self.assertRaisesRegex(RuntimeError, "18-step limit"):
            Agent(client, MoreTools(), lambda *args: None).run("Continue", threading.Event())
        self.assertEqual(len(client.requests), 18)

    def test_voice_transcript_is_queued_for_review_without_agent_execution(self):
        from app import Application
        with tempfile.TemporaryDirectory() as tmp:
            app = Application.__new__(Application)
            app.directory = Path(tmp)
            app.config = settings.defaults()
            app.jobs, app.events = queue.Queue(), queue.Queue()
            app.cancel = threading.Event()
            app.jobs.put({"kind": "transcribe", "key": "dummy", "config": app.config,
                          "audio": b"test", "languages": ["bn"]})
            app.jobs.put({"kind": "shutdown"})
            with patch("app.OpenAIClient") as client, patch("app.Agent") as agent:
                client.return_value.transcribe.return_value = "নোটপ্যাড খোলো"
                app._work()
                agent.assert_not_called()
            events = list(app.events.queue)
            self.assertIn(("transcript", "নোটপ্যাড খোলো"), events)
            self.assertIn(("done",), events)
            self.assertIn(("closed",), events)


if __name__ == "__main__":
    unittest.main()
