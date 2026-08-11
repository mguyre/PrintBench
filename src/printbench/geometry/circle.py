from __future__ import annotations

from dataclasses import dataclass

from printbench.style import Style

from .closed_shape import ClosedShape
from .point import Point


@dataclass(frozen=True, slots=True)
class Circle(ClosedShape):
    """A circle defined by a center point and radius."""

    center: Point
    radius: float
    style: Style | None = None

    def __post_init__(self) -> None:
        if self.radius <= 0:
            raise ValueError("radius must be greater than zero")
