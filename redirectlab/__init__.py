"""Bounded teaching API: parse UTF8 JSON bytes, evaluate full native declarations."""

from .contracts import Invalid, parse
from .model import evaluate

__all__ = ["Invalid", "parse", "evaluate"]
