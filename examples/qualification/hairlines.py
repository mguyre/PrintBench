from printbench import Document, Point, SvgRenderer
from printbench.qualification import hairlines, purge_bar

doc = Document(
    width=215.9,
    height=279.4,
)

doc.add(
    purge_bar(
        origin=Point(10.0, 260.0),
        width=60,
        height=10.0,
        color="black",
    )
)

doc.add(
    hairlines(
        bottom_left=Point(10.0, 220.0),
        box_width=55.0,
        box_height=25.0,
        box_spacing=10.0,
        line_spacing=5.0,
        line_width=0.05,
        color="black",
        label_font_size=4.0,
        label_gap=1.0,
    )
)

renderer = SvgRenderer()
svg = renderer.render(doc)

with open("hairlines.svg", "w", encoding="utf-8") as file:
    file.write(svg)
