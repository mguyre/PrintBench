from __future__ import annotations

from dataclasses import dataclass

from .point import Point
from .vector import Vector


@dataclass(frozen=True, slots=True)
class Line:
    start: Point
    end: Point

    def vector(self) -> Vector:
        """Return the displacement from start to end."""
        return self.end - self.start

    def length(self) -> float:
        return self.vector().length()

    def direction(self) -> Vector:
        return self.vector().normalized()

    def midpoint(self) -> Point:
        return self.start + self.vector() / 2
