from printbench.qualification.printer_pixels import (
    _pattern_to_rgba,
    _printer_pixel_pattern,
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
