import math

from printbench.document import ClipContainer, Group
from printbench.geometry import Line, Point, Rectangle, Text
from printbench.style import Style


def hairlines(
    bottom_left: Point,
    box_width: float,
    box_height: float,
    box_spacing: float,
    color: str = "black",
    label_font_size: float = 4.0,
) -> Group:
    group = Group()
    angles = (5.0, 10.0, 15.0)

    for index, angle in enumerate(angles):
        x = bottom_left.x + index * (box_width + box_spacing)

        label = Text(
            bottom_left=Point(
                x,
                bottom_left.y + box_height,
            ),
            text=f"{angle:g}°",
            font_size=label_font_size,
            style=Style(fill_color=color),
        )

        shape = Rectangle(
            bottom_left=Point(x, bottom_left.y),
            width=box_width,
            height=box_height,
        )

        target = ClipContainer(shape)

        start = Point(
            x,
            bottom_left.y,
        )

        line_length = box_width * 2.0
        angle_radians = math.radians(angle)

        end = Point(
            start.x + line_length * math.cos(angle_radians),
            start.y + line_length * math.sin(angle_radians),
        )

        target.add(
            Line(
                start=start,
                end=end,
                style=Style(stroke_color=color),
            )
        )

        group.add(label)
        group.add(target)

    return group
