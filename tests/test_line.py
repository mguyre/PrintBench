from printbench import Line, Point, Vector


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
