from __future__ import annotations

from dataclasses import dataclass

from .point import Point
from .vector import Vector


@dataclass(frozen=True, slots=True)
class Line:
    start: Point
    end: Point

    def length(self) -> float:
        return self.start.distance_to(self.end)

    def direction(self) -> Vector:
        return (self.end - self.start).normalized()

    def midpoint(self) -> Point:
        return self.start + (self.end - self.start) / 2
