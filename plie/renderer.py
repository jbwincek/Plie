from blessed import Terminal
from plie.view import Bounds
import re


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
                raise TypeError('Size parameter should be a tuple-like object: (width, height)')
        self.dict = {}
        self.view_stack = []
        if view:
            self.add_view(view)
            # regex's for bounds matching

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
        self.update()

    def composite(self, view_object_dict, position=(0, 0), size=(0, 0)):
        """ given a view_object represented as a dictionary of cells of size and position, add that to
        the internal dict, at the correct position.

        Args:
            view_object_dict: a cell space dictionary representation of a view object
            position: where the top left corner should go
            size: how big it is


        """
        for x, y in [(x, y) for y in range(size[1]) for x in range(size[0])]:
            # TODO verify that using a .get method with the stand in value of ' ' is right
            self.dict[(x + position[0], y + position[1])] = view_object_dict.get((x, y), ' ')

    def update(self):
        """
        Update the internal dictionary cell space representation to match what's currently on the view stack

        """
        view = self.view_stack[-1]
        space_left_over_for_body = self.term.height
        if view.header:
            header_size = (self.term.width, 1)
            try:
                header_size = self._extract_bounds_information(view.header.bounds, header_size)
            except (KeyError, IndexError):
                pass
            view.header.view_object.update(bounds=header_size)
            self.composite(view.header.view_object.as_cells(),
                           position=(0, 0),
                           size=header_size)
            space_left_over_for_body -= header_size[1]  # remove header height from allotted space

        if view.footer:
            footer_size = (self.term.width, 1)
            try:
                footer_size = self._extract_bounds_information(view.footer.bounds, footer_size)
            except (KeyError, IndexError):
                pass
            view.footer.view_object.update(bounds=footer_size)
            self.composite(view.footer.view_object.as_cells(),
                           position=(0, self.term.height - 1),
                           size=footer_size)
            space_left_over_for_body -= footer_size[1]  # remove footer height from allotted space

        if view.body:
            body_size = (self.term.width, space_left_over_for_body)
            try:
                body_size = self._extract_bounds_information(view.body[0].bounds, body_size)
            except (KeyError, IndexError):
                pass
            view.body[0].view_object.update(bounds=body_size)
            self.composite(view.body[0].view_object.as_cells(),
                           position=(0, 1),
                           size=body_size)

    def _insert_blanking_view(self):
        """ Adds a view to the stack of spaces to stop translucency
        """
        pass

    @staticmethod
    def _extract_bounds_information(bounds_representation, available_space):
        """ Figures out bounding box size from a variety of input formats

        Args:
            bounds_representation: a representation of bounds which can be a number pair as a
            string or ints, or percentages as strings with optional addition and subtraction of
            cells components
            available_space: 50% takes up half the space of this quantity, used to translate the
            percentages into amount of cells

        Returns: A Bounds namedtuple specifying in cells how big the thing passed to it would be.

        """
        if isinstance(available_space, (tuple, list)):
            # cast available space to a namedtuple if it is not
            available_space = Bounds(width=available_space[0], height=available_space[1])
        elif not isinstance(available_space, Bounds):
            raise ValueError('expected available_space as a sequence or namedtuple')

        pattern = re.compile(r"(?P<percent>\d{1,4})%( *(?P<operator>[-+]) *(?P<amount>\d+)){0,1}")

        if isinstance(bounds_representation, Bounds):
            if isinstance(bounds_representation.width, str):  # 10% (+5) cases
                width_match = re.match(pattern, bounds_representation.width)
                if width_match:
                    width_percentage = float(width_match.group('percent')) * .01
                    temp_width = round(available_space.width * width_percentage)
                    if width_match.group('operator') and width_match.group('amount'):  # 10%+5 cases
                        if width_match.group('operator') == '+':
                            width = temp_width + int(width_match.group('amount'))
                        else:
                            width = temp_width - int(width_match.group('amount'))
                    else:  # 10% case
                        width = temp_width
                else:
                    if bounds_representation.width[0] == '-':
                        raise ValueError('Negative percentages for bounds are not supported')
                    else:
                        raise ValueError('Could not find relevant information in width')
            else:  # 40 case
                try:
                    width = int(bounds_representation.width)
                except ValueError:
                    raise ValueError('bounds.width is not in a supported format: {}'.format(
                        bounds_representation.width))

            if isinstance(bounds_representation.height, str):  # 10% (+5) cases
                height_match = re.match(pattern, bounds_representation.height)
                if height_match:
                    height_percentage = float(height_match.group('percent')) * .01
                    temp_height = round(available_space.height * height_percentage)
                    if height_match.group('operator') and height_match.group(
                            'amount'):  # 10%+5 cases
                        if height_match.group('operator') == '+':
                            height = temp_height + int(height_match.group('amount'))
                        else:
                            height = temp_height - int(height_match.group('amount'))
                    else:  # 10% case
                        height = temp_height
                else:
                    if bounds_representation.height[0] == '-':
                        raise ValueError('Negative percentages for bounds are not supported')
                    else:
                        raise ValueError('Could not find relevant information in height')
            else:  # 40 case
                try:
                    height = int(bounds_representation.height)
                except ValueError:
                    raise ValueError('bounds.height is not in a supported format: {}'.format(
                        bounds_representation.height))
        else:  # bounds is just a (num,num) pair of some sort or badly formatted
            try:
                width = int(bounds_representation[0])
                height = int(bounds_representation[1])
            except TypeError:
                raise ValueError('Bounds was not a comprehensible format')

        return Bounds(width=width, height=height)
