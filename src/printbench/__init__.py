"""
PrintBench

A framework for generating and analyzing print characterization targets.
"""

from .document import Document
from .geometry import Circle, Ellipse, Line, Point, Rectangle, Vector
from .renderers import SvgRenderer
from .style import StrokeStyle, Style

__version__ = "0.1.0"

__all__ = [
    "Circle",
    "Document",
    "Ellipse",
    "Line",
    "Point",
    "Rectangle",
    "StrokeStyle",
    "Style",
    "SvgRenderer",
    "Vector",
]
