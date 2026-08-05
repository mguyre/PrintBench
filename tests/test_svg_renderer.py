from printbench import Document, Point, SvgRenderer


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
    # this is normally called in the start of render which is not used in this UT
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
