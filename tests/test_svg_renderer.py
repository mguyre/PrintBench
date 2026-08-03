from printbench import Document, SvgRenderer


def test_empty_document_renders_to_svg():
    doc = Document(
        width=333,
        height=418,
    )

    renderer = SvgRenderer()

    svg = renderer.render(doc)

    assert svg.startswith("<svg")
    assert svg.endswith("</svg>")
