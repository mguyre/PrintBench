import math

import pytest

from printbench.document import ClipContainer, Group
from printbench.geometry import Line, Point, Text
from printbench.qualification import hairlines


def test_hairlines_creates_three_clipping_boxes():
    group = hairlines(
        bottom_left=Point(12.3, 45.6),
        box_width=43.2,
        box_height=21.4,
        box_spacing=7.8,
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


def test_hairlines_creates_lines_at_expected_angles():
    group = hairlines(
        bottom_left=Point(12.3, 45.6),
        box_width=43.2,
        box_height=21.4,
        box_spacing=7.8,
        color="cyan",
    )

    targets = [element for element in group if isinstance(element, ClipContainer)]
    expected_angles = [5.0, 10.0, 15.0]

    for target, expected_angle in zip(targets, expected_angles):
        elements = list(target)

        assert len(elements) == 1
        assert isinstance(elements[0], Line)

        line = elements[0]

        dx = line.end.x - line.start.x
        dy = line.end.y - line.start.y

        angle = math.degrees(math.atan2(dy, dx))

        assert angle == pytest.approx(expected_angle)


def test_hairlines_start_at_bottom_left_of_each_box():
    group = hairlines(
        bottom_left=Point(12.3, 45.6),
        box_width=43.2,
        box_height=21.4,
        box_spacing=7.8,
        color="cyan",
    )

    targets = [element for element in group if isinstance(element, ClipContainer)]

    expected_starts = [
        Point(12.3, 45.6),
        Point(63.3, 45.6),
        Point(114.3, 45.6),
    ]

    for target, expected_start in zip(targets, expected_starts):
        line = list(target)[0]
        assert line.start == expected_start


def test_hairlines_creates_angle_labels():
    group = hairlines(
        bottom_left=Point(12.3, 45.6),
        box_width=43.2,
        box_height=21.4,
        box_spacing=7.8,
        color="cyan",
    )

    labels = [element for element in group if isinstance(element, Text)]

    assert len(labels) == 3
    assert [label.text for label in labels] == ["5°", "10°", "15°"]
