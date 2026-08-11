from dataclasses import dataclass, field

import svgwrite

from printbench import (
    ClipContainer,
    Circle,
    Document,
    Ellipse,
    Line,
    Point,
    Polygon,
    Polyline,
    Rectangle,
)
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
            profile="full",
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

    def _render(self, element, parent=None) -> None:
        if parent is None:
            parent = self._drawing
        if isinstance(element, Line):
            self._render_line(element, parent)
        elif isinstance(element, ClipContainer):
            self._render_clip_container(element, parent)
        elif isinstance(element, Circle):
            self._render_circle(element, parent)
        elif isinstance(element, Polygon):
            self._render_polygon(element, parent)
        elif isinstance(element, Polyline):
            self._render_polyline(element, parent)
        elif isinstance(element, Rectangle):
            self._render_rectangle(element, parent)
        elif isinstance(element, Ellipse):
            self._render_ellipse(element, parent)
        else:
            raise TypeError(f"Unsupported element type: {type(element).__name__}")

    def _render_line(self, line: Line, parent) -> None:
        start = self._map_point(line.start)
        end = self._map_point(line.end)

        style = self._effective_style(line.style)
        attributes = self._common_style_to_svg_attributes(style)

        svg_line = self._drawing.line(
            start=(start.x, start.y),
            end=(end.x, end.y),
            **attributes,
        )

        parent.add(svg_line)

    def _render_circle(self, circle: Circle, parent) -> None:
        center_point = self._map_point(circle.center)
        style = self._effective_style(circle.style)
        attributes = self._closed_style_to_svg_attributes(style)

        svg_circle = self._drawing.circle(
            center=(center_point.x, center_point.y),
            r=circle.radius,
            **attributes,
        )
        parent.add(svg_circle)

    def _render_rectangle(self, rectangle: Rectangle, parent) -> None:
        """Emit a rectangle using the top left corner, width and height values"""
        top_left = Point(
            rectangle.bottom_left.x,
            rectangle.bottom_left.y + rectangle.height,
        )
        insert_point = self._map_point(top_left)

        style = self._effective_style(rectangle.style)
        attributes = self._closed_style_to_svg_attributes(style)

        svg_rect = self._drawing.rect(
            insert=(insert_point.x, insert_point.y),
            size=(rectangle.width, rectangle.height),
            **attributes,
        )
        parent.add(svg_rect)

    def _render_ellipse(self, ellipse: Ellipse, parent) -> None:
        """Emit an ellipse using the center point and x and y radi"""
        center = self._map_point(ellipse.center)

        style = self._effective_style(ellipse.style)
        attributes = self._closed_style_to_svg_attributes(style)

        svg_ellipse = self._drawing.ellipse(
            center=(center.x, center.y),
            r=(ellipse.radius_x, ellipse.radius_y),
            **attributes,
        )
        parent.add(svg_ellipse)

    def _render_polyline(self, polyline: Polyline, parent) -> None:
        """Emit a polyline as a string of points"""
        points = [self._map_point(point) for point in polyline.points]

        style = self._effective_style(polyline.style)
        attributes = self._common_style_to_svg_attributes(style)

        svg_polyline = self._drawing.polyline(
            points=[(point.x, point.y) for point in points],
            **attributes,
        )
        parent.add(svg_polyline)

    def _render_polygon(self, polygon: Polygon, parent) -> None:
        """Emit a closed polygon as a string of points"""
        points = [self._map_point(point) for point in polygon.points]

        style = self._effective_style(polygon.style)
        attributes = self._closed_style_to_svg_attributes(style)

        svg_polygon = self._drawing.polygon(
            points=[(point.x, point.y) for point in points],
            **attributes,
        )
        parent.add(svg_polygon)

    def _render_clip_container(self, container: ClipContainer, parent) -> None:
        shape = container.shape

        if not isinstance(shape, Circle):
            raise TypeError(f"Unsupported clipping shape: {type(shape).__name__}")

        center = self._map_point(shape.center)

        clip_id = "clip-1"

        clip_path = self._drawing.clipPath(id=clip_id)

        clip_path.add(
            self._drawing.circle(
                center=(center.x, center.y),
                r=shape.radius,
            )
        )

        self._drawing.defs.add(clip_path)

        group = self._drawing.g(clip_path=f"url(#{clip_id})")

        for element in container:
            self._render(element, parent=group)

        parent.add(group)

        self._render(shape, parent=parent)
