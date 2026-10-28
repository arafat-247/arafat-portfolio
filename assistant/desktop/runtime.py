"""Restore system DLL lookup while a frozen Windows app launches children.

PyInstaller documents that its DLL search directory is inherited by external
programs. Node, Edge and normal Windows applications need their system lookup.
"""
from contextlib import contextmanager
import os
import sys
import threading
import subprocess

_lock = threading.RLock()


def stop_playwright(playwright, grace_seconds=3.0):
    """Close the SDK; bound an unresponsive driver using its owned process handle.

    The transport layout is checked against the pinned Playwright version.
    Termination uses the retained Popen handle, never a guessed process ID.
    """
    process = None
    process_transport = None
    loop = None
    try:
        connection = playwright._impl_obj._connection
        candidate_transport = connection._transport._proc._transport
        candidate = candidate_transport._proc
        if isinstance(candidate, subprocess.Popen):
            process = candidate
            process_transport = candidate_transport
            loop = getattr(connection, "_loop", None)
    except AttributeError:
        pass
    forced = threading.Event()

    def end_owned_driver():
        if process is not None:
            try:
                if process.poll() is None:
                    process.terminate()
                    forced.set()
            except OSError:
                pass
        # An exited driver can still leave an inherited stdout pipe open.
        # Close only this driver's asyncio transport, on its owning loop.
        if process_transport is not None and loop is not None and not loop.is_closed():
            close = getattr(process_transport, "close", None)
            if close:
                try:
                    loop.call_soon_threadsafe(close)
                    forced.set()
                except RuntimeError:
                    pass

    timer = threading.Timer(grace_seconds, end_owned_driver)
    timer.daemon = True
    timer.start()
    try:
        playwright.stop()
    except Exception:
        end_owned_driver()
        raise
    finally:
        timer.cancel()
        timer.join(timeout=1)
    return forced.is_set()


@contextmanager
def external_program_environment():
    if sys.platform != "win32" or not getattr(sys, "frozen", False):
        yield
        return
    import ctypes
    from ctypes import wintypes
    with _lock:
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.GetDllDirectoryW.argtypes = [wintypes.DWORD, wintypes.LPWSTR]
        kernel.GetDllDirectoryW.restype = wintypes.DWORD
        kernel.SetDllDirectoryW.argtypes = [wintypes.LPCWSTR]
        kernel.SetDllDirectoryW.restype = wintypes.BOOL
        size = kernel.GetDllDirectoryW(0, None)
        buffer = ctypes.create_unicode_buffer(size + 1)
        kernel.GetDllDirectoryW(len(buffer), buffer)
        previous_directory = buffer.value or None
        previous_path = os.environ.get("PATH")
        base = os.path.normcase(os.path.abspath(sys._MEIPASS))
        parts = []
        for value in (previous_path or "").split(os.pathsep):
            normal = os.path.normcase(os.path.abspath(value.strip('"'))) if value else ""
            if normal != base and not normal.startswith(base + os.sep):
                parts.append(value)
        if not kernel.SetDllDirectoryW(None):
            raise ctypes.WinError(ctypes.get_last_error())
        os.environ["PATH"] = os.pathsep.join(parts)
        try:
            yield
        finally:
            if previous_path is None:
                os.environ.pop("PATH", None)
            else:
                os.environ["PATH"] = previous_path
            if not kernel.SetDllDirectoryW(previous_directory):
                raise ctypes.WinError(ctypes.get_last_error())
