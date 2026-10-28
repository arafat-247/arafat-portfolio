import asyncio
import io
import json
import os
from pathlib import Path
import struct
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from browser_driver import ThreadedPipeTransport, read_exactly, start_playwright
    from runtime import stop_playwright
    AVAILABLE = True
except ImportError:
    AVAILABLE = False


@unittest.skipUnless(AVAILABLE, "Playwright is not installed")
class DriverTests(unittest.TestCase):
    def test_short_reads_are_assembled_and_incomplete_frames_rejected(self):
        class Short(io.BytesIO):
            def read(self, size):
                return super().read(min(size, 2))
        self.assertEqual(read_exactly(Short(b"abcdef"), 6), b"abcdef")
        with self.assertRaises(EOFError):
            read_exactly(Short(b"abc"), 4)

    def test_native_child_pipe_preserves_bangla_and_callbacks_stay_on_owner_thread(self):
        with tempfile.TemporaryDirectory() as folder:
            script = Path(folder) / "echo_driver.py"
            script.write_text("""import sys,struct
incoming,outgoing=sys.stdin.buffer,sys.stdout.buffer
while True:
    header=incoming.read(4)
    if not header: break
    size=struct.unpack('<I',header)[0]
    payload=incoming.read(size)
    outgoing.write(struct.pack('<I',len(payload))+payload)
    outgoing.flush()
""", encoding="utf-8")
            loop = asyncio.new_event_loop()
            transport = ThreadedPipeTransport(loop)
            owner = threading.get_ident()
            received = []
            def on_message(value):
                self.assertEqual(threading.get_ident(), owner)
                received.append(value)
                transport.request_stop()
            transport.on_message = on_message
            try:
                with patch("browser_driver.compute_driver_executable", return_value=(sys.executable, str(script))), \
                     patch("browser_driver.get_driver_env", return_value=dict(os.environ)):
                    loop.run_until_complete(transport.connect())
                transport.send({"id": 1, "instruction": "বাংলায় লিখুন"})
                loop.run_until_complete(asyncio.wait_for(transport.run(), timeout=10))
                loop.run_until_complete(transport.wait_until_stopped())
                self.assertEqual(received, [{"id": 1, "instruction": "বাংলায় লিখুন"}])
                self.assertEqual(transport._proc.poll(), 0)
                self.assertFalse(transport._reader.is_alive())
            finally:
                loop.close()

    def test_real_sdk_handshake_and_shutdown_use_the_owned_native_pipe(self):
        p = start_playwright()
        transport = p._impl_obj._connection._transport
        loop = p._impl_obj._connection._loop
        self.assertIsInstance(transport, ThreadedPipeTransport)
        try:
            self.assertEqual(p.chromium.name, "chromium")
        finally:
            self.assertFalse(stop_playwright(p))
        self.assertEqual(transport._proc.poll(), 0)
        self.assertFalse(transport._reader.is_alive())
        self.assertTrue(loop.is_closed())


if __name__ == "__main__":
    unittest.main()
