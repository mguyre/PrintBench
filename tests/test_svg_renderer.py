from printbench import (
    Circle,
    Document,
    Ellipse,
    Line,
    Point,
    Polygon,
    Polyline,
    Rectangle,
    SvgRenderer,
)
from printbench.style import StrokeStyle, Style


def test_empty_document_renders_to_svg():
    doc = Document(
        width=432.1,
        height=567.8,
    )

    renderer = SvgRenderer()

    svg = renderer.render(doc)

    opening_tag_length = svg.index(">") + 1
    opening_tag = svg[:opening_tag_length]
    closing_tag_start = svg.rindex("<")
    # body = svg[opening_tag_length:closing_tag_start]
    end_tag = svg[closing_tag_start:]

    # print(f"svg text: {svg}")
    assert opening_tag.startswith("<svg")
    assert opening_tag.endswith(">")
    assert 'xmlns="http://www.w3.org/2000/svg"' in opening_tag
    assert 'width="432.1mm"' in opening_tag
    assert 'height="567.8mm"' in opening_tag
    assert 'viewBox="0,0,432.1,567.8"' in opening_tag

    assert end_tag == "</svg>"


def test_renderer_maps_point_to_svg_coordinates():
    doc = Document(
        width=987,
        height=654,
    )
    renderer = SvgRenderer(doc)
    # _initialize is normally called in the start of render which is not used in this UT
    renderer._initialize(doc)

    # Cartesian (origin at lower left)
    #
    #     +y
    #      ^
    #      |
    #      +----> +x
    #
    # SVG (origin at upper left)
    #
    #      +----> +x
    #      |
    #      v
    #     +y

    test_point = Point(23, 56)
    expected = Point(23, (654 - 56))
    result = renderer._map_point(test_point)

    assert result == expected


def test_initialize_sets_renderer_default_style():
    doc = Document(
        width=432.1,
        height=567.8,
        default_style=Style(),
    )

    renderer = SvgRenderer()
    renderer._initialize(doc)

    # should be the default svg_renderer values
    assert renderer._default_style == Style(
        fill_color="none",
        stroke_color="black",
        stroke_width=1.0,
        stroke_style=None,
    )


def test_effective_style_uses_renderer_default():
    renderer = SvgRenderer()

    renderer._default_style = Style(
        fill_color="none",
        stroke_color="black",
        stroke_width=1.0,
        stroke_style=StrokeStyle.SOLID,
    )

    result = renderer._effective_style(None)

    assert result == renderer._default_style


def test_effective_style_empty_style_uses_renderer_default():
    renderer = SvgRenderer()

    renderer._default_style = Style(
        fill_color="none",
        stroke_color="black",
        stroke_width=1.0,
        stroke_style=StrokeStyle.SOLID,
    )

    result = renderer._effective_style(Style())

    assert result == renderer._default_style


def test_effective_style_overrides_stroke_color():
    renderer = SvgRenderer()

    default = Style(
        stroke_color="blanchedalmond",
        stroke_width=987.654,
    )
    renderer._default_style = default

    override = Style(
        stroke_color="red",
    )

    result = renderer._effective_style(override)

    assert result.stroke_color == "red"
    assert result.stroke_width == default.stroke_width
    assert result.stroke_style == default.stroke_style


def test_effective_style_overrides_stroke_width():
    renderer = SvgRenderer()

    default = Style(
        stroke_color="blanchedalmond",
        stroke_width=987.654,
    )
    renderer._default_style = default

    override = Style(
        stroke_width=default.stroke_width + 1.0,
    )

    result = renderer._effective_style(override)

    assert result.stroke_color == default.stroke_color
    assert result.stroke_width == default.stroke_width + 1.0
    assert result.stroke_style == default.stroke_style


def test_effective_style_overrides_stroke_style():
    renderer = SvgRenderer()

    default = Style(
        stroke_color="blanchedalmond",
        stroke_width=987.654,
    )
    renderer._default_style = default

    override = Style(
        stroke_style=StrokeStyle.DASHED,
    )

    result = renderer._effective_style(override)

    assert result.stroke_color == default.stroke_color
    assert result.stroke_width == default.stroke_width
    assert result.stroke_style == StrokeStyle.DASHED


def test_effective_style_overrides_all_values():
    renderer = SvgRenderer()

    default = Style(
        stroke_color="blanchedalmond",
        stroke_width=987.654,
    )
    renderer._default_style = default

    override = Style(
        stroke_color="red",
        stroke_width=default.stroke_width + 1.0,
        stroke_style=StrokeStyle.DASHED,
    )

    result = renderer._effective_style(override)

    assert result == override


def test_render_line():
    doc = Document(
        width=432.1,
        height=567.8,
        default_style=Style(
            stroke_color="blanchedalmond",
            stroke_width=1.234,
        ),
    )

    doc.add(
        Line(
            start=Point(12.3, 45.6),
            end=Point(78.9, 101.2),
        )
    )

    renderer = SvgRenderer()

    svg = renderer.render(doc)
    line_start = svg.index("<line")
    line_end = svg.index("/>", line_start) + len("/>")

    encoded_line = svg[line_start:line_end]

    assert encoded_line.startswith("<line")
    assert encoded_line.endswith("/>")

    assert 'x1="12.3"' in encoded_line
    assert 'y1="522.2"' in encoded_line

    assert 'x2="78.9"' in encoded_line
    assert 'y2="466.6"' in encoded_line

    assert 'stroke="blanchedalmond"' in encoded_line
    assert 'stroke-width="1.234"' in encoded_line

    svg_start = svg.index("<svg")
    svg_end = svg.rindex("</svg>")

    assert svg_start < line_start
    assert line_end <= svg_end


def test_render_line_with_style_override():
    doc = Document(
        width=432.1,
        height=567.8,
        default_style=Style(
            stroke_color="blanchedalmond",
            stroke_width=1.234,
        ),
    )

    doc.add(
        Line(
            start=Point(12.3, 45.6),
            end=Point(78.9, 101.2),
            style=Style(
                stroke_color="darkorchid",
            ),
        )
    )

    renderer = SvgRenderer()

    svg = renderer.render(doc)

    line_start = svg.index("<line")
    line_end = svg.index("/>", line_start)

    encoded_line = svg[line_start : line_end + len("/>")]

    assert encoded_line.startswith("<line")
    assert encoded_line.endswith("/>")

    assert 'stroke="darkorchid"' in encoded_line
    assert 'stroke-width="1.234"' in encoded_line


def test_render_line_with_stroke_width_override():
    doc = Document(
        width=432.1,
        height=567.8,
        default_style=Style(
            stroke_color="blanchedalmond",
            stroke_width=1.234,
        ),
    )

    doc.add(
        Line(
            start=Point(12.3, 45.6),
            end=Point(78.9, 101.2),
            style=Style(
                stroke_width=9.876,
            ),
        )
    )

    renderer = SvgRenderer()

    svg = renderer.render(doc)

    line_start = svg.index("<line")
    line_end = svg.index("/>", line_start)

    encoded_line = svg[line_start : line_end + len("/>")]

    assert encoded_line.startswith("<line")
    assert encoded_line.endswith("/>")

    assert 'stroke="blanchedalmond"' in encoded_line
    assert 'stroke-width="9.876"' in encoded_line


def test_render_dashed_line() -> None:
    """Renderer emits a dashed SVG line."""

    doc = Document(
        width=432.1,
        height=567.8,
        default_style=Style(
            stroke_color="blanchedalmond",
            stroke_width=1.234,
        ),
    )

    style = Style(
        stroke_color="black",
        stroke_style=StrokeStyle.DASHED,
    )

    doc.add(
        Line(
            Point(10, 20),
            Point(30, 40),
            style=style,
        )
    )

    renderer = SvgRenderer()

    svg = renderer.render(doc)

    line_start = svg.index("<line")
    line_end = svg.index("/>", line_start) + 2

    encoded_line = svg[line_start:line_end]

    assert 'stroke-dasharray="5,5"' in encoded_line


def test_render_centerline() -> None:
    """Renderer emits a centerline SVG line."""

    doc = Document(
        width=432.1,
        height=567.8,
        default_style=Style(
            stroke_color="blanchedalmond",
            stroke_width=1.234,
        ),
    )

    style = Style(
        stroke_color="black",
        stroke_style=StrokeStyle.CENTERLINE,
    )

    doc.add(
        Line(
            Point(10, 20),
            Point(30, 40),
            style=style,
        )
    )

    renderer = SvgRenderer()

    svg = renderer.render(doc)
    # print(svg)

    line_start = svg.index("<line")
    line_end = svg.index("/>", line_start) + 2

    encoded_line = svg[line_start:line_end]

    assert 'stroke-dasharray="10,5,2,5"' in encoded_line


def test_closed_style_to_svg_attributes_includes_fill():
    renderer = SvgRenderer()

    style = Style(
        fill_color="blanchedalmond",
        stroke_color="cornflowerblue",
        stroke_width=1.234,
        stroke_style=StrokeStyle.DASHED,
    )

    attributes = renderer._closed_style_to_svg_attributes(style)

    assert attributes["fill"] == "blanchedalmond"
    assert attributes["stroke"] == "cornflowerblue"
    assert attributes["stroke_width"] == 1.234
    assert attributes["stroke_dasharray"] == "5,5"


def test_render_circle() -> None:
    doc = Document(
        width=432.1,
        height=567.8,
        default_style=Style(
            stroke_color="blanchedalmond",
            stroke_width=1.234,
        ),
    )

    doc.add(
        Circle(
            center=Point(12.3, 45.6),
            radius=78.9,
        )
    )

    renderer = SvgRenderer()
    svg = renderer.render(doc)
    # print(svg)
    circle_start = svg.index("<circle")
    circle_end = svg.index("/>", circle_start) + len("/>")

    encoded_circle = svg[circle_start:circle_end]

    assert encoded_circle.startswith("<circle")
    assert encoded_circle.endswith("/>")

    assert 'cx="12.3"' in encoded_circle
    assert 'cy="522.2"' in encoded_circle  # Cartesian to SVG: 567.8 - 45.6 = 522.2
    assert 'r="78.9"' in encoded_circle

    assert 'stroke="blanchedalmond"' in encoded_circle
    assert 'stroke-width="1.234"' in encoded_circle
    assert 'fill="none"' in encoded_circle


def test_render_filled_circle() -> None:
    doc = Document(
        width=432.1,
        height=567.8,
        default_style=Style(
            stroke_color="blanchedalmond",
            stroke_width=1.234,
        ),
    )

    doc.add(
        Circle(
            center=Point(12.3, 45.6),
            radius=78.9,
            style=Style(
                fill_color="cornflowerblue",
            ),
        )
    )

    renderer = SvgRenderer()
    svg = renderer.render(doc)

    circle_start = svg.index("<circle")
    circle_end = svg.index("/>", circle_start) + 2

    encoded_circle = svg[circle_start:circle_end]

    assert 'fill="cornflowerblue"' in encoded_circle


def test_render_rectangle() -> None:
    doc = Document(
        width=432.1,
        height=567.8,
        default_style=Style(
            stroke_color="blanchedalmond",
            stroke_width=1.234,
        ),
    )

    doc.add(
        Rectangle(
            bottom_left=Point(12.3, 45.6),
            width=78.9,
            height=23.4,
        )
    )

    renderer = SvgRenderer()
    svg = renderer.render(doc)

    rect_start = svg.index("<rect")
    rect_end = svg.index("/>", rect_start) + 2

    encoded_rect = svg[rect_start:rect_end]

    assert encoded_rect.startswith("<rect")
    assert encoded_rect.endswith("/>")

    assert 'x="12.3"' in encoded_rect
    assert 'y="498.8"' in encoded_rect

    assert 'width="78.9"' in encoded_rect
    assert 'height="23.4"' in encoded_rect

    assert 'fill="none"' in encoded_rect
    assert 'stroke="blanchedalmond"' in encoded_rect
    assert 'stroke-width="1.234"' in encoded_rect


def test_render_filled_rectangle() -> None:
    doc = Document(
        width=432.1,
        height=567.8,
        default_style=Style(
            stroke_color="blanchedalmond",
            stroke_width=1.234,
        ),
    )

    doc.add(
        Rectangle(
            bottom_left=Point(12.3, 45.6),
            width=78.9,
            height=23.4,
            style=Style(
                fill_color="cornflowerblue",
            ),
        )
    )

    renderer = SvgRenderer()
    svg = renderer.render(doc)

    rect_start = svg.index("<rect")
    rect_end = svg.index("/>", rect_start) + 2

    encoded_rect = svg[rect_start:rect_end]

    assert 'fill="cornflowerblue"' in encoded_rect


def test_render_ellipse() -> None:
    doc = Document(
        width=432.1,
        height=567.8,
        default_style=Style(
            stroke_color="blanchedalmond",
            stroke_width=1.234,
        ),
    )

    doc.add(
        Ellipse(
            center=Point(12.3, 45.6),
            radius_x=78.9,
            radius_y=23.4,
        )
    )

    renderer = SvgRenderer()
    svg = renderer.render(doc)

    rect_start = svg.index("<ellipse")
    rect_end = svg.index("/>", rect_start) + 2

    encoded_ellipse = svg[rect_start:rect_end]

    assert encoded_ellipse.startswith("<ellipse")
    assert encoded_ellipse.endswith("/>")

    assert 'cx="12.3"' in encoded_ellipse
    assert 'cy="522.2"' in encoded_ellipse  # 567.8 - 45.6

    assert 'rx="78.9"' in encoded_ellipse
    assert 'ry="23.4"' in encoded_ellipse

    assert 'fill="none"' in encoded_ellipse
    assert 'stroke="blanchedalmond"' in encoded_ellipse
    assert 'stroke-width="1.234"' in encoded_ellipse


def test_render_filled_ellipse() -> None:
    doc = Document(
        width=432.1,
        height=567.8,
        default_style=Style(
            stroke_color="blanchedalmond",
            stroke_width=1.234,
        ),
    )

    doc.add(
        Ellipse(
            center=Point(12.3, 45.6),
            radius_x=78.9,
            radius_y=23.4,
            style=Style(fill_color="lemonchiffon"),
        )
    )

    renderer = SvgRenderer()
    svg = renderer.render(doc)

    rect_start = svg.index("<ellipse")
    rect_end = svg.index("/>", rect_start) + 2

    encoded_ellipse = svg[rect_start:rect_end]

    assert encoded_ellipse.startswith("<ellipse")
    assert encoded_ellipse.endswith("/>")

    assert 'cx="12.3"' in encoded_ellipse
    assert 'cy="522.2"' in encoded_ellipse  # 567.8 - 45.6

    assert 'rx="78.9"' in encoded_ellipse
    assert 'ry="23.4"' in encoded_ellipse

    assert 'fill="lemonchiffon"' in encoded_ellipse
    assert 'stroke="blanchedalmond"' in encoded_ellipse
    assert 'stroke-width="1.234"' in encoded_ellipse


def test_render_polyline() -> None:
    doc = Document(
        width=432.1,
        height=567.8,
        default_style=Style(
            stroke_color="blanchedalmond",
            stroke_width=1.234,
        ),
    )

    doc.add(
        Polyline(
            points=(
                Point(12.3, 45.6),
                Point(78.9, 101.2),
                Point(123.4, 56.7),
            ),
        )
    )

    renderer = SvgRenderer()
    svg = renderer.render(doc)

    polyline_start = svg.index("<polyline")
    polyline_end = svg.index("/>", polyline_start) + 2

    encoded_polyline = svg[polyline_start:polyline_end]

    assert encoded_polyline.startswith("<polyline")
    assert encoded_polyline.endswith("/>")

    # The expected point mappings for the difference between Cartesian and SVG origins:
    # (12.3,  45.6)  →  (12.3,  522.2)
    # (78.9, 101.2)  →  (78.9,  466.6)
    # (123.4, 56.7)  →  (123.4, 511.1)

    assert 'points="12.3,522.2 78.9,466.6 123.4,511.1"' in encoded_polyline

    assert 'stroke="blanchedalmond"' in encoded_polyline
    assert 'stroke-width="1.234"' in encoded_polyline


def test_render_polygon() -> None:
    doc = Document(
        width=432.1,
        height=567.8,
        default_style=Style(
            stroke_color="blanchedalmond",
            stroke_width=1.234,
        ),
    )

    doc.add(
        Polygon(
            points=(
                Point(34.7, 82.3),
                Point(156.8, 234.5),
                Point(287.6, 143.2),
            ),
        )
    )

    renderer = SvgRenderer()
    svg = renderer.render(doc)

    polygon_start = svg.index("<polygon")
    polygon_end = svg.index("/>", polygon_start) + 2

    encoded_polygon = svg[polygon_start:polygon_end]

    assert encoded_polygon.startswith("<polygon")
    assert encoded_polygon.endswith("/>")

    # The expected point mappings for the difference between Cartesian and SVG origins:
    # (34.7,  82.3)  →  (34.7,  485.5)
    # (156.8, 234.5) →  (156.8, 333.3)
    # (287.6, 143.2) →  (287.6, 424.6)
    assert 'points="34.7,485.5 156.8,333.3 287.6,424.6"' in encoded_polygon

    assert 'stroke="blanchedalmond"' in encoded_polygon
    assert 'stroke-width="1.234"' in encoded_polygon
    assert 'fill="none"' in encoded_polygon
