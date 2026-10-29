"""Opt-in live local inference, with real approved note output and no OpenAI."""
import argparse
import json
from pathlib import Path
import tempfile
import threading

from automation import Tools
from core import Agent
from local_client import LocalClient, LocalEngine, LocalTransport, pull_starter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="qwen3:1.7b")
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    report = {"ok": False, "model": args.model, "openai_used": False, "checks": []}
    cancel = threading.Event()
    with tempfile.TemporaryDirectory(prefix="assistant-live-local-") as folder:
        root = Path(folder)
        engine = LocalEngine(root)
        try:
            engine.start(cancel)
            pull_starter(LocalTransport(cancel), args.model, lambda *items: print(*items, flush=True))
            client = LocalClient(args.model, cancel)
            tools = Tools(root / "browser", root / "notes", {}, lambda *items: True, lambda *items: None)
            try:
                reply = Agent(client, tools, lambda *items: print(*items, flush=True)).run(
                    "Use save_note exactly once. filename: local-check. content: Hello, Arafat. বাংলা পরীক্ষা। Then confirm the saved note.", cancel)
                files = list((root / "notes").glob("*.txt"))
                assert len(files) == 1, "Expected exactly one real saved note"
                content = files[0].read_text(encoding="utf-8")
                assert "Hello, Arafat." in content and "বাংলা পরীক্ষা" in content, "Model did not preserve requested content"
                assert reply.strip(), "Model did not produce a final answer"
                report["checks"].append("Real local model invoked approved save_note, wrote English/Bangla and returned an answer")
                result = client.response([{"role": "user", "content": "বাংলায় এক বাক্যে বলো তুমি কী করতে পারো। কোনও টুল ব্যবহার করো না।"}], [])
                text = " ".join(p["text"] for item in result["output"] if item["type"] == "message" for p in item["content"])
                assert any("\u0980" <= c <= "\u09ff" for c in text), "Expected a Bangla reply"
                report["checks"].append("Real local model returned Bangla text")
                report["bangla_reply"] = text
                report["ok"] = True
            finally:
                tools.close()
        finally:
            engine.close()
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
