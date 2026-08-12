from dataclasses import dataclass, field

import svgwrite
import base64

from printbench import (
    Circle,
    ClipContainer,
    Document,
    Dot,
    Ellipse,
    Line,
    Point,
    Polygon,
    Polyline,
    Raster,
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
    _clip_id: int | None = None

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
        self._clip_id = 0
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
        elif isinstance(element, Dot):
            self._render_dot(element, parent)
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
        elif isinstance(element, Raster):
            self._render_raster(element, parent)
        else:
            raise TypeError(f"Unsupported element type: {type(element).__name__}")

    def _svg_number(self, value: float) -> float:
        return round(value, 4)

    def _render_line(self, line: Line, parent) -> None:
        start = self._map_point(line.start)
        end = self._map_point(line.end)

        style = self._effective_style(line.style)
        attributes = self._common_style_to_svg_attributes(style)

        svg_line = self._drawing.line(
            start=(self._svg_number(start.x), self._svg_number(start.y)),
            end=(self._svg_number(end.x), self._svg_number(end.y)),
            **attributes,
        )

        parent.add(svg_line)

    def _render_circle(self, circle: Circle, parent) -> None:
        svg_circle = self._circle_to_svg(circle)

        style = self._effective_style(circle.style)
        attributes = self._closed_style_to_svg_attributes(style)

        svg_circle.update(attributes)
        parent.add(svg_circle)

    def _circle_to_svg(self, circle: Circle):
        center = self._map_point(circle.center)

        return self._drawing.circle(
            center=(
                self._svg_number(center.x),
                self._svg_number(center.y),
            ),
            r=self._svg_number(circle.radius),
        )

    def _render_rectangle(self, rectangle: Rectangle, parent) -> None:
        """Emit a rectangle using the top left corner, width and height values."""
        svg_rect = self._rectangle_to_svg(rectangle)

        style = self._effective_style(rectangle.style)
        attributes = self._closed_style_to_svg_attributes(style)

        svg_rect.update(attributes)

        parent.add(svg_rect)

    def _rectangle_to_svg(self, rectangle: Rectangle):
        top_left = Point(
            rectangle.bottom_left.x,
            rectangle.bottom_left.y + rectangle.height,
        )
        insert_point = self._map_point(top_left)

        return self._drawing.rect(
            insert=(
                self._svg_number(insert_point.x),
                self._svg_number(insert_point.y),
            ),
            size=(
                self._svg_number(rectangle.width),
                self._svg_number(rectangle.height),
            ),
        )

    def _render_ellipse(self, ellipse: Ellipse, parent) -> None:
        """Emit an ellipse using the center point and x and y radi"""
        svg_ellipse = self._ellipse_to_svg(ellipse)
        style = self._effective_style(ellipse.style)
        attributes = self._closed_style_to_svg_attributes(style)
        svg_ellipse.update(attributes)

        parent.add(svg_ellipse)

    def _ellipse_to_svg(self, ellipse: Ellipse):
        center = self._map_point(ellipse.center)
        return self._drawing.ellipse(
            center=(self._svg_number(center.x), self._svg_number(center.y)),
            r=(self._svg_number(ellipse.radius_x), self._svg_number(ellipse.radius_y)),
        )

    def _render_polyline(self, polyline: Polyline, parent) -> None:
        """Emit a polyline as a string of points"""
        points = [self._map_point(point) for point in polyline.points]

        style = self._effective_style(polyline.style)
        attributes = self._common_style_to_svg_attributes(style)

        svg_polyline = self._drawing.polyline(
            points=[
                (self._svg_number(point.x), self._svg_number(point.y))
                for point in points
            ],
            **attributes,
        )
        parent.add(svg_polyline)

    def _render_polygon(self, polygon: Polygon, parent) -> None:
        svg_polygon = self._polygon_to_svg(polygon)

        style = self._effective_style(polygon.style)
        attributes = self._closed_style_to_svg_attributes(style)

        svg_polygon.update(attributes)
        parent.add(svg_polygon)

    def _polygon_to_svg(self, polygon: Polygon):
        points = []

        for point in polygon.points:
            mapped = self._map_point(point)

            points.append(
                (
                    self._svg_number(mapped.x),
                    self._svg_number(mapped.y),
                )
            )

        return self._drawing.polygon(points=points)

    def _render_dot(self, dot: Dot, parent) -> None:
        center = self._map_point(dot.center)

        if dot.style is not None and dot.style.fill_color is not None:
            dot_color = dot.style.fill_color
        elif (
            self._default_style.fill_color is not None
            and self._default_style.fill_color != "none"
        ):
            dot_color = self._default_style.fill_color
        else:
            dot_color = "black"

        svg_dot = self._drawing.circle(
            center=(
                self._svg_number(center.x),
                self._svg_number(center.y),
            ),
            r=self._svg_number(dot.diameter / 2.0),
        )

        svg_dot["fill"] = dot_color
        svg_dot["stroke"] = "none"
        parent.add(svg_dot)

    def _render_clip_container(self, container: ClipContainer, parent) -> None:
        clip_id = self._next_clip_id()

        clip_path = self._drawing.clipPath(id=clip_id)

        clip_path.add(self._render_clip_shape(container.shape))

        self._drawing.defs.add(clip_path)

        group = self._drawing.g(clip_path=f"url(#{clip_id})")

        for element in container:
            self._render(element, parent=group)

        parent.add(group)

        self._render(container.shape, parent=parent)

    def _render_clip_shape(self, shape):
        if isinstance(shape, Circle):
            return self._circle_to_svg(shape)

        if isinstance(shape, Rectangle):
            return self._rectangle_to_svg(shape)

        if isinstance(shape, Ellipse):
            return self._ellipse_to_svg(shape)

        if isinstance(shape, Polygon):
            return self._polygon_to_svg(shape)

        raise TypeError(f"Unsupported clipping shape: {type(shape).__name__}")

    def _next_clip_id(self) -> str:
        self._clip_id += 1
        return f"clip-{self._clip_id}"

    def _render_raster(self, raster: Raster, parent) -> None:
        encoded_png = base64.b64encode(raster.png_data).decode("ascii")
        data_uri = f"data:image/png;base64,{encoded_png}"

        svg_x = raster.origin.x
        svg_y = self._document.height - raster.origin.y - raster.height

        parent.add(
            self._drawing.image(
                href=data_uri,
                insert=(
                    self._svg_number(svg_x),
                    self._svg_number(svg_y),
                ),
                size=(
                    self._svg_number(raster.width),
                    self._svg_number(raster.height),
                ),
            )
        )
