import pytest

from printbench import Vector


def test_vector_creation():
    vector = Vector(3, 4)

    assert vector.x == 3
    assert vector.y == 4


def test_vector_subtraction():
    left = Vector(7, 5)
    right = Vector(2, 3)

    result = left - right

    assert result == Vector(5, 2)


def test_vector_scalar_multiplication():
    vector = Vector(3, 4)

    result = vector * 2

    assert result == Vector(6, 8)


def test_vector_reverse_scalar_multiplication():
    vector = Vector(3, 4)

    result = 2 * vector

    assert result == Vector(6, 8)


def test_vector_scalar_division():
    vector = Vector(8, 6)

    result = vector / 2

    assert result == Vector(4, 3)


def test_length():
    assert Vector(3, 4).length() == 5.0


def test_length_squared():
    assert Vector(3, 4).length_squared() == 25.0


def test_zero_length():
    assert Vector(0, 0).length() == 0.0
    assert Vector(0, 0).length_squared() == 0.0


def test_negative_components():
    assert Vector(-3, -4).length() == 5.0


def test_length_squared_of_zero_vector_is_zero():
    v = Vector(0, 0)

    assert v.length_squared() == 0


def test_length_squared_of_345_vector_is_25():
    v = Vector(3, 4)

    result = v.length_squared()

    assert result == 25


def test_length_of_zero_vector_is_zero():
    v = Vector(0, 0)

    result = v.length()

    assert result == 0


def test_length_is_independent_of_sign():
    v = Vector(-3, -4)

    result = v.length()

    assert result == 5


def test_normalized_345_vector():
    v = Vector(3, 4)

    result = v.normalized()

    assert result == Vector(0.6, 0.8)


def test_normalized_vector_has_unit_length():
    v = Vector(3, 4)

    result = v.normalized()

    assert result.length() == pytest.approx(1.0)


def test_normalizing_zero_vector_raises_value_error():
    with pytest.raises(ValueError):
        Vector(0, 0).normalized()


def test_dot_product():
    assert Vector(1, 2).dot(Vector(3, 4)) == 11


def test_dot_product_with_zero_vector():
    assert Vector(3, 4).dot(Vector(0, 0)) == 0


def test_dot_product_is_commutative():
    a = Vector(2, 5)
    b = Vector(7, 11)

    assert a.dot(b) == b.dot(a)


def test_perpendicular_vectors_have_zero_dot_product():
    assert Vector(1, 0).dot(Vector(0, 1)) == 0
