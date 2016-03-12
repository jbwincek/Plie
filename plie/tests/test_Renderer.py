import plie
from blessed import Terminal
from collections import namedtuple
import pytest


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
    valid_options = [' ', '\n']  # newline char instead of term signal
    #valid_options = [' ', str(term.move_down)]
    for char in output:
        assert char in valid_options

def test_extract_bounds_basic_case():
    """
    Tests for if it handles an int

    Returns: a dot
    """
    r = plie.Renderer()
    b = plie.Bounds(width=10,height=10)
    output = r._extract_bounds_information(b,(25,25))
    assert output.width == 10 and output.height == 10

def test_extract_bounds_just_percentages():
    """
    Tests for if it handles an int

    Returns: a dot
    """
    r = plie.Renderer()
    b = plie.Bounds(width='10%',height='10%')
    output = r._extract_bounds_information(b,(100,100))
    assert output.width == 10 and output.height == 10


def test_extract_bounds_percentages_with_addition():
    """
    Tests for if it handles an int

    Returns: a dot
    """
    r = plie.Renderer()
    b = plie.Bounds(width='10%+1',height='10%+1')
    output = r._extract_bounds_information(b,(100,100))
    assert output.width == 11 and output.height == 11

def test_extract_bounds_percentages_with_subtraction():
    """
    Ensures handling of subtraction works as expected

    Returns: a dot
    """
    r = plie.Renderer()
    b = plie.Bounds(width='10%-1',height='10%-1')
    output = r._extract_bounds_information(b,(100,100))
    assert output.width == 9 and output.height == 9

def test_extract_bounds_badly_formatted():
    with pytest.raises(ValueError):
        r = plie.Renderer()
        b = plie.Bounds(width='something', height='random')
        output = r._extract_bounds_information(b, (100, 100))

def test_extract_bounds_negative_percentages_error():
    """
    Makes sure negative percentages raise an error

    Returns: a dot
    """
    r = plie.Renderer()
    b = plie.Bounds(width='-10%',height='-10%')
    with pytest.raises(ValueError):
        output = r._extract_bounds_information(b,(100,100))