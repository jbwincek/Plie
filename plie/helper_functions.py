from plie.styles import BORDER_STYLE
from plie.view import Bounds
from plie.cellspace import CellSpace


def borderer(bounds, cells=None, term=None, border_style='default'):
    """ Creates a border around an area of the given size

    borderer will work with either just a size parameter, producing only the cells for the border,
    or for applying a border to an already filled cell space

    Args:
        bounds: the width and height of the area to apply a border to
        cells: dict of cells, with keys of format (x,y) and values as single character strings
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

    if not cells:
        new_cells = CellSpace()
    else:
        new_cells = cells
    new_cells[(0, 0)] = BORDER_STYLE[border_style]['top_left']
    new_cells[(bounds.width - 1, 0)] = BORDER_STYLE[border_style]['top_right']
    new_cells[(0, bounds.height - 1)] = BORDER_STYLE[border_style]['bottom_left']
    new_cells[(bounds.width - 1, bounds.height - 1)] = BORDER_STYLE[border_style]['bottom_right']
    if bounds.width >= 3:
        span = bounds.width - 2
        for x in range(1, span+1):  # offset by one to not mess up the corners
            new_cells[(x, 0)] = BORDER_STYLE[border_style]['horizontal']
            new_cells[(x, bounds.height-1)] = BORDER_STYLE[border_style]['horizontal']
    if bounds.height >= 3:
        span = bounds.height - 2
        for y in range(1, span + 1):
            new_cells[(0, y)] = BORDER_STYLE[border_style]['vertical']
            new_cells[(bounds.width-1, y)] = BORDER_STYLE[border_style]['vertical']

    return new_cells


def backgrounder(bounds, cells=None, background='.', term=None):
    """Replace all empty cells with the specified background cell,
        or fill size bounds with background str

    Notes:
        'empty' cells means cells with actually nothing in them, cells with spaces
        in them will be left unmodified.

    Args:
        bounds: of the region to background, in format (width, height)
        cells: dictionary of cells with keys of style (x,y)
        background: the character to replace empty cells with

    Returns: a cell space dictionary with empty cells replaced

    """
    if not cells:
        cells = CellSpace()

    new_cells = CellSpace()
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

