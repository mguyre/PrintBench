from printbench import Document, Point, SvgRenderer
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


def test_effective_style_uses_renderer_default():
    renderer = SvgRenderer()

    renderer._default_style = Style(
        stroke_color="black",
        stroke_width=1.0,
    )

    result = renderer._effective_style(None)

    assert result == renderer._default_style


def test_effective_style_empty_style_uses_renderer_default():
    renderer = SvgRenderer()

    renderer._default_style = Style(
        stroke_color="black",
        stroke_width=1.0,
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
