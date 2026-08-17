from io import BytesIO

import pytest
from PIL import Image

from printbench.geometry import Point, Raster
from printbench.qualification.printer_pixels import (
    _pattern_to_rgba,
    _printer_pixel_pattern,
    printer_pixel_raster,
)


def test_printer_pixel_pattern_one_pixel_marks():
    pattern = _printer_pixel_pattern(
        width=8,
        height=4,
        mark_size=1,
    )

    assert pattern == [
        [1, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 1],
    ]


def test_printer_pixel_pattern_two_pixel_marks():
    pattern = _printer_pixel_pattern(
        width=16,
        height=8,
        mark_size=2,
    )

    assert pattern == [
        [1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
    ]


def test_printer_pixel_pattern_four_pixel_marks():
    pattern = _printer_pixel_pattern(
        width=32,
        height=16,
        mark_size=4,
    )

    first_mark_row = [1] * 4 + [0] * 12 + [1] * 4 + [0] * 12
    second_mark_row = [0] * 4 + [1] * 4 + [0] * 12 + [1] * 4 + [0] * 8

    assert pattern[0] == first_mark_row
    assert pattern[3] == first_mark_row

    assert pattern[4] == second_mark_row
    assert pattern[7] == second_mark_row


def test_pattern_to_rgba():
    pattern = [
        [1, 0],
        [0, 1],
    ]

    rgba = _pattern_to_rgba(
        pattern,
        color=(17, 83, 191),
    )

    assert rgba == [
        [(17, 83, 191, 255), (0, 0, 0, 0)],
        [(0, 0, 0, 0), (17, 83, 191, 255)],
    ]


def test_pattern_to_rgba_with_white():
    pattern = [
        [1, 0],
        [0, 1],
    ]

    rgba = _pattern_to_rgba(
        pattern,
        color=(255, 255, 255),
    )

    assert rgba == [
        [(255, 255, 255, 255), (0, 0, 0, 0)],
        [(0, 0, 0, 0), (255, 255, 255, 255)],
    ]


def test_printer_pixel_raster_dimensions():
    raster = printer_pixel_raster(
        origin=Point(12.3, 45.6),
        width_in_pixels=8,
        height_in_pixels=4,
        mark_size=1,
        color=(17, 83, 191),
        dpi_x=720,
        dpi_y=720,
    )

    assert isinstance(raster, Raster)

    assert raster.origin == Point(12.3, 45.6)
    assert raster.width == pytest.approx(8 * 25.4 / 720)
    assert raster.height == pytest.approx(4 * 25.4 / 720)


def test_printer_pixel_raster_png_data():
    raster = printer_pixel_raster(
        origin=Point(12.3, 45.6),
        width_in_pixels=8,
        height_in_pixels=4,
        mark_size=1,
        color=(17, 83, 191),
        dpi_x=720,
        dpi_y=720,
    )

    image = Image.open(BytesIO(raster.png_data))

    assert image.size == (8, 4)
    assert image.mode == "RGBA"

    assert list(image.get_flattened_data()) == [
        (17, 83, 191, 255),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (17, 83, 191, 255),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (17, 83, 191, 255),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (17, 83, 191, 255),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (17, 83, 191, 255),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (17, 83, 191, 255),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (17, 83, 191, 255),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (17, 83, 191, 255),
    ]


def test_printer_pixel_raster_rejects_nonpositive_width():
    with pytest.raises(
        ValueError,
        match="width_in_pixels must be greater than zero",
    ):
        printer_pixel_raster(
            origin=Point(12.3, 45.6),
            width_in_pixels=0,
            height_in_pixels=4,
            mark_size=1,
            color=(17, 83, 191),
        )


def test_printer_pixel_raster_rejects_nonpositive_height():
    with pytest.raises(
        ValueError,
        match="height_in_pixels must be greater than zero",
    ):
        printer_pixel_raster(
            origin=Point(12.3, 45.6),
            width_in_pixels=8,
            height_in_pixels=0,
            mark_size=1,
            color=(17, 83, 191),
        )


def test_printer_pixel_raster_rejects_nonpositive_mark_size():
    with pytest.raises(
        ValueError,
        match="mark_size must be greater than zero",
    ):
        printer_pixel_raster(
            origin=Point(12.3, 45.6),
            width_in_pixels=8,
            height_in_pixels=4,
            mark_size=0,
            color=(17, 83, 191),
        )


def test_printer_pixel_raster_rejects_nonpositive_dpi_x():
    with pytest.raises(
        ValueError,
        match="dpi_x must be greater than zero",
    ):
        printer_pixel_raster(
            origin=Point(12.3, 45.6),
            width_in_pixels=8,
            height_in_pixels=4,
            mark_size=1,
            color=(17, 83, 191),
            dpi_x=0,
            dpi_y=720,
        )


def test_printer_pixel_raster_rejects_nonpositive_dpi_y():
    with pytest.raises(
        ValueError,
        match="dpi_y must be greater than zero",
    ):
        printer_pixel_raster(
            origin=Point(12.3, 45.6),
            width_in_pixels=8,
            height_in_pixels=4,
            mark_size=1,
            color=(17, 83, 191),
            dpi_x=720,
            dpi_y=0,
        )


def test_printer_pixel_raster_rejects_color_component_out_of_range():
    with pytest.raises(
        ValueError,
        match="color components must be between 0 and 255",
    ):
        printer_pixel_raster(
            origin=Point(12.3, 45.6),
            width_in_pixels=8,
            height_in_pixels=4,
            mark_size=1,
            color=(17, 83, 256),
        )


def test_printer_pixel_raster_rejects_invalid_color_length():
    with pytest.raises(
        ValueError,
        match="color must contain exactly three components",
    ):
        printer_pixel_raster(
            origin=Point(12.3, 45.6),
            width_in_pixels=8,
            height_in_pixels=4,
            mark_size=1,
            color=(17, 83),
        )
