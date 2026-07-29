from dataclasses import FrozenInstanceError

import pytest

from printbench import Point, Vector


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


def test_subtracting_two_points_returns_a_vector():
    p1 = Point(10, 20)
    p2 = Point(13, 24)

    assert p2 - p1 == Vector(3, 4)


def test_adding_a_vector_to_a_point_returns_a_point():
    p = Point(10, 20)
    v = Vector(3, 4)

    assert p + v == Point(13, 24)


def test_subtracting_a_vector_from_a_point_returns_a_point():
    p = Point(13, 24)
    v = Vector(3, 4)

    assert p - v == Point(10, 20)


def test_adding_two_points_is_not_supported():
    with pytest.raises(TypeError):
        Point(1, 2) + Point(3, 4)


def test_distance_between_points():
    p1 = Point(10, 20)
    p2 = Point(13, 24)

    assert p1.distance_to(p2) == 5


def test_distance_to_same_point_is_zero():
    p1 = Point(5, 60)
    p2 = Point(5, 60)
    assert p1.distance_to(p2) == 0


def test_distance_is_symmetric():
    p1 = Point(10, 20)
    p2 = Point(13, 24)

    assert p1.distance_to(p2) == p2.distance_to(p1)
