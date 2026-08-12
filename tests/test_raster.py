import pytest

from printbench.geometry import Point, Raster


def test_raster_stores_values():
    origin = Point(12.3, 45.6)
    png_data = b"pretend png data"

    raster = Raster(
        origin=origin,
        width=7.89,
        height=6.54,
        png_data=png_data,
    )

    assert raster.origin == origin
    assert raster.width == pytest.approx(7.89)
    assert raster.height == pytest.approx(6.54)
    assert raster.png_data == png_data


def test_raster_rejects_zero_width():
    with pytest.raises(ValueError):
        Raster(
            origin=Point(12.3, 45.6),
            width=0.0,
            height=6.54,
            png_data=b"pretend png data",
        )


def test_raster_rejects_negative_width():
    with pytest.raises(ValueError):
        Raster(
            origin=Point(12.3, 45.6),
            width=-7.89,
            height=6.54,
            png_data=b"pretend png data",
        )


def test_raster_rejects_zero_height():
    with pytest.raises(ValueError):
        Raster(
            origin=Point(12.3, 45.6),
            width=7.89,
            height=0.0,
            png_data=b"pretend png data",
        )


def test_raster_rejects_negative_height():
    with pytest.raises(ValueError):
        Raster(
            origin=Point(12.3, 45.6),
            width=7.89,
            height=-6.54,
            png_data=b"pretend png data",
        )


def test_raster_is_immutable():
    raster = Raster(
        origin=Point(12.3, 45.6),
        width=7.89,
        height=6.54,
        png_data=b"pretend png data",
    )

    with pytest.raises(AttributeError):
        raster.width = 1.23
