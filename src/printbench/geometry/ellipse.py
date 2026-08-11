from __future__ import annotations

from dataclasses import dataclass

from printbench.style import Style

from .closed_shape import ClosedShape
from .point import Point


@dataclass(frozen=True, slots=True)
class Ellipse(ClosedShape):
    """An ellipse defined by a center point and two radii."""

    center: Point
    radius_x: float
    radius_y: float
    style: Style | None = None

    def __post_init__(self) -> None:
        if self.radius_x <= 0:
            raise ValueError("radius_x must be greater than zero")
        if self.radius_y <= 0:
            raise ValueError("radius_y must be greater than zero")
