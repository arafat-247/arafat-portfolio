"""Restore system DLL lookup while a frozen Windows app launches children.

PyInstaller documents that its DLL search directory is inherited by external
programs. Node, Edge and normal Windows applications need their system lookup.
"""
from contextlib import contextmanager
import os
import sys
import threading

_lock = threading.RLock()


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
