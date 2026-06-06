"""ByakuganVisualizer package."""

from __future__ import annotations

try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:  # pragma: no cover
    from importlib_metadata import PackageNotFoundError, version

try:
    __version__ = version("ByakuganVisualizer")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

from byakuganvisualizer.processor import ByakuganProcessor

__all__ = ["ByakuganProcessor", "__version__"]
