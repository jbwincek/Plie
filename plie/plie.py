
from contextlib import contextmanager


from curtsies import FSArray, FullscreenWindow, Input
from plie.helper_functions import array_insert, borderer

"""
Notes on this file: This is an attempt to use context managers to composite shape renderings
around other things. More simply, puts borders around text.
"""




@contextmanager
def border(array, border_style='default'):
    """ Context manager to put a border around any array.

        Uses the outermost cell of the array on all sides to create the border, so if there is
        content there it will get overwritten.

        Args:
            array: an FSArray to have a border made around it
            border_style: the style of the border to use
    """
    array_size = array.shape # property with format (num_rows, num_columns)
    yield borderer(array, height=array_size[0], width=array_size[1], border_style=border_style)


@contextmanager
def simple_title(array, text='Title', offset=0):
    """ Adds a title bar to the top of an FSArray.

    Args:
        array:  an FSArray to have the title added to
        text:   the text which gets used as a title, can be multiple lines
        offset: the offset in cells from the top to place the title (0 would overlap a border)
    """
    yield array_insert(text, array, offset=(1,offset))


class TitleBar():
    """  A context manager to add a title to the top of a FSArray

    Args:
        array: The array to add the title bar to
        text: What the title should say
        offset: how far in cells from the top to put the title, default is at top,
        which overlaps the border (if there is one).
    """
    def __init__(self, array, text='Title', offset=0):
        self._text = text
        self.array = array_insert(self._text, array, offset=(1, offset))
        self.offset = offset

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    @property
    def text(self):
        return self.text

    @text.setter
    def text(self, text):
        """ Automatically updates title text upon setting """
        self._text = text
        self.array = array_insert(self._text, self.array, offset=(1, self.offset))


class PopUp():
    """ Show a popup notification style message with text for a brief period of time

    Args:
        window: the window in which to show the popup
        text: the text to display, can contain newlines
        delay: the amount of time to show the popup
    """
