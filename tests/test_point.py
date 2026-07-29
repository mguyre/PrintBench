from dataclasses import FrozenInstanceError

import pytest

from printbench import Point


def test_create_point():
    point = Point(10.5, 20.25)

    assert point.x == 10.5
    assert point.y == 20.25


def test_points_compare_equal():
    assert Point(1.0, 2.0) == Point(1.0, 2.0)


def test_point_is_immutable():
    point = Point(1.0, 2.0)

    with pytest.raises(FrozenInstanceError):
        point.x = 3.0
