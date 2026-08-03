from __future__ import annotations

import math
from dataclasses import dataclass

from printbench.style import Style

from .point import Point


@dataclass(frozen=True, slots=True)
class Polygon:
    """a closed object made up of a list of connected points"""

    points: tuple[Point, ...]
    style: Style | None = None

    def __post_init__(self) -> None:
        if len(self.points) < 3:
            raise ValueError("polygon must contain at least three points")


def inscribed_regular_polygon(
    center: Point,
    circumradius: float,
    sides: int,
    rotation: float = 0.0,
    style: Style | None = None,
) -> Polygon:
    """Creates a closed polygon of n equal sides where the points fall on the circle"""

    if sides < 3:
        raise ValueError("regular polygon must have at least three sides")
    if circumradius <= 0:
        raise ValueError("circumradius must be greater than zero")

    points = []

    angle_step = 2.0 * math.pi / sides
    rotation_radians = math.radians(rotation)

    for index in range(sides):
        angle = rotation_radians + index * angle_step

        points.append(
            Point(
                center.x + circumradius * math.cos(angle),
                center.y + circumradius * math.sin(angle),
            )
        )

    return Polygon(
        points=tuple(points),
        style=style,
    )


def circumscribed_regular_polygon(
    center: Point,
    inradius: float,
    sides: int,
    rotation: float = 0.0,
    style: Style | None = None,
) -> Polygon:
    """Creates a closed polygon of n equal sides where the midpoints of the sides are tangent to the circle"""
    circumradius = inradius / math.cos(math.pi / sides)

    return inscribed_regular_polygon(
        center=center,
        circumradius=circumradius,
        sides=sides,
        rotation=rotation,
        style=style,
    )
