from collections import namedtuple
from functools import partial
from typing import Sequence
from textwrap import wrap


class Text:
    """ Text is the universal class for dealing with all single text snippets.
    Args:
        text: the text to display (can be changed later
        callout: an attribute made available for storing an attribute, it is used
                 if this Text object gets selected by some event.
        justify: specifies which justification the text should have, options are:
                 'left' where all the text aligns with the left edge,
                 'centered' where all the text is centered in the middle of the,
                            available space
                 'right' where all the text aligns with the right edge
        bounds: the bounding box for the Text object in screen space cells, will
                be set automatically by Renderer usually
    """
    def __init__(self,
                 text:str='',
                 callout:callable=None,
                 justify:str='left',
                 bounds:Sequence=None):
        self.text = text
        self.callout = callout
        self.justify = justify
        self.cells = {}
        try:
            # preferred method for handling bounds (as a namedtuple)
            self.width = bounds.width
            self.height = bounds.height
        except AttributeError:
            if isinstance(bounds, (list,tuple)):
                # fall back if it's not a namedtuple, uses format (width, height)
                self.width = bounds[0]
                self.height = bounds[1]
            else:
                raise AttributeError('bounds must be specified')


    def update(self, bounds:Sequence=None, text:str=None, **kwargs):
        """ For changing internal state, including updating the text to display.

        update() accepts **kwargs, so any keyword argument passed during initialization can be
        passed again, to change the stored value.

        Returns: True if updating went well
        """
        pass

    def display(self):
        """ Translates the internal state and translates it into a screen-space cell dict of size
        bounds

        Returns: Dictionary with keys of format (x,y), of size bounds and single character
        strings as the values.

        """
        operation = {'left': partial(str.ljust),
                     'centered': partial(str.center),
                     'right': partial(str.rjust)}

        lines = wrap(self.text, self.width)
        formatted = []
        for line in lines:
            # apply the appropriate string method to each line
            formatted.append(operation[self.justify](line, self.width))

        # Add each cell to the dictionary
        for y, line in enumerate(formatted):
            for x, char in enumerate(line):
                self.cells[(x, y)] = char

        return self.cells


    def _update_by_cell(self, cell:tuple, char:str ):
        """ Update a particular cell in the internal dictionary

        Args:
            cell: A tuple specifying which cell to modify
            char: A single character string to change the cell too.

        """
        pass
