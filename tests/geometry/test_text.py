import pytest

from printbench import Point, Style, Text


def test_text_stores_geometry_and_style():
    style = Style(fill_color="cyan")

    text = Text(
        bottom_left=Point(12.3, 45.6),
        text="5°",
        font_size=4.7,
        style=style,
    )

    assert text.bottom_left == Point(12.3, 45.6)
    assert text.text == "5°"
    assert text.font_size == 4.7
    assert text.style == style


def test_text_rejects_empty_text():
    with pytest.raises(ValueError):
        Text(
            bottom_left=Point(12.3, 45.6),
            text="",
            font_size=4.7,
        )


@pytest.mark.parametrize("font_size", [0.0, -1.2])
def test_text_rejects_non_positive_font_size(font_size):
    with pytest.raises(ValueError):
        Text(
            bottom_left=Point(12.3, 45.6),
            text="5°",
            font_size=font_size,
        )
