"""
Line geometry.

Represents a directed line segment between two Points.

A Line derives its behavior from the relationship between
its endpoints rather than duplicating geometric calculations.
"""

from __future__ import annotations

from dataclasses import dataclass

from printbench.style import Style

from .point import Point
from .vector import Vector


@dataclass(frozen=True, slots=True)
class Line:
    start: Point
    end: Point
    style: Style | None = None

    def vector(self) -> Vector:
        """Return the displacement from start to end."""
        return self.end - self.start

    def length(self) -> float:
        return self.vector().length()

    def direction(self) -> Vector:
        return self.vector().normalized()

    def midpoint(self) -> Point:
        return self.start + self.vector() / 2


def center_mark(
    center: Point,
    size: float,
    style: Style | None = None,
) -> tuple[Line, Line]:
    """Create horizontal and vertical lines centered on a point."""

    if size <= 0:
        raise ValueError("size must be greater than zero")

    half_size = size / 2.0

    horizontal = Line(
        start=Point(
            center.x - half_size,
            center.y,
        ),
        end=Point(
            center.x + half_size,
            center.y,
        ),
        style=style,
    )

    vertical = Line(
        start=Point(
            center.x,
            center.y - half_size,
        ),
        end=Point(
            center.x,
            center.y + half_size,
        ),
        style=style,
    )

    return horizontal, vertical
