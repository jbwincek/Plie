from blessed import Terminal


class Renderer():
    def __init__(self, size=(10,10), view=None):
        self.term = Terminal
        self.size = size
        self.dict = {}

    def formulate(self):
        """ Turns the internal dictionary into a string for rendering.

        Returns: A string that could render the whole screen if printed.
        """
        output_list = []
        for y in range(self.size[1]):
            if y > 0:
                output_list.append('\n')
            output_list.extend([self.dict.get((x, y), ' ') for x in range(self.size[0])])
        return ''.join(output_list)

    def display(self):
        """

        """
        pass

    def add_view(self):
        """
        Add a view to the view stack, with a blank view underneath it if needed.
        """
        pass

    def composite(self):
        """
        given a dict of size and position, add that to the internal dict, at the correct position.
        """
        pass

    def _insert_blanking_view(self):
        """ Adds a view to the stack of spaces to stop translucency
        """
        pass