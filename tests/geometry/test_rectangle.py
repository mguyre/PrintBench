from dataclasses import FrozenInstanceError

import pytest

from printbench import Point, Rectangle, StrokeStyle, Style


def test_rectangle_stores_values() -> None:
    bottom_left = Point(12.3, 45.6)
    style = Style(
        fill_color="cornflowerblue",
        stroke_color="blanchedalmond",
        stroke_width=1.234,
        stroke_style=StrokeStyle.DASHED,
    )

    rectangle = Rectangle(
        bottom_left=bottom_left,
        width=78.9,
        height=23.4,
        style=style,
    )

    assert rectangle.bottom_left == bottom_left
    assert rectangle.width == 78.9
    assert rectangle.height == 23.4
    assert rectangle.style == style


def test_rectangle_is_immutable() -> None:
    rectangle = Rectangle(
        bottom_left=Point(12.3, 45.6),
        width=78.9,
        height=67.9,
    )

    with pytest.raises(FrozenInstanceError):
        rectangle.bottom_left = 98.7


@pytest.mark.parametrize(
    ("width", "height"),
    [
        (0.0, 45.6),
        (-1.234, 45.6),
        (78.9, 0.0),
        (78.9, -1.234),
    ],
)
def test_rectangle_rejects_non_positive_dimensions(
    width: float,
    height: float,
) -> None:
    with pytest.raises(ValueError):
        Rectangle(
            bottom_left=Point(12.3, 45.6),
            width=width,
            height=height,
        )
