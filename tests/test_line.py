import pytest

from printbench import Line, Point, StrokeStyle, Style, Vector, center_mark


def test_line_has_correct_length():
    line = Line(
        Point(10, 20),
        Point(13, 24),
    )

    assert line.length() == 5


def test_line_direction():
    line = Line(
        Point(10, 20),
        Point(13, 24),
    )

    assert line.direction() == Vector(3, 4).normalized()


def test_line_midpoint():
    line = Line(
        Point(10, 20),
        Point(14, 28),
    )

    assert line.midpoint() == Point(12, 24)


def test_line_can_reference_a_style():
    style = Style(
        stroke_color="cyan",
        stroke_width=0.137,
        stroke_style=StrokeStyle.CENTERLINE,
    )

    line = Line(
        Point(17, 31),
        Point(59, 113),
        style=style,
    )

    assert line.style is style


def test_center_mark_creates_two_centered_lines() -> None:
    center = Point(123.4, 234.5)

    horizontal, vertical = center_mark(
        center=center,
        size=45.6,
    )

    assert horizontal.start.x == pytest.approx(100.6)
    assert horizontal.start.y == pytest.approx(234.5)
    assert horizontal.end.x == pytest.approx(146.2)
    assert horizontal.end.y == pytest.approx(234.5)

    assert vertical.start.x == pytest.approx(123.4)
    assert vertical.start.y == pytest.approx(211.7)
    assert vertical.end.x == pytest.approx(123.4)
    assert vertical.end.y == pytest.approx(257.3)


@pytest.mark.parametrize(
    "size",
    [0.0, -1.234],
)
def test_center_mark_rejects_non_positive_size(
    size: float,
) -> None:
    with pytest.raises(ValueError):
        center_mark(
            center=Point(12.3, 45.6),
            size=size,
        )


def test_center_mark_preserves_style() -> None:
    style = Style(
        stroke_color="blanchedalmond",
        stroke_width=1.234,
        stroke_style=StrokeStyle.DASHED,
    )

    horizontal, vertical = center_mark(
        center=Point(123.4, 234.5),
        size=45.6,
        style=style,
    )

    assert horizontal.style == style
    assert vertical.style == style
