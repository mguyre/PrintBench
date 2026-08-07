"""
PrintBench

A framework for generating and analyzing print characterization targets.
"""

from .document import Document
from .geometry import Circle, Line, Point, Vector
from .renderers import SvgRenderer
from .style import StrokeStyle, Style

__version__ = "0.1.0"

__all__ = [
    "Circle",
    "Document",
    "Line",
    "Point",
    "StrokeStyle",
    "Style",
    "SvgRenderer",
    "Vector",
]
