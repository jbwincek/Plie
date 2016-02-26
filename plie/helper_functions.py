
def array_insert(insertable,
                 receives_insertion,
                 offset=(2, 2),
                 highlight=False,
                 highlight_color='blue'):

    """ inserts insertable into receives_insertion, where insertable is a string, and
    receives_insertion is an FSArray

    array_insert will insert insertables bigger than receives_insertion can handle

    Args:
        insertable: a string to insert
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



def borderer(array=None, width=40, height=30,):
    """ Give it height and width, and it'll give you a bordered box as a FSArray.

    borderer consumes the outermost cell for border drawing.

    Args:
        array: FSArray to surround with a border
        width: of the border
        height: of the border

    Returns: FSArray with a border surrounding it

    """
    top_left = '╒'
    top_right = '╕'
    bottom_left = '╘'
    bottom_right = '╛'
    horizontal = '═'
    vertical = '│'
    if not array:
        box_array = fsarray([' ' * width for _ in range(height)])
    else:
        box_array = array
    box_array[0, 0] = top_left
    box_array[0, width - 1] = top_right
    box_array[height - 1, 0] = bottom_left
    box_array[height - 1, width - 1] = bottom_right
    if width >= 3:  # fill space between corners if needed
        span = width - 2
        for index in range(span):
            box_array[0, index + 1] = horizontal
            box_array[height - 1, index + 1] = horizontal
    if height >= 3:
        span = height - 2
        for index in range(span):
            box_array[index + 1, 0] = vertical
            box_array[index + 1, width - 1] = vertical
    return box_array


def fit_text(text, array, margin=1, justification='left', vertical_position='top'):
    """ Fit and flow text into an array, splits words to newlines at spaces.

    Args:
        text: The text to fill the array with. Can include special characters, newlines and spaces.
        array: The FSArray to put the text into.
        margin: Amount of space to leave around the text in cells
        justification: acceptable options are 'left', 'right' and 'center'
        vertical_position: acceptable options are 'top', 'center', and 'bottom'

    Returns: an FSArray with the text filling the interior.

    """
    array_size = array.shape