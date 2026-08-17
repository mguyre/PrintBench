from __future__ import annotations

from dataclasses import dataclass

from printbench.geometry.point import Point
from printbench.style import Style


@dataclass(frozen=True, slots=True)
class Text:
    """Text positioned in Cartesian coordinates."""

    bottom_left: Point
    text: str
    font_size: float
    style: Style | None = None

    def __post_init__(self) -> None:
        if not self.text:
            raise ValueError("text must not be empty")

        if self.font_size <= 0:
            raise ValueError("font_size must be positive")
