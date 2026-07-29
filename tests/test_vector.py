from printbench import Vector


def test_vector_creation():
    vector = Vector(3, 4)

    assert vector.x == 3
    assert vector.y == 4
