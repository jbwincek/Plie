from blessed import Terminal


class Renderer:
    """ The thing that translates Views and View objects into actual text on the screen.

    Args:
        size: a tuple like, (width, height) in cells, if not specified Renderer will use the
            full terminal size
        view: a View instance

    """
    def __init__(self, size=None, view=None):
        """ Initialize the Renderer """

        self.term = Terminal()
        if not size:
            self.size = (self.term.width, self.term.height)
        else:
            try:
                self.size = (size[0], size[1])
            except TypeError:
                raise TypeError('size parameter should be a tuple-like object')

        self.dict = {}
        self.view_stack = []
        if view:
            self.add_view(view)

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
        Go through the view on the top of the view stack, and add everything it contains to the
        dict.

        """
        self.update()

        with self.term.fullscreen():
            print(self.formulate(), end='')

    def add_view(self, view):
        """ Add a view to the view stack, with a blank view underneath it if needed.

        Args:
            view: a View instance to add to the internal stack of Views

        """

        self.view_stack.append(view)

    def composite(self, view_object_dict, position = (0,0), size = (0,0)):
        """ given a view_object represented as a dictionary of cells of size and position, add that to
        the internal dict, at the correct position.

        Args:
            view_object_dict: a cell space dictionary representation of a view object
            position: where the top left corner should go
            size: how big it is


        """
        for y in range(size[1]):
            for x in range(size[0]):
                # TODO verify that using a .get method with the stand in value of ' ' is right
                self.dict[(x + position[0], y + position[1])] = view_object_dict.get((x,y), ' ')


    def update(self):
        """
        Update the internal dictionary cell space representation to match what's currently on the view stack

        """
        view = self.view_stack[-1]
        space_left_over_for_body = self.term.height
        if view.header:
            header_size = (self.term.width, 1)
            #TODO handle bounds (both percent and int style)
            view.header.view_object.update(bounds=header_size)
            self.composite(view.header.view_object.as_cells(),
                            position=(0,0),
                            size=header_size)
            space_left_over_for_body -= header_size[1] # remove header height from allotted space

        if view.footer:
            footer_size = (self.term.width, 1)
            # TODO handle bounds (both percent and int style)
            view.footer.view_object.update(bounds=footer_size)
            self.composite(view.footer.view_object.as_cells(),
                           position=(0, self.term.height-1),
                           size=footer_size)
            space_left_over_for_body -= footer_size[1] # remove footer height from allotted space

        if view.body:
            body_size = (self.term.width, space_left_over_for_body)
            # TODO handle bounds (both percent and int style)
            view.body[0].view_object.update(bounds=body_size)

            self.composite(view.body[0].view_object.as_cells(),
                           position=(0, 1),
                           size=body_size)



    def _insert_blanking_view(self):
        """ Adds a view to the stack of spaces to stop translucency
        """
        pass