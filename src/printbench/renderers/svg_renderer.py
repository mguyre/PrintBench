from dataclasses import dataclass

import svgwrite

from printbench import Document, Line, Point
from printbench.style import Style


@dataclass(slots=True)
class SvgRenderer:

    _document: Document | None = None
    _document_height: float = 0.0  # Set by _initialize() before rendering.
    _default_style: Style | None = None
    _drawing: svgwrite.Drawing | None = None

    def render(self, document: Document) -> str:
        self._initialize(document)

        for element in document:
            self._render(element)

        return self._drawing.tostring()

    def _initialize(self, document: Document) -> None:
        if document.default_style is None:
            raise ValueError("Document.default_style cannot be None")
        self._document = document
        self._document_height = document.height
        self._default_style = document.default_style
        self._drawing = svgwrite.Drawing(
            size=(
                f"{document.width}{document.units}",
                f"{document.height}{document.units}",
            ),
            profile="tiny",
        )
        self._drawing.viewbox(
            minx=0,
            miny=0,
            width=document.width,
            height=document.height,
        )
        # TODO:
        # Resolve document.default_style into a renderer-specific complete style.

    def _map_point(self, point: Point) -> Point:
        """Map a document point (Cartesian) into SVG coordinates."""
        # Cartesian is bottom left origin
        # SVG is top left origin
        return Point(
            point.x,
            self._document_height - point.y,
        )

    def _render(self, element) -> None:
        if isinstance(element, Line):
            self._render_line(element)
        else:
            raise TypeError(f"Unsupported element type: {type(element).__name__}")

    def _render_line(self, line: Line) -> str:
        start = self._map_point(line.start)
        end = self._map_point(line.end)
        style = line.style or self._default_style

        return (
            f"<line "
            f'x1="{start.x}" '
            f'y1="{start.y}" '
            f'x2="{end.x}" '
            f'y2="{end.y}" '
            f'stroke="{style.stroke_color}" '
            f'stroke_width="{style.stroke_width}" '
            "/>"
        )
