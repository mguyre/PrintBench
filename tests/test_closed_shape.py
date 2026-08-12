import pytest

from printbench.geometry import (
    Circle,
    ClosedShape,
    Line,
    Point,
    Polygon,
)


@pytest.mark.parametrize(
    "shape",
    [
        Circle(center=Point(12.3, 45.6), radius=7.8),
        Polygon(
            points=[
                Point(1.2, 3.4),
                Point(12.3, 4.5),
                Point(6.7, 15.8),
            ]
        ),
    ],
)
def test_closed_shapes_are_closed_shape(shape):
    assert isinstance(shape, ClosedShape)


def test_line_is_not_closed_shape():
    line = Line(
        start=Point(12.3, 45.6),
        end=Point(78.9, 12.3),
    )

    assert not isinstance(line, ClosedShape)
