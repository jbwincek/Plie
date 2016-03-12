from collections import namedtuple
Bounds = namedtuple('Bounds', 'width height')
Position = namedtuple('Position', 'vertical horizontal')


class Section:
    """ An organizational class, helps define the structure of View"""

    def __init__(self, bounds=(), positioning=None, view_object=None, styles=[]):
        """
        Args:
            bounds: A tuple-like, containing width and height of the section, can be formatted
                    either as an integer pair, or a pair of strings representing percentages
                    example: `(25, 40)` or `('100%', '50%')`

            positioning: A tuple-like, containing a pair of strings describing how the Section
                    should be positioned. `left`, `centered`, `right` are the three valid options
                    for horizontal positioning. `top`, `centered`, 'bottom' are the three valid
                    options for vertical positioning.
                    example: `('left', 'centered')` or as a namedtuple:
                             Position(vertical='bottom', horizontal='right')

            view_object: either a Text or MultiText view_object (this is what actually gets
                    rendered), the Renderer handles all the bounds specifying in the view_object call,
                    so only parameters like text, and justify are appropriate.

            styles: a list of styles to apply to the view_object

        Returns: an initialized Section object
        """
        self.bounds = bounds
        self.positioning = positioning
        self.view_object = view_object
        self.styles = styles

    def __bool__(self):
        if not self.bounds and not self.positioning and not self.view_object and not self.styles:
            # Case where all things are Falsey
            return False
        else:
            return True

    def __repr__(self):
        return 'Section(bounds=%r, positioning=%r, view_object=%r, styles=%r)' % (
            self.bounds, self.positioning, self.view_object, self.styles)


class View:
    """ Views are an organizational structure that contain all the view objects.

    Views can be constructed piece wise by setting individual properties, or they can
    be constructed by passing a well formed view dict to the constructor.

    Fields are filed with a section (header, footer) a list of sections (body), or a dictionary (
    util), if they are not filled out will be set to False-y values.

    Views contain four main sections:
        * header
            * headers are attached to the top of the terminal, and usually 1 cell tall
        * body
            * bodies are in the middle and take up the majority of the terminal, bodies
            can contain multiple view objects in a list. Each view object is treated
            as its own section with bounds, positioning, the view_object itself and styles.
        * footer
            * footers are like headers, but attached to the bottom of the terminal
        * util
            * a dictionary for storing extra information

    The three renderable sections (header, body, footer) have a styles attribute, which
    is a list of 'styles' (borders, colors, etc) to apply to that section.

    Views can repr themselves into a valid view dict.

    """

    def __init__(self, view_dict=None):
        self.header = Section()  # create an empty Section
        self.body = []  # empty list for holding Sections
        self.footer = Section()
        self.util = {}
        if view_dict:
            # check to see if there's an item, then assign it if it's there
            header = view_dict.get('header', False)
            if header:
                h_bounds = header.get('bounds', False)
                if h_bounds:
                    self.header.bounds = h_bounds

                h_view_object = header.get('view_object', False)
                if h_view_object:
                    self.header.view_object = h_view_object

                # header might not have positioning, but better safe than sorry
                h_positioning = header.get('positioning', False)
                if h_positioning:
                    self.header.positioning = h_positioning

                h_styles = header.get('styles', False)
                if h_styles:
                    self.header.styles.extend(h_styles)

            # generate a list of body Sections
            body_in_dict = view_dict.get('body', False)
            if body_in_dict:
                # handle the case where body_in_dict is just a single item
                if not isinstance(body_in_dict, (list, tuple, set)):
                    body_list = [body_in_dict]
                else:
                    body_list = body_in_dict
                for body_element in body_list:
                    b_bounds = body_element.get('bounds', ())
                    b_view_object = body_element.get('view_object', None)
                    b_positioning = body_element.get('positioning', None)
                    b_styles = body_element.get('styles', [])
                    s = Section(b_bounds, b_positioning, b_view_object, b_styles)
                    self.body.append(s)

            footer = view_dict.get('footer', False)
            if footer:
                f_bounds = footer.get('bounds', False)
                if f_bounds:
                    self.footer.bounds = f_bounds

                f_view_object = footer.get('view_object', False)
                if f_view_object:
                    self.footer.view_object = f_view_object

                f_positioning = footer.get('positioning', False)
                if f_positioning:
                    self.footer.positioning = f_positioning

                f_styles = footer.get('styles', False)
                if f_styles:
                    self.footer.styles.extend(f_styles)

            util = view_dict.get('util', False)
            if util:
                self.util = util

    def __iter__(self):
        """ Iterate through all the contained view_objects

        Returns: tuple: (view_object.as_cells, bounds)

        """
