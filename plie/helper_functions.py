from plie.styles import BORDER_STYLE
from plie.view import Bounds


def borderer(cells, bounds, border_style='default'):
    """ Give it a dict of cells, and the size of the area, and it'll border it for you.

    Args:
        cells: dict of cells, with keys of format (x,y) and values as single character strings
        bounds: the width and height of the area to apply a border to
        border_style: specifies which border style to use

    Returns: a cell space dict that now has a border around it

    """
    if isinstance(bounds, (list,tuple)):
        try:
            bounds = Bounds(width = bounds[0], height=bounds[1])
        except IndexError:
            raise IndexError('bounds passed was not a pair')
    elif isinstance(bounds, Bounds):
        pass
    else:
        raise AttributeError('bounds passed was not in a comprehensible format, try using a Bounds '
                             'object')

    new_cells = cells
    new_cells[(0,0)] = BORDER_STYLE[border_style]['top_left']
    new_cells[(bounds.width - 1,0 )] = BORDER_STYLE[border_style]['top_right']
    new_cells[(0, bounds.height - 1)] = BORDER_STYLE[border_style]['bottom_left']
    new_cells[(bounds.width - 1, bounds.height - 1)] = BORDER_STYLE[border_style]['bottom_right']
    if bounds.width >= 3:
        span = bounds.width - 2
        for x in range(1, span+1): #offset by one to not mess up the corners
            new_cells[(x,0)] = BORDER_STYLE[border_style]['horizontal']
            new_cells[(x, bounds.height-1)] = BORDER_STYLE[border_style]['horizontal']
    if bounds.height >= 3:
        span = bounds.height -2
        for y in range(1, span+1):
            new_cells[(0,y)] = BORDER_STYLE[border_style]['vertical']
            new_cells[(bounds.width-1, y)] = BORDER_STYLE[border_style]['vertical']

    return new_cells


def fit_text(text, array, margin=1, justification='left', vertical_position='top', indent=False,
             truncate=True) :
    """ Fit and flow text into an array, splits words to newlines at spaces.

    Args:
        text: The text to fill the array with. Can include special characters, newlines and spaces.
        array: The FSArray to put the text into.
        margin: Amount of space to leave around the text in cells
        justification: acceptable options are 'left', 'right' and 'center'
        vertical_position: acceptable options are 'top', 'center', and 'bottom'
        indent: whether or not to indent the first line of paragraphs
        truncate: specifies whether or not to truncate text, if false, raise AttributeError

    Returns: an FSArray with the text filling the interior.

    Raises:
        AttributeError: if the string is too long to fit in the array, and truncate is set to False

    """
    array_height, array_width = array.shape


def backgrounder(cells, bounds, background = '.'):
    """Replace all empty cells with the specified background cell

    Notes:
        'empty' cells means cells with actually nothing in them, cells with spaces
        in them will be left unmodified.

    Args:
        cells: dictionary of cells with keys of style (x,y)
        bounds: of the region to background, in format (width, height)
        background: the character to replace empty cells with

    Returns: a cell space dictionary with empty cells replaced

    """
    new_cells = {}
    if isinstance(bounds, (list, tuple)):
        try:
            bounds = Bounds(width=bounds[0], height=bounds[1])
        except IndexError:
            raise IndexError('bounds passed was not a pair')
    elif isinstance(bounds, Bounds):
        pass
    else:
        raise AttributeError('bounds passed was not in a comprehensible format, try using a Bounds '
                             'object')

    for x, y in [(x,y) for y in range(bounds.height) for x in range(bounds.width)]:
        cell = cells.get((x,y), '')
        if cell == '':
            new_cells[(x,y)] = background
        else:
            new_cells[(x, y)] = cell

    return new_cells

