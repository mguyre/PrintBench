from __future__ import annotations

from dataclasses import dataclass

from printbench.style import Style

from .closed_shape import ClosedShape
from .point import Point


@dataclass(frozen=True, slots=True)
class Rectangle(ClosedShape):
    """A rectangle defined by its bottom-left corner, width, and height."""

    bottom_left: Point
    width: float
    height: float
    style: Style | None = None

    def __post_init__(self) -> None:
        if self.width <= 0:
            raise ValueError("width must be greater than zero")

        if self.height <= 0:
            raise ValueError("height must be greater than zero")
