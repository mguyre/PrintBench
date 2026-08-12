import pytest

from printbench import Style
from printbench.geometry import Dot, Point


def test_dot_stores_center_and_diameter():
    center = Point(12.3, 45.6)

    dot = Dot(center=center, diameter=0.0353)

    assert dot.center == center
    assert dot.diameter == pytest.approx(0.0353)


def test_dot_rejects_zero_diameter():
    with pytest.raises(ValueError):
        Dot(center=Point(12.3, 45.6), diameter=0.0)


def test_dot_rejects_negative_diameter():
    with pytest.raises(ValueError):
        Dot(center=Point(12.3, 45.6), diameter=-0.0353)


def test_dot_is_immutable():
    dot = Dot(center=Point(12.3, 45.6), diameter=0.0353)

    with pytest.raises(AttributeError):
        dot.diameter = 0.1


def test_dot_stores_style():
    style = Style(stroke_color="magenta")

    dot = Dot(
        center=Point(12.3, 45.6),
        diameter=0.0353,
        style=style,
    )

    assert dot.style == style
