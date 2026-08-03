"""
Vector geometry.

Represents a displacement in Cartesian space.

A Vector has magnitude and direction but no fixed location.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Vector:
    """Represents a displacement in 2D space."""

    # the starting point is implied a (0,0)

    x: float
    y: float

    # ----------------------------------------------------------------------
    # Arithmetic Operators
    # ----------------------------------------------------------------------
    def __add__(self, other: Vector) -> Vector:
        """Return the sum of two vectors."""

        if not isinstance(other, Vector):
            return NotImplemented

        return Vector(
            self.x + other.x,
            self.y + other.y,
        )

    def __sub__(self, other: object) -> Vector:
        """Return the difference between two vectors."""

        if not isinstance(other, Vector):
            return NotImplemented

        return Vector(
            self.x - other.x,
            self.y - other.y,
        )

    def __mul__(self, scalar: object) -> Vector:
        """Scale a vector."""

        if not isinstance(scalar, (int, float)):
            return NotImplemented

        return Vector(
            self.x * scalar,
            self.y * scalar,
        )

    def __rmul__(self, scalar: float) -> Vector:
        """Scale a vector."""

        return self * scalar

    def __truediv__(self, scalar: object) -> Vector:
        """Divide a vector by a scalar."""

        if not isinstance(scalar, (int, float)):
            return NotImplemented

        return Vector(
            self.x / scalar,
            self.y / scalar,
        )

    # ----------------------------------------------------------------------
    # Geometric Operations
    # ----------------------------------------------------------------------
    def length(self) -> float:
        """Return the Euclidean length of the vector."""
        return math.hypot(self.x, self.y)

    def length_squared(self) -> float:
        """Return the squared Euclidean length of the vector."""
        return self.x * self.x + self.y * self.y

    # ----------------------------------------------------------------------
    # Utility Methods
    # ----------------------------------------------------------------------
    def normalized(self) -> Vector:
        """Return a unit vector with the same direction."""

        length = self.length()

        if length == 0:
            raise ValueError("Cannot normalize a zero-length vector.")

        return Vector(
            self.x / length,
            self.y / length,
        )

    def dot(self, other: Vector) -> float:
        """a · b == b · a"""
        return self.x * other.x + self.y * other.y
