from printbench.geometry import Point, Rectangle
from printbench.qualification import purge_bar


def test_purge_bar():
    bar = purge_bar(origin=Point(12.3, 45.6), width=123.4, height=5.6, color="hotpink")

    assert isinstance(bar, Rectangle)
    assert bar.bottom_left == Point(12.3, 45.6)
    assert bar.width == 123.4
    assert bar.height == 5.6
    assert bar.style is not None
    assert bar.style.fill_color == "hotpink"
    assert bar.style.stroke_color == "hotpink"
