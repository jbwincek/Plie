
"""
An experiment of how view as a class could work.
"""


class Section():
    def __init__(self):
        self.bounds = None
        self.positioning = None
        self.view_object = None
        self.styles = []


class View():
    """ Views are an organizational structure that contain all the view objects.

    Views can be constructed piece wise by setting individual properties, or they can
    be constructed by passing a well formed view dict to the constructor.

    Fields that are not filled out will be set to None.

    Views contain four main sections:
        * header
            * headers are attached to the top of the terminal, and usually 1 cell tall
        * body
            * bodies are in the middle and take up the majority of the terminal, use a
             Multitext if more than one Text view object is needed.
        * footer
            * footers are like headers, but attached to the bottom of the terminal
        * util
            * a dictionary for storing extra information

    The three renderable sections (header, body, footer) have a styles attribute, which
    is a list of 'styles' (borders, colors, etc) to apply to that section.

    Views can repr themselves into a valid view dict.

    """
    def __init__(self, view_dict=None):
        self.header = Section()
        self.body = Section()
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

            # do the same thing for the body section
            body = view_dict.get('body', False)
            if body:
                b_bounds = body.get('bounds', False)
                if b_bounds:
                    self.body.bounds = b_bounds

                b_view_object = body.get('view_object', False)
                if b_view_object:
                    self.body.view_object = b_view_object

                b_positioning = body.get('positioning', False)
                if b_positioning:
                    self.body.positioning = b_positioning

                b_styles = body.get('styles', False)
                if b_styles:
                    self.body.styles.extend(b_styles)
            
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



