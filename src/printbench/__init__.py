"""
PrintBench

A framework for generating and analyzing print characterization targets.
"""

from .document import ClipContainer, Document
from .geometry import (
    Circle,
    ClosedShape,
    Dot,
    Ellipse,
    Line,
    Point,
    Polygon,
    Polyline,
    Raster,
    Rectangle,
    Vector,
    center_mark,
    circumscribed_regular_polygon,
    inscribed_regular_polygon,
)
from .renderers import SvgRenderer
from .style import StrokeStyle, Style

__version__ = "0.2.0"

__all__ = [
    "Circle",
    "ClipContainer",
    "ClosedShape",
    "Document",
    "Dot",
    "Ellipse",
    "Line",
    "Point",
    "Polygon",
    "Polyline",
    "Raster",
    "Rectangle",
    "StrokeStyle",
    "Style",
    "SvgRenderer",
    "Vector",
    "center_mark",
    "circumscribed_regular_polygon",
    "inscribed_regular_polygon",
]
