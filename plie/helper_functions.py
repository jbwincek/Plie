from plie.styles import BORDER_STYLE


def array_insert(insertable,
                 receives_insertion,
                 offset=(2, 2),
                 highlight=False,
                 highlight_color='blue'):

    """ Inserts insertable into receives_insertion,

    array_insert will insert insertables bigger than receives_insertion can handle

    Args:
        insertable: string to insert
        receives_insertion: an FSArray to
        offset: distance from top left to start insertion.
            (x,y) format because that's the only reasonable way
        highlight: changes the coloring of the char to insert, used to make text look highlighted
        highlight_color: sets the color for showing the highlight, see curtsies foreground color
            choices for a list of possible options

    Notes:
        Goes character by character through insertable to add them one at a time to
        receives_insertion since that gets around the complication of making slice sizes with the
        length of strings trying to be inserted.
    """
    y = offset[1]
    for x, char in enumerate(insertable):
        if char in ('\n', '\r'):
            y += 1
        if highlight:
            receives_insertion[y, offset[0] + x] = fmtstr(char, fg=highlight_color)
        else:
            receives_insertion[y, offset[0] + x] = char
    return receives_insertion


def borderer(array=None, width=40, height=30, border_style='default'):
    """ Give it height and width, and it'll give you a bordered box as a FSArray.

    borderer consumes the outermost cell for border drawing.

    Args:
        array: FSArray to surround with a border
        width: of the border
        height: of the border
        border_style: the style of the border to use

    Returns: FSArray with a border surrounding it

    """

    # TODO update this to use cell dictionaries instead of relying on curtsies

    if not array:
        box_array = fsarray([' ' * width for _ in range(height)])
    else:
        box_array = array
    box_array[0, 0] = BORDER_STYLE[border_style]['top_left']
    box_array[0, width - 1] = BORDER_STYLE[border_style]['top_right']
    box_array[height - 1, 0] = BORDER_STYLE[border_style]['bottom_left']
    box_array[height - 1, width - 1] = BORDER_STYLE[border_style]['bottom_right']
    if width >= 3:  # fill space between corners if needed
        span = width - 2
        for index in range(span):
            box_array[0, index + 1] = BORDER_STYLE[border_style]['horizontal']
            box_array[height - 1, index + 1] = BORDER_STYLE[border_style]['horizontal']
    if height >= 3:
        span = height - 2
        for index in range(span):
            box_array[index + 1, 0] = BORDER_STYLE[border_style]['vertical']
            box_array[index + 1, width - 1] = BORDER_STYLE[border_style]['vertical']
    return box_array


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

