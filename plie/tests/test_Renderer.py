import plie
from blessed import Terminal
from collections import namedtuple


def test_for_blank_rendering_length():
    """
    Tests that formulating an empty view returns a string of correct length

    Notes:
        The checksize is 109 because 10*10 + moving down 9 times to cover each row
    """
    term = Terminal()
    width = 10
    height = 10
    r = plie.Renderer(size=(width,height), view={})
    output = r.formulate()
    assert len(output) == 109


def test_for_blank_rendering_content():
    """
    Tests that formulating an empty view returns a string filled with spaces
    and bless.Terminal.move_down characters.
    """
    term = Terminal()
    width = 10
    height = 10
    r = plie.Renderer(size=(width,height), view={})
    output = r.formulate()
    valid_options = [' ', str(term.move_down)]
    for char in output:
        assert char in valid_options
