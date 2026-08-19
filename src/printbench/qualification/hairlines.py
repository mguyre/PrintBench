import math

from printbench.document import ClipContainer, Group
from printbench.geometry import Line, Point, Rectangle, Text, Vector
from printbench.style import Style


def hairlines(
    bottom_left: Point,
    box_width: float,
    box_height: float,
    box_spacing: float,
    line_spacing: float,
    line_width: float,
    color: str = "black",
    label_font_size: float = 4.0,
    label_gap: float = 1.0,
) -> Group:
    group = Group()
    angles = (5.0, 10.0, 15.0)

    for index, angle in enumerate(angles):
        x = bottom_left.x + index * (box_width + box_spacing)

        label = Text(
            bottom_left=Point(
                x,
                bottom_left.y + box_height + label_gap,
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

        lines = _parallel_lines(
            bottom_left=Point(x, bottom_left.y),
            width=box_width,
            height=box_height,
            angle=angle,
            spacing=line_spacing,
            line_width=line_width,
            color=color,
        )

        for line in lines:
            target.add(line)

        group.add(label)
        group.add(target)

    return group


def _parallel_lines(
    bottom_left: Point,
    width: float,
    height: float,
    angle: float,
    spacing: float,
    line_width: float,
    color: str,
) -> list[Line]:
    angle_radians = math.radians(angle)

    direction = Vector(
        math.cos(angle_radians),
        math.sin(angle_radians),
    )

    normal = Vector(
        -direction.y,
        direction.x,
    )

    center = Point(
        bottom_left.x + width / 2.0,
        bottom_left.y + height / 2.0,
    )

    diagonal = math.hypot(width, height)

    lines = []
    offset = -diagonal

    while offset <= diagonal:
        line_center = center + normal * offset

        start = line_center - direction * diagonal
        end = line_center + direction * diagonal

        lines.append(
            Line(
                start=start,
                end=end,
                style=Style(
                    stroke_color=color,
                    stroke_width=line_width,
                ),
            )
        )

        offset += spacing

    return lines
