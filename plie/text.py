from collections import namedtuple
from functools import partial
from textwrap import wrap


class Text:
    """ Text is the universal class for dealing with all single text snippets.

    Text helps with basic formatting, justification, word wrapping to the appropriate width and
    acts as a way to contain a block of text for applying styles to it or developing a
    layout.

    Args:
        text: the text to display (can be changed later

        callout: an attribute made available for storing a function, it is used if this Text object
            gets selected by some event.

        justify: specifies which justification the text should have, options are:
            'left' where all the text aligns with the left edge,
            'center' where all the text is centered in the middle of the, available space
            'right' where all the text aligns with the right edge

        bounds: the bounding box for the Text object in screen space cells, will be set
            automatically by Renderer usually

    Returns: an initialized Text object

        """
    def __init__(self, text='', callout=None, justify='left', bounds=None, replace_whitespace=True):
        self.callout = callout
        self.justify = justify
        self.cells = {}
        self._replace_whitespace = replace_whitespace
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
                self.width = 0
                self.height = 0
        if self.width:
            self.text = '\n'.join(wrap(text, self.width, replace_whitespace=self._replace_whitespace))
        else:
            self.text = text

    def __repr__(self):
        return 'Text(text=%r, callout=%r, justify=%r, bounds=%r)' % (self.text, self.callout,
                                                               self.justify, (self.width,
                                                                              self.height))
    def __str__(self):
        # TODO decide if this should have styling and formatting applied to it
        return self.text

    def update(self, bounds=None, text=None, **kwargs):
        """For changing internal state, including updating the text to display.

        update() accepts ``**kwargs``, so any keyword argument passed during initialization can be
        passed again, to change the stored value.

        Returns: True if updating went well
        """
        if bounds:
            self._update_bounds(bounds)
        if text:
            if self.width:
                self.text = '\n'.join(wrap(text, self.width, replace_whitespace=self._replace_whitespace))
            else:
                self.text = text
        if kwargs.get('callout', False):
            self.callout = kwargs['callout']
        if kwargs.get('justify', False):
            self.justify = kwargs['justify']
        if kwargs.get('replace_whitespace', False):
            self._replace_whitespace = kwargs['replace_whitespace']

    @property
    def lines(self):
        """
        Returns: the number of lines that the Text instance uses
        """
        return len(self.text.split('\n'))

    def as_cells(self):
        """ Translates the internal state and translates it into a screen-space cell dict of size
        bounds

        Returns: Dictionary with keys of format (x,y), of size bounds and single character
        strings as the values.

        """
        operation = {'left': partial(str.ljust),
                     'center': partial(str.center),
                     'right': partial(str.rjust)}

        lines = self.text.split('\n')
        formatted = []
        for line in lines:
            # apply the appropriate string method to each line
            formatted.append(operation[self.justify](line, self.width))

        # Add each cell to the dictionary
        for x, y in [(x, y) for y in range(self.height) for x in range(self.width)]:
            try:
                self.cells[(x,y)] = formatted[y][x]
            except IndexError:
                self.cells[(x,y)] = ' '

        return self.cells

    def _update_by_cell(self, cell, char):
        """ Update a particular cell in the internal dictionary

        Args:
            cell: A tuple specifying which cell to modify
            char: A single character string to change the cell too.

        """
        pass

    def _update_bounds(self, bounds):
        try:
            # preferred method for handling bounds (as a namedtuple)
            self.width = bounds.width
            self.height = bounds.height
        except AttributeError:
            if isinstance(bounds, (list, tuple)):
                # fall back if it's not a namedtuple, uses format (width, height)
                self.width = bounds[0]
                self.height = bounds[1]
            else:
                pass