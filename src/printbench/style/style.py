from dataclasses import dataclass

from .stroke_style import StrokeStyle


@dataclass(frozen=True, slots=True)
class Style:
    """Describes how geometry should be rendered."""

    stroke_color: str | None = None
    stroke_width: float | None = None
    stroke_style: StrokeStyle | None = None
    fill_color: str | None = None
