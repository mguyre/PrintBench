from printbench import StrokeStyle


def test_stroke_style_contains_solid():
    assert StrokeStyle.SOLID.value == "solid"


def test_stroke_style_contains_dashed():
    assert StrokeStyle.DASHED.value == "dashed"


def test_stroke_style_contains_dotted():
    assert StrokeStyle.DOTTED.value == "dotted"


def test_stroke_style_contains_centerline():
    assert StrokeStyle.CENTERLINE.value == "centerline"
