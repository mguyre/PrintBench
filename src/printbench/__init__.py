"""
PrintBench

A framework for generating and analyzing print characterization targets.
"""

from .document import Document
from .geometry import Line, Point, Vector
from .renderers import SvgRenderer

__version__ = "0.1.0"

__all__ = [
    "Document",
    "Line",
    "Point",
    "SvgRenderer",
    "Vector",
]
