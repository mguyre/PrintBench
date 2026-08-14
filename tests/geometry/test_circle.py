from dataclasses import FrozenInstanceError

import pytest

from printbench import Circle, Point, StrokeStyle, Style


def test_circle_stores_values() -> None:
    center = Point(12.3, 45.6)
    style = Style(
        stroke_color="blanchedalmond",
        stroke_width=1.234,
        stroke_style=StrokeStyle.DASHED,
    )

    circle = Circle(
        center=center,
        radius=78.9,
        style=style,
    )

    assert circle.center == center
    assert circle.radius == 78.9
    assert circle.style == style


def test_circle_is_immutable() -> None:
    circle = Circle(
        center=Point(12.3, 45.6),
        radius=78.9,
    )

    with pytest.raises(FrozenInstanceError):
        circle.radius = 98.7


@pytest.mark.parametrize(
    "radius",
    [
        0.0,
        -1.234,
    ],
)
def test_circle_rejects_non_positive_radius(radius: float) -> None:
    with pytest.raises(ValueError):
        Circle(
            center=Point(12.3, 45.6),
            radius=radius,
        )
