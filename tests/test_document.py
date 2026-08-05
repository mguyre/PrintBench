import pytest

from printbench import Document, Line, Point, Style


@pytest.mark.parametrize(
    "width, height",
    [
        (0, 418),
        (-1, 418),
        (333, 0),
        (333, -1),
    ],
)
def test_document_dimensions_must_be_positive(width, height):
    with pytest.raises(ValueError):
        Document(width=width, height=height)


def test_document_has_specified_dimensions():
    doc = Document(
        width=333,
        height=418,
    )

    assert doc.width == 333
    assert doc.height == 418


def test_new_document_is_empty():
    doc = Document(
        width=333,
        height=418,
    )

    assert len(doc) == 0
    assert list(doc) == []


def test_adding_an_element_increases_document_size():
    doc = Document(
        width=333,
        height=418,
    )

    line = Line(
        Point(0, 0),
        Point(10, 10),
    )

    doc.add(line)

    assert len(doc) == 1


def test_document_preserves_insertion_order():
    doc = Document(
        width=333,
        height=418,
    )

    first = Line(
        Point(0, 0),
        Point(1, 1),
    )

    second = Line(
        Point(2, 2),
        Point(3, 3),
    )

    doc.add(first)
    doc.add(second)

    assert list(doc) == [first, second]


def test_document_has_default_style():
    doc = Document(
        width=123,
        height=456,
    )
    assert doc.default_style == Style()


def test_document_accepts_custom_default_style() -> None:
    default_style = Style()
    assert default_style.stroke_width is None
    style = Style(stroke_width=1.0)

    document = Document(width=123, height=456, default_style=style)

    assert document.default_style is style
