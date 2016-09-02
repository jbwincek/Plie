from blessed import Terminal
from collections import ChainMap
from numbers import Integral
import plie
from plie import Bounds
from plie import CellSpace
from plie.defaults import default_sections
import re


class RendererOld:
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
            # TODO verify that using a .get method with the stand in value of '' is right
            self.dict[(x + position[0], y + position[1])] = view_object_dict.get((x, y), '')

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
            # currently, this just makes the view_object take up the entire space for body
            # which completely disregards the size that someone might set for a view_object
            # this seems very wrong, especially since using positioning won't work until the object
            # doesn't take up the whole space.
            body_size = (self.term.width, space_left_over_for_body)
            try:
                body_size = self._extract_bounds_information(view.body[0].bounds, body_size)
            except (KeyError, IndexError):
                pass
            try:
                position = self._calculate_position(view.body[0].positioning, body_size,)
            except AttributeError:
                position = (0,1)
            view.body[0].view_object.update(bounds=body_size)
            self.composite(view.body[0].view_object.as_cells(),
                           position=position,
                           size=body_size)

    def _insert_blanking_view(self):
        """ Adds a view to the stack of spaces to stop translucency
        """
        pass

    def _calculate_position(self, positioning, available_space, size_of_object):
        """ Calculates exact

        Args:
            positioning: a Position object specifying where in the available space this thing
                should be placed.
                vertical has three options: 'top', 'centered', 'bottom'
                horizontal has three options: 'left', 'centered', 'bottom'
            available_space: the bounds used to specify the available space to position this
                object in
            size_of_object: how big the object we're positioning is.

        Returns: a coordinate pair tuple of where to put the top left corner
        """


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


class Renderer():
    def __init__(self, size=None, view=None, terminal=None):
        if not terminal:
            self.term = Terminal()
        else:
            self.term = terminal
        if not size:
            self.size = (self.term.width, self.term.height)
        else:
            try:
                self.size = (size[0], size[1])
            except TypeError:
                raise TypeError('Size parameter should be a tuple-like object: (width, height)')

        self.default_sections = default_sections
        self.cells = CellSpace()

        if view:
            self.add_view(view)
        else:
            self.view = {}

    def add_view(self, view):
        """ Take in a valid view dict, and initialize anything that needs initializing,
        then store it ready for displaying

        Notes:
            To initialize in this context means find the size for each Renderable, by examining
            the bounds, padding and positioning. So that when the Renderable is initialized,
            it can start at the appropriate size.
            The instance of the Renderable for each renderable section then gets added to that
            section.

            Sections get turned into ChainMaps, if they share a name with any of the default
            sections, they can inherit attributes from that default.

        Args:
            view: a valid view dict

        Returns: nothing, but adds an initialized view to the ChainMap

        """
        self.view = view
        for section in view.keys():
            chainmapped = ChainMap(self.view[section])
            try:
                chainmapped.maps.append(self.default_sections[section])
            except KeyError:
                pass
            self.view[section] = chainmapped
            if view[section].get('renderable', False):
                self._initialize_section(section)

    def composite(self, cellspace, position=(0, 0)):
        """ Given a cellspace and position, add that to the internal dict at the correct position.

        Args:
            cellspace: a cell space dictionary representation of a view object
            position: where the top left corner should go
        """
        for x,y in [(x,y) for y in range(cellspace.height) for x in range(cellspace.width)]:
            if cellspace.get((x,y), False):
                self.cells[(x+position[0],y+position[1])] = cellspace[(x,y)]

    def display(self, update=True, flush=True):
        """ Display fullscreen out to the terminal.

         Args:
             update: whether or not to update before displaying
             flush: whether or not to flush the internal state before rendering

         Notes:
            Uses Blessed for fullscreen terminal support.

        """
        if flush:
            self.cells = CellSpace()
        if update:
            self.update()

        with self.term.fullscreen():
            print(self.formulate(), end='')

    def formulate(self):
        """ Turns the internal dictionary into a string for rendering.

        Returns: A string that could render the whole screen if printed.
        """
        output_list = []
        for y in range(self.size[1]):
            if y > 0:
                output_list.append('\n')
            output_list.extend([self.cells.get((x, y), ' ') for x in range(self.size[0])])
        return ''.join(output_list)

    def update(self):
        """Updates the internal dictionary representation"""

        for section in self.view.keys():
            # only update renderable sections
            if self.view[section]['renderable']:
                # get the cells from the initialized instance
                new_cells = CellSpace(self.view[section]['instance'].as_cells())
                # extrapolate size information from new_cells
                bounds = Bounds(new_cells.width, new_cells.height)
                paddinged_size = self._apply_padding(bounds, self.view[section]['padding'])
                horz_padding = (bounds.width - paddinged_size[0]) //2
                vert_padding = (bounds.height - paddinged_size[1]) //2
                position = self._interpret_position(section, bounds)
                position = position[0]-horz_padding, position[1]-horz_padding

                # apply styles if they exist
                if self.view[section]['styles']:
                    for style_tuple in self.view[section]['styles']:
                        paddingless_bounds = bounds[0] + 2*horz_padding, bounds[1] + 2*horz_padding
                        self.composite(style_tuple[0](paddingless_bounds, **style_tuple[1]),
                                       position)

                content_position = position[0] + horz_padding, position[1] + vert_padding
                self.composite(new_cells, content_position)

    def _initialize_section(self, section):
        """ Go through a section figuring out bounds information and initializing the view_object
        Args
            section: a key for the section that should be initialized
            view: the index in the view of the view, 0 means top

        Notes:
            Does not return anything, but modifies the state of the view

        """
        bounding_information = self.view[section]['bounds']
        available_space = plie.Bounds(width=self.term.width, height=self.term.height)
        bounds = self._extract_bounds_information(bounding_information, available_space)
        bounds = self._apply_padding(bounds, self.view[section]['padding'])

        renderable = self.view[section]['view_object']
        kwargs = self.view[section]['contents']
        self.view[section]['instance'] = renderable(bounds=bounds, **kwargs)

    def _apply_padding(self, bounds, padding):
        """ Interpret the padding information, and the apply that to the bounds

        Args:
            bounds:
            padding: a padding representation

        Notes:
            There are four valid padding representations:
                * single number, means that padding on all sides,
                * two numbers means the first is top/bottom, and the second is right/left
                * three numbers means top, right, bottom
                * four numbers means top, right, bottom, left

        Returns: updated shrunken bounds

        """
        if isinstance(padding,Integral):
            new_width = bounds.width - (2*padding)
            new_height = bounds.height - (2*padding)
        elif len(padding) == 2:
            new_width = bounds.width - (2 * int(padding[1]))
            new_height = bounds.height - (2 * int(padding[0]))
        elif len(padding) == 3:
            new_width = bounds.width - int(padding[1])
            new_height = bounds.width - int(padding[0]) - int(padding[2])
        elif len(padding) == 4:
            new_width = bounds.width - int(padding[1]) - int(padding[3])
            new_height = bounds.width - int(padding[0]) - int(padding[2])
        else:
            raise TypeError('padding was not in a comprehensible format, got {}'.format(padding))
        return plie.Bounds(width=new_width, height=new_height)

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


    def _interpret_position(self, section, literal_bounds):
        """ From a section, find where the top left corner should go

        Notes:
            position can have three formatting options, percentage, choice, and integer
            percent is the standard percentage plus an optional cell modifier (50%+1)
            vertical_choice = 'top' | 'middle' | 'bottom'
            horizontal_choice = 'left' | 'middle' | 'right'
            integer means number of cells from the top or left side
            * Position refers to the center of the object mostly, specifics:
                * 50% means centered
                * 0% means top row or left column
                * 100% means last row, or right column

        Args:
            section: a key to lookup the section in the view dict
            literal_bounds: (x,y) size in cells for how big the object is

        Returns: an (x,y) tuple describing where the top left corner should go


        """
        # bounds = self._extract_bounds_information(self.view[section]['bounds'], self.size)
        # bounds = self._apply_padding(bounds, self.view[section]['padding'])

        x = self._position_1D(literal_bounds[0], self.size[0],
                              self.view[section]['positioning'].horizontal)

        y = self._position_1D(literal_bounds[1], self.size[1],
                              self.view[section]['positioning'].vertical)
        return (x,y)

    def _position_1D(self, size_of_the_object, span, specifier):
        """
        Notes:
            Currently will return values lower than 0 and bigger than span, if percentage with
            an operator pushes it that far. Negative percentages are not supported though.

        Args:
            size_of_the_object: 1D size in cells of the object
            span: refers to the size of the space the object is being put into
            specifier: the something used to specify the position

        Returns: an integer specifying how far from the left or top the thing should go

        """
        start_choice = {'top', 'left'}
        middle_choice = {'middle'}
        end_choice = {'bottom', 'right'}

        if isinstance(specifier, Integral):
            # case where specifier is just an integer
            return specifier
        elif specifier in start_choice | middle_choice | end_choice:
            # case where specifier is words
            if specifier in start_choice:
                return 0
            elif specifier in middle_choice:
                return round(span / 2 - size_of_the_object / 2)
            else:
                return span-size_of_the_object
        else:
            pattern = re.compile(
                r"(?P<percent>\d{1,4})%( *(?P<operator>[-+]) *(?P<amount>\d+)){0,1}")
            match = re.match(pattern, specifier)
            if match:
                percentage = float(match.group('percent')) * .01
                temp_start = int((span * percentage) - (size_of_the_object / 2))
                if match.group('operator') and match.group('amount'):  # 10%+5 cases
                    if match.group('operator') == '+':
                        return temp_start + int(match.group('amount'))
                    else:
                        return temp_start - int(match.group('amount'))
                else:  # 10% case
                    return temp_start
            else:
                raise ValueError('Specifier {} was not in a comprehensible format'.format(specifier))





