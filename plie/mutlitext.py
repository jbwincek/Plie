from textwrap import wrap
from plie.text import Text
from plie.view import Bounds

class DunFuckedUpError(Exception):
    pass

class MultiText(Text):
    """ MultiText displays sequences of text, including bulleted lists.

    MultiText can be used for lists of text, menus, and other things that involve multiple distinct
    elements of vertically arranged text.

    Args:
        texts: sequence of text strings to display (preferably immutable)
        bullet_choice: a string that will be used as the bullet for each list item
        justify: which justification to use for the list items
        bounds: bounding box specifying size in cells (x,y), usually set by Renderer

    """

    def __init__(self, texts=(), bullet_choice='', justify='left', bounds=None,
                 **kwargs):
        self.bullet_choice = bullet_choice
        self.justify = justify
        self.cells = {}
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
                self.width = 0
                self.height = 0

        self.texts = []
        if texts:
            self._update_texts(texts)


    def __repr__(self):
        return 'MultiText(texts=%r, bullet_choice=%r, justify=%r, bounds=%r)' % \
               (self.texts, self.bullet_choice, self.justify, (self.width, self.height))

    def __str__(self):
        """ creates a printable string of this instance

        Individual texts in in the MultiText instance are prefixed with self.bullet_choice,
        multiline texts have subsequent lines indented to where they start at an equal indent
        to the first line

        Returns: a printable string of the contents of this instance

        """
        lines = []
        for text_elem in self.texts:
            for i, line in enumerate(str(text_elem).split('\n')):
                if i == 0:
                    lines.append(self.bullet_choice + line)
                else:
                    blank_space = ' ' * self.term.length(self.bullet_choice)
                    lines.append(blank_space + line)
        return '\n'.join(lines)

    def __len__(self):
        return self.term.length(self.texts)

    def __getitem__(self, index):
        return self.texts[index]

    def update(self, bounds=None, texts=None, specific_text=(), bullet_choice=None):
        """For changing internal state

        Args:
            bounds: update the bounds, either a tuple or a Bounds object
            texts: update the entire list of texts
            specific_text: a tuple of format (new_text_string, index)
            bullet_choice: update the bullet_choice

        Returns: nothing, but updates the internal state
        """
        if bounds:
            # TODO verify that this works
            super()._update_bounds(bounds)
            for text_elem in self.texts:
                text_elem._update_bounds(bounds)
        if texts:
            self._update_texts(texts)
        if specific_text:
            try:
                self.texts[specific_text[1]].update(text=specific_text[0])
            except IndexError:
                raise IndexError("Index given ({}) for which text to update wasn't found".format(
                    specific_text[1]))
        if bullet_choice:
            self.bullet_choice = bullet_choice

    def as_cells(self):
        """ Translates the internal state into a cell space based format for transferring

        Returns: a dictionary cell space representation of all the contained text objects
        """

        # TODO see note:
        # NOTE:
        # This currently treats terminal escape sequences as normal characters, as such
        # it breaks line widths for strings with escape sequences. Terminal.length from
        # blessed will get the printable length of a string, it is based off of the
        # bless.Sequence class

        temp_lines = str(self).split('\n')
        output_lines = [ ]
        for line in temp_lines:
            output_lines.append(self.term.split_seqs(line))
        cells_to_output = {}
        for y in range(self.height):
            for x in range(self.width):
                try:
                    current_char = output_lines[y][x]
                    if self.term.length(current_char) == 0:
                        #raise DunFuckedUpError(repr(current_char + ' ({}, {})'.format(x,y)))
                        cells_to_output[(x, y)] = current_char + '--'
                    cells_to_output[(x, y)] = current_char
                except IndexError:
                    cells_to_output[(x, y)] = '.'
        return cells_to_output

    def _update_texts(self, texts):
        for text_elem in texts:
            if self.width:
                num_lines = len(self.term.wrap(text_elem, self.width, replace_whitespace=False))
                space_remaining_after_bullet = self.width - self.term.length(self.bullet_choice)
                elem_bounds = Bounds(space_remaining_after_bullet, num_lines)
                self.texts.append(Text(text=text_elem, justify=self.justify, bounds=elem_bounds))
            else:
                self.texts.append(Text(text=text_elem, justify=self.justify))

