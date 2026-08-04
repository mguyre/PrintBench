from printbench import Style


def test_new_style_defaults_to_none():
    style = Style()

    assert style.stroke_color is None
    assert style.stroke_width is None
    assert style.stroke_style is None


# def test_style_stores_values():

# def test_style_is_immutable():
