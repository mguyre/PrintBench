from dataclasses import FrozenInstanceError

import pytest

from printbench import StrokeStyle, Style


def test_new_style_defaults_to_none():
    style = Style()

    assert style.stroke_color is None
    assert style.stroke_width is None
    assert style.stroke_style is None


def test_style_stores_values():
    style = Style(
        stroke_color="cyan",
        stroke_width=0.137,
        stroke_style=StrokeStyle.CENTERLINE,
    )

    assert style.stroke_color == "cyan"
    assert style.stroke_width == 0.137
    assert style.stroke_style is StrokeStyle.CENTERLINE


def test_styles_with_same_values_are_equal():
    style1 = Style(
        stroke_color="cyan",
        stroke_width=0.137,
        stroke_style=StrokeStyle.CENTERLINE,
    )

    style2 = Style(
        stroke_color="cyan",
        stroke_width=0.137,
        stroke_style=StrokeStyle.CENTERLINE,
    )

    assert style1 == style2


def test_style_is_immutable():
    style = Style()

    with pytest.raises(FrozenInstanceError):
        style.stroke_width = 0.137
