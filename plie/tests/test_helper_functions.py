from plie.helper_functions import borderer
from plie.helper_functions import backgrounder
from plie.text import Text

def test_borderer_basic():
    test_cells = {
        (0, 0): ' ',
        (0, 1): ' ',
        (0, 2): ' ',
        (1, 0): ' ',
        (1, 1): 'a',
        (1, 2): ' ',
        (2, 0): ' ',
        (2, 1): ' ',
        (2, 2): ' ',
    }
    expected_result_cells = {
        (0, 0): '╒',
        (0, 1): '│',
        (0, 2): '╘',
        (1, 0): '═',
        (1, 1): 'a',
        (1, 2): '═',
        (2, 0): '╕',
        (2, 1): '│',
        (2, 2): '╛',
    }
    got_cells = borderer(test_cells,(3,3))
    assert got_cells == expected_result_cells


def test_borderer_rounded():
    test_cells = {
        (0, 0): ' ',
        (0, 1): ' ',
        (0, 2): ' ',
        (1, 0): ' ',
        (1, 1): 'a',
        (1, 2): ' ',
        (2, 0): ' ',
        (2, 1): ' ',
        (2, 2): ' ',
    }
    expected_result_cells = {
        (0, 0): '╭',
        (0, 1): '│',
        (0, 2): '╰',
        (1, 0): '─',
        (1, 1): 'a',
        (1, 2): '─',
        (2, 0): '╮',
        (2, 1): '│',
        (2, 2): '╯',
    }
    got_cells = borderer(test_cells,(3,3), border_style='rounded')
    assert got_cells == expected_result_cells


def test_backgrounder():
    test_cells = {
        (0, 0): '',
        (0, 1): '',
        (0, 2): '',
        (1, 0): '',
        (1, 1): 'a',
        (1, 2): '',
        (2, 0): '',
        (2, 1): '',
        (2, 2): '',
    }
    # holy cow that's ☟ hard to read
    expected_cells = {
        (0, 0): '.',
        (0, 1): '.',
        (0, 2): '.',
        (1, 0): '.',
        (1, 1): 'a',
        (1, 2): '.',
        (2, 0): '.',
        (2, 1): '.',
        (2, 2): '.',
    }
    got_cells = backgrounder(test_cells, (3,3))
    assert got_cells == expected_cells