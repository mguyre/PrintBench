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
