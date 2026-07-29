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
