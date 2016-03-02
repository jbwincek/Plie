

class Text():
    def __init__(self,
                 text='',
                 callout=None,
                 justify='left',
                 horizontal_position='centered',
                 vertical_position='centered',
                 bounds=None):
        pass

    def update(self, bounds=None, text=None, **kwargs):
        """ For changing internal state, including updating the text to display.

        update() accepts **kwargs, so any keyword argument passed during initialization can be
        passed again, to change the stored value.

        Returns: True if updating went well
        """

    def display(self):
        """ That's the internal state and translates it into a screen-space cell dict of size bounds

        Returns: Dictionary with keys of format (x,y), of size bounds and single character
        strings as the values.

        """


