from io import BytesIO

from PIL import Image

from printbench.geometry import Point, Raster


def _printer_pixel_pattern(
    width: int,
    height: int,
    mark_size: int,
):
    """A One bit means print the given color for that pixel,
    A zero bit means don't print anything for that pixel"""
    pattern = []
    # pitch = 4 × mark_size
    pitch = 4 * mark_size

    for y in range(height):
        row = []

        mark_row = y // mark_size
        offset = (mark_row % 4) * mark_size

        for x in range(width):
            relative_x = (x - offset) % pitch

            if relative_x < mark_size:
                row.append(1)
            else:
                row.append(0)

        pattern.append(row)

    return pattern


def _pattern_to_rgba(
    pattern,
    color,
):
    rgba = []

    for row in pattern:
        rgba_row = []

        for pixel in row:
            if pixel:
                rgba_row.append((*color, 255))
            else:
                rgba_row.append((0, 0, 0, 0))

        rgba.append(rgba_row)

    return rgba


def printer_pixel_raster(
    origin: Point,
    width_in_pixels: int,
    height_in_pixels: int,
    mark_size: int,
    color: tuple[int, int, int],
    dpi_x: float = 720.0,
    dpi_y: float = 720.0,
) -> Raster:
    if width_in_pixels <= 0:
        raise ValueError("width_in_pixels must be greater than zero")
    if height_in_pixels <= 0:
        raise ValueError("height_in_pixels must be greater than zero")
    if mark_size <= 0:
        raise ValueError("mark_size must be greater than zero")
    if dpi_x <= 0:
        raise ValueError("dpi_x must be greater than zero")
    if dpi_y <= 0:
        raise ValueError("dpi_y must be greater than zero")
    if len(color) != 3:
        raise ValueError("color must contain exactly three components")
    if any(component < 0 or component > 255 for component in color):
        raise ValueError("color components must be between 0 and 255")

    pattern = _printer_pixel_pattern(
        width=width_in_pixels,
        height=height_in_pixels,
        mark_size=mark_size,
    )

    rgba = _pattern_to_rgba(
        pattern,
        color=color,
    )

    image = Image.new(
        "RGBA",
        (width_in_pixels, height_in_pixels),
    )

    pixels = [pixel for row in rgba for pixel in row]

    image.putdata(pixels)

    png_buffer = BytesIO()
    image.save(png_buffer, format="PNG")

    return Raster(
        origin=origin,
        width=width_in_pixels * 25.4 / dpi_x,
        height=height_in_pixels * 25.4 / dpi_y,
        png_data=png_buffer.getvalue(),
    )
