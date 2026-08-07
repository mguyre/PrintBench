from dataclasses import dataclass, field

import svgwrite

from printbench import Circle, Document, Line, Point
from printbench.style import StrokeStyle, Style

_STROKE_PATTERNS = {
    StrokeStyle.SOLID: None,
    StrokeStyle.DASHED: "5,5",
    StrokeStyle.CENTERLINE: "10,5,2,5",
}

_DEFAULT_FILL_COLOR = "none"


@dataclass(slots=True)
class SvgRenderer:

    _document: Document | None = None
    _document_height: float = 0.0  # Set by _initialize() before rendering.
    _default_style: Style = field(default_factory=Style)
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
        self._default_style = self._initialize_default_style(document.default_style)

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

    def _initialize_default_style(self, style: Style) -> Style:
        """Initialize the renderer default style."""

        return Style(
            fill_color=(
                style.fill_color
                if style.fill_color is not None
                else _DEFAULT_FILL_COLOR
            ),
            stroke_color=(
                style.stroke_color if style.stroke_color is not None else "black"
            ),
            stroke_width=(
                style.stroke_width if style.stroke_width is not None else 1.0
            ),
            stroke_style=style.stroke_style,
        )

    def _effective_style(
        self,
        style: Style | None,
    ) -> Style:
        """Combine an element style with the renderer default style."""

        if style is None:
            return self._default_style

        return Style(
            fill_color=(
                style.fill_color
                if style.fill_color is not None
                else self._default_style.fill_color
            ),
            stroke_color=(
                style.stroke_color
                if style.stroke_color is not None
                else self._default_style.stroke_color
            ),
            stroke_width=(
                style.stroke_width
                if style.stroke_width is not None
                else self._default_style.stroke_width
            ),
            stroke_style=(
                style.stroke_style
                if style.stroke_style is not None
                else self._default_style.stroke_style
            ),
        )

    def _common_style_to_svg_attributes(
        self,
        style: Style,
    ) -> dict[str, object]:
        """Convert the style elements used by all sgv shapes into svgwrite attributes."""

        attributes: dict[str, object] = {}

        attributes["stroke"] = style.stroke_color
        attributes["stroke_width"] = style.stroke_width

        if style.stroke_style is not None:
            attributes.update(
                self._stroke_style_to_svg_attributes(
                    style.stroke_style,
                )
            )

        return attributes

    def _closed_style_to_svg_attributes(
        self,
        style: Style,
    ) -> dict[str, object]:
        """Convert Style properties for a closed SVG shape."""

        attributes = self._common_style_to_svg_attributes(style)
        attributes["fill"] = style.fill_color

        return attributes

    def _stroke_style_to_svg_attributes(
        self,
        stroke_style: StrokeStyle,
    ) -> dict[str, object]:
        """Convert a StrokeStyle into svgwrite attributes."""

        dasharray = _STROKE_PATTERNS[stroke_style]

        if dasharray is None:
            return {}

        return {"stroke_dasharray": dasharray}

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
        elif isinstance(element, Circle):
            self._render_circle(element)
        else:
            raise TypeError(f"Unsupported element type: {type(element).__name__}")

    def _render_line(self, line: Line) -> None:
        start = self._map_point(line.start)
        end = self._map_point(line.end)

        style = self._effective_style(line.style)
        attributes = self._common_style_to_svg_attributes(style)

        self._drawing.add(
            self._drawing.line(
                start=(start.x, start.y),
                end=(end.x, end.y),
                **attributes,
            )
        )

    def _render_circle(self, circle: Circle) -> None:
        center_point = self._map_point(circle.center)
        style = self._effective_style(circle.style)
        attributes = self._closed_style_to_svg_attributes(style)
        self._drawing.add(
            self._drawing.circle(
                center=(center_point.x, center_point.y),
                r=circle.radius,
                **attributes,
            )
        )
