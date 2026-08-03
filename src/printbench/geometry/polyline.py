from __future__ import annotations

from dataclasses import dataclass

from printbench.style import Style

from .point import Point


@dataclass(frozen=True, slots=True)
class Polyline:
    """an object made up of a list of connected points"""

    points: tuple[Point, ...]
    style: Style | None = None

    def __post_init__(self) -> None:
        if len(self.points) < 2:
            raise ValueError("polyline must contain at least two points")
