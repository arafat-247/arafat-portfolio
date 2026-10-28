"""Restore system DLL lookup while a frozen Windows app launches children.

PyInstaller documents that its DLL search directory is inherited by external
programs. Node, Edge and normal Windows applications need their system lookup.
"""
from contextlib import contextmanager
import os
import sys
import threading
import subprocess
import asyncio

_lock = threading.RLock()


@contextmanager
def single_instance(directory):
    """Keep two copies from racing a rotating OAuth refresh token."""
    if sys.platform != "win32":
        yield True
        return
    import ctypes
    import hashlib
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.CreateMutexW.argtypes = [ctypes.c_void_p, ctypes.c_bool, ctypes.c_wchar_p]
    kernel.CreateMutexW.restype = ctypes.c_void_p
    kernel.ReleaseMutex.argtypes = [ctypes.c_void_p]
    kernel.CloseHandle.argtypes = [ctypes.c_void_p]
    name = "Local\\ArafatAssistant-" + hashlib.sha256(str(directory).casefold().encode()).hexdigest()[:32]
    handle = kernel.CreateMutexW(None, True, name)
    if not handle:
        raise RuntimeError("Could not create the assistant's instance lock.")
    owned = ctypes.get_last_error() != 183
    try:
        yield owned
    finally:
        if owned:
            kernel.ReleaseMutex(handle)
        kernel.CloseHandle(handle)


def stop_playwright(playwright, grace_seconds=3.0, observe=None):
    """Close the SDK; bound an unresponsive driver using its owned process handle.

    The transport layout is checked against the pinned Playwright version.
    Termination uses the retained Popen handle, never a guessed process ID.
    """
    process = None
    process_transport = None
    loop = None
    sdk_process = None
    try:
        connection = playwright._impl_obj._connection
        sdk_process = connection._transport._proc
        candidate_transport = sdk_process._transport
        process_transport = candidate_transport
        loop = getattr(connection, "_loop", None)
        candidate = candidate_transport._proc
        if isinstance(candidate, subprocess.Popen):
            process = candidate
    except AttributeError:
        pass
    forced = threading.Event()
    original_communicate = getattr(sdk_process, "communicate", None)

    def close_exited_driver_pipes():
        if process_transport is not None:
            process_transport.close()
        if sdk_process is not None:
            for name in ("stdout", "stderr"):
                reader = getattr(sdk_process, name, None)
                if isinstance(reader, asyncio.StreamReader):
                    reader.feed_eof()

    if original_communicate is not None and process is not None:
        async def bounded_communicate(*args, **kwargs):
            # PipeTransport.run drains Process.communicate after request_stop.
            # Windows can retain an unresolved pipe waiter after the driver
            # exits. Its protocol output is no longer used during shutdown.
            if process.poll() is not None:
                close_exited_driver_pipes()
                forced.set()
                return None, None
            try:
                return await asyncio.wait_for(original_communicate(*args, **kwargs), timeout=grace_seconds)
            except asyncio.TimeoutError:
                if process.poll() is not None:
                    close_exited_driver_pipes()
                    forced.set()
                    return None, None
                raise
        sdk_process.communicate = bounded_communicate

    def diagnostic(stage):
        if observe:
            observe({"stage": stage, "owned_process_handle": process is not None,
                     "owned_transport": process_transport is not None,
                     "loop_present": loop is not None,
                     "process_returncode": process.poll() if process is not None else None})

    diagnostic("before driver stop")

    def end_owned_driver():
        diagnostic("driver shutdown grace elapsed")
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
                def finish_owned_pipes():
                    # On Windows a closed proactor transport can leave its
                    # StreamReader waiting despite the driver already exiting.
                    # Feed EOF only to that exited driver's retained readers.
                    exited = process is not None and process.poll() is not None
                    if exited and sdk_process is not None:
                        close_exited_driver_pipes()
                    else:
                        close()
                    diagnostic("owned driver pipes closed")
                try:
                    loop.call_soon_threadsafe(finish_owned_pipes)
                    forced.set()
                except RuntimeError:
                    pass
        diagnostic("owned driver cleanup requested")

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
        if original_communicate is not None:
            sdk_process.communicate = original_communicate
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
