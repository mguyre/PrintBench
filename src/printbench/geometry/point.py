from __future__ import annotations

from dataclasses import dataclass
from typing import overload

from .vector import Vector


@dataclass(frozen=True, slots=True)
class Point:
    """
    A two-dimensional point expressed in millimeters.

    The PrintBench geometry engine uses millimeters as its
    internal unit of measure.
    """

    x: float
    y: float

    @overload
    def __sub__(self, other: Point) -> Vector: ...

    @overload
    def __sub__(self, other: Vector) -> Point: ...

    def __sub__(self, other):
        if isinstance(other, Point):
            return Vector(
                self.x - other.x,
                self.y - other.y,
            )
        if isinstance(other, Vector):
            return Point(
                self.x - other.x,
                self.y - other.y,
            )
        return NotImplemented

    def __add__(self, other: object) -> Point:
        if not isinstance(other, Vector):
            return NotImplemented
        return Point(
            self.x + other.x,
            self.y + other.y,
        )

    def distance_to(self, other: Point) -> float:
        """Return the Euclidean distance to another point."""

        return (other - self).length()
