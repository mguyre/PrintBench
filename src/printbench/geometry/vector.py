from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Vector:
    """Represents a displacement in 2D space."""

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

    def __sub__(self, other: Vector) -> Vector:
        """Return the difference between two vectors."""

        if not isinstance(other, Vector):
            return NotImplemented

        return Vector(
            self.x - other.x,
            self.y - other.y,
        )

    def __mul__(self, scalar: float) -> Vector:
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

    def __truediv__(self, scalar: float) -> Vector:
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

    # ----------------------------------------------------------------------
    # Utility Methods
    # ----------------------------------------------------------------------
