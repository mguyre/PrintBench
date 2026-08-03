from dataclasses import dataclass

from printbench import Document, Line, Point


@dataclass(slots=True)
class SvgRenderer:

    def render(self, document: Document) -> str:
        svg_header = (
            '<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{document.width}{document.units}" '
            f'height="{document.height}{document.units}" '
            f'viewBox="0 0 {document.width} {document.height}"'
            ">"
        )

        svg_footer = "</svg>"

        return f"{svg_header}{svg_footer}"

    def _map_point(self, point: Point, document: Document) -> Point:
        """Map a document point (Cartesian) into SVG coordinates."""
        # Cartesian is bottom left origin
        # SVG is top left origin
        return Point(
            point.x,
            document.height - point.y,
        )

    def _render_line(self, line: Line, document: Document) -> str:
        start = self._map_point(line.start, document)
        end = self._map_point(line.end, document)

        return (
            f"<line "
            f'x1="{start.x}" '
            f'y1="{start.y}" '
            f'x2="{end.x}" '
            f'y2="{end.y}" />'
        )
