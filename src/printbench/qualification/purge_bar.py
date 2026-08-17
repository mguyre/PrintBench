from printbench.geometry import Point, Rectangle
from printbench.style import Style


def purge_bar(
    origin: Point, width: float, height: float, color: str = "black"
) -> Rectangle:
    return Rectangle(
        bottom_left=origin,
        width=width,
        height=height,
        style=Style(fill_color=color, stroke_color=color),
    )
