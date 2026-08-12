from __future__ import annotations

from dataclasses import dataclass

from printbench.style import Style

from .point import Point


@dataclass(frozen=True, slots=True)
class Dot:
    """
    A circular dot with a solid fill and no stroke expressed in millimeters.
    """

    center: Point
    diameter: float
    style: Style | None = None

    def __post_init__(self) -> None:
        if self.diameter <= 0:
            raise ValueError("diameter must be greater than zero")
