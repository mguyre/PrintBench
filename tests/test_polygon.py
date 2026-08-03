from dataclasses import FrozenInstanceError

import pytest

from printbench import (
    Point,
    Polygon,
    circumscribed_regular_polygon,
    inscribed_regular_polygon,
)
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

    polygon = Polygon(
        points=points,
        style=style,
    )

    assert polygon.points == points
    assert polygon.style == style


def test_polyline_is_immutable() -> None:
    polygon = Polygon(
        points=(
            Point(12.3, 45.6),
            Point(78.9, 101.2),
            Point(123.4, 56.7),
        ),
    )

    with pytest.raises(FrozenInstanceError):
        polygon.points = (
            Point(98.7, 65.4),
            Point(32.1, 10.9),
        )


@pytest.mark.parametrize(
    "points",
    [
        (),
        (Point(12.3, 45.6),),
        (Point(78.9, 98.7),),
    ],
)
def test_polyline_rejects_fewer_than_three_points(
    points: tuple[Point, ...],
) -> None:
    with pytest.raises(ValueError):
        Polygon(points=points)


def test_inscribed_regular_polygon() -> None:
    polygon = inscribed_regular_polygon(
        center=Point(100.0, 200.0),
        circumradius=25.0,
        sides=4,
    )

    expected_points = (
        Point(125.0, 200.0),
        Point(100.0, 225.0),
        Point(75.0, 200.0),
        Point(100.0, 175.0),
    )

    for actual, expected in zip(
        polygon.points,
        expected_points,
        strict=True,
    ):
        assert actual.x == pytest.approx(expected.x)
        assert actual.y == pytest.approx(expected.y)


@pytest.mark.parametrize(
    "sides",
    [0, 1, 2],
)
def test_inscribed_regular_polygon_rejects_fewer_than_three_sides(
    sides: int,
) -> None:
    with pytest.raises(ValueError):
        inscribed_regular_polygon(
            center=Point(12.3, 45.6),
            circumradius=78.9,
            sides=sides,
        )


@pytest.mark.parametrize(
    "circumradius",
    [0.0, -1.234],
)
def test_inscribed_regular_polygon_rejects_non_positive_circumradius(
    circumradius: float,
) -> None:
    with pytest.raises(ValueError):
        inscribed_regular_polygon(
            center=Point(12.3, 45.6),
            circumradius=circumradius,
            sides=6,
        )


def test_inscribed_regular_polygon_applies_rotation() -> None:
    polygon = inscribed_regular_polygon(
        center=Point(100.0, 200.0),
        circumradius=25.0,
        sides=4,
        rotation=90.0,
    )

    expected_points = (
        Point(100.0, 225.0),
        Point(75.0, 200.0),
        Point(100.0, 175.0),
        Point(125.0, 200.0),
    )

    for actual, expected in zip(
        polygon.points,
        expected_points,
        strict=True,
    ):
        assert actual.x == pytest.approx(expected.x)
        assert actual.y == pytest.approx(expected.y)


def test_circumscribed_regular_polygon() -> None:
    polygon = circumscribed_regular_polygon(
        center=Point(100.0, 200.0),
        inradius=25.0,
        sides=4,
        rotation=45.0,
    )

    expected_points = (
        Point(125.0, 225.0),
        Point(75.0, 225.0),
        Point(75.0, 175.0),
        Point(125.0, 175.0),
    )

    for actual, expected in zip(
        polygon.points,
        expected_points,
        strict=True,
    ):
        assert actual.x == pytest.approx(expected.x)
        assert actual.y == pytest.approx(expected.y)
