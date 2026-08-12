from dataclasses import dataclass

from .point import Point


@dataclass(frozen=True, slots=True)
class Raster:
    origin: Point
    width: float
    height: float
    png_data: bytes

    def __post_init__(self) -> None:
        if self.width <= 0:
            raise ValueError("width must be greater than zero")
        if self.height <= 0:
            raise ValueError("height must be greater than zero")
