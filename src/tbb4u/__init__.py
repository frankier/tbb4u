"""tbb4u: wheels for oneAPI Thread Building Blocks (oneTBB).

This distribution bundles the oneTBB shared libraries (tbb, tbbmalloc)
built from the official uxlfoundation/oneTBB sources. Wheels are tagged
py3-none-<platform>: they are independent of the Python version and ABI.
"""

from __future__ import annotations

import ctypes
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

__all__ = ["__version__", "library_path", "load"]

try:
    __version__ = version("tbb4u")
except PackageNotFoundError:  # not installed, e.g. running from a source tree
    __version__ = "0.0.0"


def library_path() -> Path:
    """Directory containing the bundled oneTBB shared libraries."""
    return Path(__file__).resolve().parent


_LIB_NAMES = {
    "win32": ["tbb12.dll"],
    "darwin": ["libtbb.12.dylib", "libtbb.dylib"],
    "linux": ["libtbb.so.12", "libtbb.so"],
}


def load():
    """Load the bundled oneTBB runtime and return the ctypes handle.

    Raises OSError if no matching library can be loaded.
    """
    candidates = _LIB_NAMES.get(sys.platform, [])
    errors = []
    for name in candidates:
        try:
            return ctypes.CDLL(str(library_path() / name))
        except OSError as exc:
            errors.append(f"{name}: {exc}")
    raise OSError(
        "Could not load the bundled oneTBB library. Tried: "
        + "; ".join(errors)
    )
