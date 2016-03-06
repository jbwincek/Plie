import plie
import pytest
from collections import namedtuple

Bounds = namedtuple('Bounds', 'width height')

def test_initialization():
    """
    tests that basic initialization works, including
    assigning bounds to a namedtuple

    """
    w_val = 20
    h_val = 30
    bounds = Bounds(width=w_val, height=h_val)
    t = plie.Text('some text', bounds=bounds)
    assert isinstance(t, plie.Text)
    assert t.width == w_val
    assert t.height == h_val

def test_bounds_as_tuple():
    """
    Tests to make sure bounds are required

    """
    w_val, h_val = 20, 30
    t = plie.Text('some text', bounds=(w_val,h_val))
    assert isinstance(t, plie.Text)
    assert t.width == w_val
    assert t.height == h_val

def test_bounds_needed_or_else_error():
    with pytest.raises(AttributeError):
        t = plie.Text('some text')

def test_string_to_cells_basic():
    """ Tests to make sure text objects are initialized well.
    This also tests left justification.
    """
    four_by_four_test_string = '123456789abcdefg'
    w_val, h_val = 4, 4
    t = plie.Text(four_by_four_test_string, bounds=(w_val,h_val))
    cells = t.display()
    assert cells[(0,0)] == '1' # first row
    assert cells[(1,0)] == '2' # checking order in first row
    assert cells[(2,0)] == '3' # continuing that
    assert cells[(3,3)] == 'g' # checking last cell in matrix

def test_center_justify():
    center_justify_test_string = 'abc def ghi'
    b = Bounds(width=5, height=5)
    t = plie.Text(center_justify_test_string, bounds=b, justify='centered')
    cells = t.display()
    for row_num in range(b.height):
        # check the edge columns that they're blank/empty
        assert cells.get((0, row_num), ' ') == ' '
        assert cells.get((4, row_num), ' ') == ' '

def test_right_justify():
    right_justify_test_string = 'abc def ghi jkl'
    b = Bounds(width=4, height=4)
    t = plie.Text(right_justify_test_string, bounds=b, justify='right')
    cells = t.display()
    for row_num in range(b.height):
        assert cells.get((3,row_num), ' ') != ' '