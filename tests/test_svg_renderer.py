from printbench import Document, Point, SvgRenderer


def test_empty_document_renders_to_svg():
    doc = Document(
        width=333,
        height=418,
    )

    renderer = SvgRenderer()

    svg = renderer.render(doc)

    opening_tag_length = svg.index(">") + 1
    opening_tag = svg[:opening_tag_length]
    end_tag = svg[opening_tag_length:]

    assert opening_tag.startswith("<svg")
    assert opening_tag.endswith(">")
    assert 'xmlns="http://www.w3.org/2000/svg"' in opening_tag
    assert 'width="333mm"' in opening_tag
    assert 'height="418mm"' in opening_tag
    assert 'viewBox="0 0 333 418"' in opening_tag

    assert end_tag == "</svg>"


def test_renderer_maps_point_to_svg_coordinates():
    doc = Document(
        width=987,
        height=654,
    )
    renderer = SvgRenderer()
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
    result = renderer._map_point(test_point, doc)

    assert result == expected
