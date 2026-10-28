"""Own the Playwright driver's pipes without Windows asyncio process waiters.

The SDK's protocol and browser APIs remain unchanged. Only its pinned local
transport is replaced; callbacks still execute on the SDK's event-loop thread.
"""
from __future__ import annotations

import asyncio
import os
import struct
import subprocess
import sys
import threading

from playwright._impl._driver import compute_driver_executable, get_driver_env
from playwright._impl._transport import Transport

_start_lock = threading.Lock()


def read_exactly(stream, length):
    parts = []
    while length:
        part = stream.read(length)
        if not part:
            raise EOFError("The browser driver pipe closed.")
        parts.append(part)
        length -= len(part)
    return b"".join(parts)


class ThreadedPipeTransport(Transport):
    _arafat_threaded_driver = True

    def __init__(self, loop):
        super().__init__(loop)
        self._queue = asyncio.Queue()
        self._stopped = False
        self._proc = None
        self._reader = None
        self._stopped_future = loop.create_future()

    async def connect(self):
        executable, script = compute_driver_executable()
        env = get_driver_env()
        if getattr(sys, "frozen", False):
            env.setdefault("PLAYWRIGHT_BROWSERS_PATH", "0")
        startupinfo = None
        if sys.platform == "win32":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
        try:
            self._proc = subprocess.Popen([str(executable), str(script), "run-driver"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                env=env, startupinfo=startupinfo)
        except Exception as exc:
            if not self.on_error_future.done():
                self.on_error_future.set_exception(exc)
            raise
        self._reader = threading.Thread(target=self._read, name="assistant-browser-pipe", daemon=True)
        self._reader.start()

    def _offer(self, value):
        if not self._stopped and not self._loop.is_closed():
            try:
                self._loop.call_soon_threadsafe(self._queue.put_nowait, value)
            except RuntimeError:
                pass

    def _read(self):
        try:
            while not self._stopped:
                length = struct.unpack("<I", read_exactly(self._proc.stdout, 4))[0]
                if length > 32_000_000:
                    raise ValueError("The browser driver message exceeded the size limit.")
                message = self.deserialize_message(read_exactly(self._proc.stdout, length))
                self._offer(message)
        except EOFError:
            self._offer(None)
        except Exception as exc:
            self._offer(exc)

    def request_stop(self):
        if self._stopped:
            return
        self._stopped = True
        if self._proc and self._proc.stdin:
            try:
                self._proc.stdin.close()
            except OSError:
                pass  # A driver that already exited may have closed its pipe.
        # Called by the SDK on its owner thread. No cross-thread wakeup is
        # needed to release the protocol dispatcher during shutdown.
        self._queue.put_nowait(None)

    async def wait_until_stopped(self):
        await self._stopped_future

    def _close_owned_process(self):
        if not self._proc:
            return
        try:
            self._proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self._proc.terminate()
            self._proc.wait(timeout=5)
        if self._reader:
            self._reader.join(timeout=2)
            if self._reader.is_alive():
                raise RuntimeError("The owned browser protocol reader did not close.")
        if self._proc.stdout:
            self._proc.stdout.close()

    async def run(self):
        try:
            while not self._stopped:
                message = await self._queue.get()
                if message is None:
                    if not self._stopped and not self.on_error_future.done():
                        self.on_error_future.set_exception(RuntimeError("The browser driver closed unexpectedly."))
                    break
                if isinstance(message, Exception):
                    raise message
                self.on_message(message)
                await asyncio.sleep(0)
        finally:
            self.request_stop()
            try:
                self._close_owned_process()
            finally:
                if not self._stopped_future.done():
                    self._stopped_future.set_result(None)

    def send(self, message):
        if self._stopped or not self._proc:
            raise RuntimeError("The browser driver is closed.")
        data = self.serialize_message(message)
        self._proc.stdin.write(struct.pack("<I", len(data)) + data)
        self._proc.stdin.flush()


def start_playwright():
    # The application creates one SDK instance on its worker thread. Patch only
    # construction, then immediately restore the SDK module's original class.
    import playwright.sync_api._context_manager as context
    with _start_lock:
        original = context.PipeTransport
        context.PipeTransport = ThreadedPipeTransport
        try:
            return context.PlaywrightContextManager().start()
        finally:
            context.PipeTransport = original
