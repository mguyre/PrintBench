from dataclasses import FrozenInstanceError

import pytest

from printbench import Ellipse, Point, StrokeStyle, Style


def test_ellipse_stores_values() -> None:
    center = Point(12.3, 45.6)
    style = Style(
        fill_color="cornflowerblue",
        stroke_color="blanchedalmond",
        stroke_width=1.234,
        stroke_style=StrokeStyle.DASHED,
    )

    ellipse = Ellipse(
        center=center,
        radius_x=78.9,
        radius_y=23.4,
        style=style,
    )

    assert ellipse.center == center
    assert ellipse.radius_x == 78.9
    assert ellipse.radius_y == 23.4
    assert ellipse.style == style


def test_ellipse_is_immutable() -> None:
    ellipse = Ellipse(
        center=Point(12.3, 45.6),
        radius_x=78.9,
        radius_y=23.4,
    )

    with pytest.raises(FrozenInstanceError):
        ellipse.radius_x = 98.7


@pytest.mark.parametrize(
    ("radius_x", "radius_y"),
    [
        (0.0, 23.4),
        (-1.234, 23.4),
        (78.9, 0.0),
        (78.9, -1.234),
    ],
)
def test_ellipse_rejects_non_positive_radii(
    radius_x: float,
    radius_y: float,
) -> None:
    with pytest.raises(ValueError):
        Ellipse(
            center=Point(12.3, 45.6),
            radius_x=radius_x,
            radius_y=radius_y,
        )
