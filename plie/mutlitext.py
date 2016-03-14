from plie import Text
from plie.view import Bounds
class MultiText(Text):
    """ Able to display sequences of text in a well formatted way

    Args:
        texts: list of text strings to display
        bullet_choice: a string that will be used as the bullet for each list item
        justify: which justification to use for each list item
        bounds: bounding box specifying size in cells (x,y)

    """
    def __init__(self, texts = (), bullet_choice = '', justify = 'left', bounds = None):

        self.bullet_choice = bullet_choice
        #super().__init__(justify=justify, bounds=bounds)
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
        return '\n'.join([self.bullet_choice + str(t) for t in self.texts])

    def update(self, bounds=None, texts=None, specific_text=(), bullet_choice = None):
        """For changing internal state

        Args:
            bounds: update the bounds, either a tuple or a Bounds object
            texts: update the entire list of texts
            specific_text: a tuple of format (new_text_string, index)
            bullet_choice: update the bullet_choice

        Returns: nothing, but updates the internal state
        """
        if bounds:
            #TODO verify that this works
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
        """ Translates the internal state into a format for transferring

        Returns: a dictionary cell space representation of all the contained text objects
        """
        y_offset = 0
        for text_elem in self.texts: # text_elem is a Text instance
            elem_cells = text_elem.as_cells() # get the cells from the current Text instance
            #TODO make this handle more than just a height of 1
            # create x,y pairs for each cell in the ranges
            height, width = text_elem.height, text_elem.width
            for x, y in [(x, y) for y in range(text_elem.lines) for x in range(text_elem.width)]:
                # specify which cell in self.cells we're changing
                current_local_cell = (x, y + y_offset)
                # map the cell from the current Text instance to the appropriate self.cells cell
                self.cells[current_local_cell] = elem_cells[(x, y)]
            y_offset += text_elem.lines # update the offset, so the next one doesn't overlap
        return self.cells

    def _update_texts(self, texts):
        for text_elem in texts:

            elem_bounds = Bounds(self.width, text_elem.lines)
            self.texts.append(Text(text=text_elem, justify=self.justify, bounds=elem_bounds))