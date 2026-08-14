from dataclasses import FrozenInstanceError

import pytest

from printbench import Point, Polyline
from printbench.style import StrokeStyle, Style


def test_polyline_stores_values() -> None:
    points = (
        Point(12.3, 45.6),
        Point(78.9, 101.2),
        Point(123.4, 56.7),
    )
    style = Style(
        stroke_color="blanchedalmond",
        stroke_width=1.234,
        stroke_style=StrokeStyle.DASHED,
    )

    polyline = Polyline(
        points=points,
        style=style,
    )

    assert polyline.points == points
    assert polyline.style == style


def test_polyline_is_immutable() -> None:
    polyline = Polyline(
        points=(
            Point(12.3, 45.6),
            Point(78.9, 101.2),
            Point(123.4, 56.7),
        ),
    )

    with pytest.raises(FrozenInstanceError):
        polyline.points = (
            Point(98.7, 65.4),
            Point(32.1, 10.9),
        )


@pytest.mark.parametrize(
    "points",
    [
        (),
        (Point(12.3, 45.6),),
    ],
)
def test_polyline_rejects_fewer_than_two_points(
    points: tuple[Point, ...],
) -> None:
    with pytest.raises(ValueError):
        Polyline(points=points)
