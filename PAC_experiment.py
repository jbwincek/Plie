import blessed
from collections import namedtuple


term = blessed.Terminal()

"""
Sketch of how a simple Presentation-Abstraction-Control architecture could look.
"""


class Offset():
    """ Simple class for ease of referring to offsets

    Args:
        x (int): how many characters from the left to start printing at (indent)
        y (int): how many lines down from the top to start printing at
    """
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __iter__(self):
        """ Enables splatting (ex: *var) """
        yield self.x
        yield self.y


class TextControlSketch:
    """ Control in a PAC architecture for displaying interactive text

        This example has a few functions entered with the keyboard:
            u sends an update command
            q quits
            b toggles bold of the displayed text
            arrow keys adjust where the text should be placed from the top left

        Args:
            text (str): what text should be passed to the abstraction
    """
    def __init__(self, text):
        """ Establishes connections to the Presentation and Abstraction components """
        self.presentation = TextPresentationSketch()
        self.abstraction = TextAbstractionSketch(text)

    def update(self):
        """ Pull data from Abstraction, then present it

        Notes:
            AMUC stands for Universal Interoperable Storage Format of Text
            UIDFT stands for Universal Interoperable Drawing Format of Text
            UDD stands for Universal Dumb Drawer
        """
        UISFT = self.abstraction.AMUC()
        UIDFT = self.presentation.AMUC(UISFT)
        UDD(UIDFT, UISFT.offset)

    def send(self, event):
        """ Receives input from external sources

        Args:
            event: a keypress in this implementation

        Notes:
            * could be called receive,but name and function is analogous to the
              generator usage of send.
            * In a more flexible implementation <event> could be more than just a key
              press and this method could serve as a dispatch for sending the event to
              different places depending on what type of event it is.

        """
        self.process_keypress(event)

    def process_keypress(self, key):
        """ process/act on/interpret a keypress

        Args:
            key: a keypress

        """
        if key == 'q':
            print('bye')
            quit()
        elif key == 'u':
            self.update()
        elif key == 'b':
            # toggle bold
            self.abstraction.bold = not self.abstraction.bold
        elif key.name in ('KEY_UP', 'KEY_DOWN', 'KEY_LEFT', 'KEY_RIGHT'):
            if key.name == 'KEY_UP':
                self.abstraction.offset.y -= 1
            elif key.name == 'KEY_DOWN':
                self.abstraction.offset.y += 1
            elif key.name == 'KEY_RIGHT':
                self.abstraction.offset.x += 1
            else:
                self.abstraction.offset.x -= 1
        else:
            self.abstraction.text = key.name or key # space has a Falsey name
        self.update()



class TextPresentationSketch:
    """ Presentation in PAC architecture, handles converting the abtraction format to UIDFT

    Notes:
        This doesn't actually draw/present anything
        Tries to not keep any internal state, only a class because the other two components
        are classes.
        AMUC stands for Abstraction/model UIDFT Converter
        UIDFT stands for Universal Interoperable Drawing Format of Text and is the format
            the UDD expects.

    """
    def __init__(self):
        pass

    def AMUC(self, UISFT):
        """ Convert abstraction format (AMUC) to presentation format (UIDFT)

        Args:
            UISFT: Universal Interoperable Storage Format, the format TextAbstractionSketch
                   outputs

        Returns: A UIDFT which is basically a printable string

        """
        text = UISFT.text
        bold = UISFT.bold
        if bold:
            prefix = term.bold
        else:
            prefix = ''
        suffix = term.normal
        UIDFT = prefix + text + suffix
        return UIDFT


class TextAbstractionSketch:
    """
    Abstraction component in PAC architecture, holds the data

    Args:
        text (str): the text that should be held
        bold (bool): a style determining whether or not to embolden the text
        offset (Offset): How far from the top left corner to place the text
    """



    def __init__(self, text, bold=False, offset=Offset(0,0)):
        self.text = text
        self.bold = bold
        self.offset = offset

    def AMUC(self):
        # Universal Interoperable Storage Format of Text
        UISFT = namedtuple('UISFT', ['text', 'bold', 'offset'])
        return UISFT(self.text, self.bold, self.offset)


def UDD(UIDFT, offset=Offset(0,0)):
    # take in input in UIDFT form and print it out
    with term.location(*offset):
        print(UIDFT)


def input_handler(control):
    with term.fullscreen():
        with term.cbreak():
            while True:
                event = term.inkey()
                control.send(event)


input_handler(TextControlSketch("test text"))
