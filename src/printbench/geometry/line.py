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
