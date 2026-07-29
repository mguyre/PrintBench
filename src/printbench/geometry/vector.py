from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Vector:
    """Represents a displacement in 2D space."""

    x: float
    y: float
