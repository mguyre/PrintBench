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
