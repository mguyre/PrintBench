from printbench import Line, Point, StrokeStyle, Style, Vector


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
