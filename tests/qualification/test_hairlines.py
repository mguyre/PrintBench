import math

import pytest

from printbench.document import ClipContainer, Group
from printbench.geometry import Line, Point, Text
from printbench.qualification import hairlines
from printbench.qualification.hairlines import _parallel_lines


def test_hairlines_creates_three_clipping_boxes():
    group = hairlines(
        bottom_left=Point(12.3, 45.6),
        box_width=43.2,
        box_height=21.4,
        box_spacing=7.8,
        line_spacing=5.3,
        line_width=0.123,
        color="cyan",
    )

    targets = [element for element in group if isinstance(element, ClipContainer)]

    assert len(targets) == 3
    assert all(isinstance(target, ClipContainer) for target in targets)

    assert targets[0].shape.bottom_left == Point(12.3, 45.6)
    assert targets[1].shape.bottom_left == Point(63.3, 45.6)
    assert targets[2].shape.bottom_left == Point(114.3, 45.6)

    for target in targets:
        assert target.shape.width == 43.2
        assert target.shape.height == 21.4


def test_hairlines_uses_expected_angles():
    group = hairlines(
        bottom_left=Point(12.3, 45.6),
        box_width=43.2,
        box_height=21.4,
        box_spacing=7.8,
        line_spacing=5.3,
        line_width=0.123,
        color="cyan",
    )

    targets = [element for element in group if isinstance(element, ClipContainer)]

    expected_angles = [5.0, 10.0, 15.0]

    for target, expected_angle in zip(targets, expected_angles):
        line = list(target)[0]

        dx = line.end.x - line.start.x
        dy = line.end.y - line.start.y

        actual_angle = math.degrees(math.atan2(dy, dx))

        assert actual_angle == pytest.approx(expected_angle)


def test_hairlines_creates_multiple_lines_in_each_box():
    group = hairlines(
        bottom_left=Point(12.3, 45.6),
        box_width=43.2,
        box_height=21.4,
        box_spacing=7.8,
        line_spacing=5.3,
        line_width=0.123,
        color="cyan",
    )

    targets = [element for element in group if isinstance(element, ClipContainer)]

    assert len(targets) == 3

    for target in targets:
        lines = list(target)

        assert len(lines) > 1
        assert all(isinstance(line, Line) for line in lines)


def test_hairlines_creates_angle_labels():
    group = hairlines(
        bottom_left=Point(12.3, 45.6),
        box_width=43.2,
        box_height=21.4,
        box_spacing=7.8,
        line_spacing=5.3,
        line_width=0.123,
        color="cyan",
    )

    labels = [element for element in group if isinstance(element, Text)]

    assert len(labels) == 3
    assert [label.text for label in labels] == ["5°", "10°", "15°"]


def test_hairlines_positions_labels_above_boxes():
    group = hairlines(
        bottom_left=Point(12.3, 45.6),
        box_width=43.2,
        box_height=21.4,
        box_spacing=7.8,
        line_spacing=5.3,
        line_width=0.123,
        color="cyan",
        label_font_size=4.7,
        label_gap=1.3,
    )

    labels = [element for element in group if isinstance(element, Text)]

    expected_positions = [
        Point(12.3, 68.3),
        Point(63.3, 68.3),
        Point(114.3, 68.3),
    ]

    for label, expected_position in zip(labels, expected_positions):
        assert label.bottom_left == expected_position
        assert label.font_size == 4.7


def test_hairlines_uses_passed_color():
    group = hairlines(
        bottom_left=Point(12.3, 45.6),
        box_width=43.2,
        box_height=21.4,
        box_spacing=7.8,
        line_spacing=5.3,
        line_width=0.123,
        color="magenta",
    )

    labels = [element for element in group if isinstance(element, Text)]

    targets = [element for element in group if isinstance(element, ClipContainer)]

    for label in labels:
        assert label.style is not None
        assert label.style.fill_color == "magenta"

    for target in targets:
        line = list(target)[0]

        assert line.style is not None
        assert line.style.stroke_color == "magenta"


def test_parallel_lines_creates_multiple_lines():
    lines = _parallel_lines(
        bottom_left=Point(12.3, 45.6),
        width=43.2,
        height=21.4,
        angle=10.0,
        spacing=5.3,
        line_width=0.123,
        color="cyan",
    )

    assert len(lines) > 1
    assert all(isinstance(line, Line) for line in lines)


def test_parallel_lines_have_expected_angle():
    lines = _parallel_lines(
        bottom_left=Point(12.3, 45.6),
        width=43.2,
        height=21.4,
        angle=12.7,
        spacing=5.3,
        line_width=0.123,
        color="cyan",
    )

    for line in lines:
        dx = line.end.x - line.start.x
        dy = line.end.y - line.start.y

        actual_angle = math.degrees(math.atan2(dy, dx))

        assert actual_angle == pytest.approx(12.7)


def test_parallel_lines_have_expected_spacing():
    lines = _parallel_lines(
        bottom_left=Point(12.3, 45.6),
        width=43.2,
        height=21.4,
        angle=12.7,
        spacing=5.3,
        line_width=0.123,
        color="cyan",
    )

    for first, second in zip(lines, lines[1:]):
        dx = second.start.x - first.start.x
        dy = second.start.y - first.start.y

        actual_spacing = math.hypot(dx, dy)

        assert actual_spacing == pytest.approx(5.3)


def _signed_distance_from_line(point: Point, line: Line) -> float:
    dx = line.end.x - line.start.x
    dy = line.end.y - line.start.y

    length = math.hypot(dx, dy)

    return (dx * (point.y - line.start.y) - dy * (point.x - line.start.x)) / length


def test_parallel_lines_cover_requested_rectangle():
    bottom_left = Point(12.3, 45.6)
    width = 43.2
    height = 21.4

    lines = _parallel_lines(
        bottom_left=bottom_left,
        width=width,
        height=height,
        angle=12.7,
        spacing=5.3,
        line_width=0.123,
        color="cyan",
    )

    corners = [
        bottom_left,
        Point(bottom_left.x + width, bottom_left.y),
        Point(bottom_left.x, bottom_left.y + height),
        Point(bottom_left.x + width, bottom_left.y + height),
    ]

    first = lines[0]
    last = lines[-1]

    for corner in corners:
        first_distance = _signed_distance_from_line(corner, first)
        last_distance = _signed_distance_from_line(corner, last)

        assert first_distance * last_distance <= 0.0


def test_parallel_lines_use_requested_style():
    lines = _parallel_lines(
        bottom_left=Point(12.3, 45.6),
        width=43.2,
        height=21.4,
        angle=12.7,
        spacing=5.3,
        line_width=0.123,
        color="magenta",
    )

    for line in lines:
        assert line.style is not None
        assert line.style.stroke_width == 0.123
        assert line.style.stroke_color == "magenta"
