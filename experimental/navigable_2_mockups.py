import sys
import os
sys.path.insert(0, os.path.abspath('../'))
import plie
import blessed
import time


class Navigable():
    """Navigable ABC"""
    def __init__(self, **kwargs):
        #raise AttributeError('Navigable init called')
        pass

    def handles_input(self, key):
        pass


class Navigable1D():
    def __init__(self, cursor_location=0, wrap_around=False, **kwargs):
        self.cursor_location = cursor_location
        if kwargs.get('texts', False):
            self.list_size = len(kwargs['texts'])
        else:
            self.list_size = 0
        self.wrap_around = wrap_around
        self.not_handled = ('KEY_LEFT', 'KEY_RIGHT', 'KEY_DELETE')
        super(Navigable1D, self).__init__(**kwargs)

    def handles_input(self, key):
        if key.name == 'KEY_UP':
            self.up()
        elif key.name == 'KEY_DOWN':
            self.down()
        elif key.name == "KEY_ENTER":
            self.select()
        elif key.name in self.not_handled:
            pass
        else:
            pass

    def up(self):
        if self.cursor_location > 0:
            self.cursor_location -= 1
        else:
            if self.wrap_around:
                self.cursor_location = self.list_size
            else:
                pass

    def down(self):
        if self.cursor_location < self.list_size -1:
            self.cursor_location += 1
        else:
            if self.wrap_around:
                self.cursor_location = 0
            else:
                pass

    def select(self):
        print("selected cursor location {}".format(self.cursor_location))


class NavigableMenu(Navigable1D, plie.MultiText):
    def __init__(self, *args, **kwargs):
        super(NavigableMenu, self).__init__(**kwargs)

    def __str__(self):
        lines = []
        for which, text_elem in enumerate(self.texts):  # process each text element
            if which == self.cursor_location:
                for i, line in enumerate(str(text_elem).split('\n')):
                    if i == 0:  # the first line gets bulleted
                        lines.append(self.bullet_choice + '--' + line)
                    else:  # remainders are just indented
                        blank_space = ' ' * len(self.bullet_choice)
                        lines.append(blank_space + '--' + line)
            else:
                for i, line in enumerate(str(text_elem).split('\n')):
                    if i == 0:
                        lines.append(self.bullet_choice + line)
                    else:
                        blank_space = ' ' * len(self.bullet_choice)
                        lines.append(blank_space + line)
        return '\n'.join(lines)


class NavigableMultiText(plie.MultiText):
    def __init__(self, texts=(), bullet_choice='', justify='left', bounds=None,
                 cursor_location=0, wrap_around=False):
        super(NavigableMultiText, self).__init__(texts=texts,bullet_choice=bullet_choice,
                                                 justify=justify, )


def handle_keyboard(term):
    try:
        with term.cbreak():
            while True:
                yield term.inkey()
    except KeyboardInterrupt:
        exit()


def run():
    item_three = """item three is significantly longer than the others, it shows that MultiText
    can handle multiple lines well, including making sure the indent is right when a list is
    bulleted. This could be lorem ipsum, but it's not."""

    some_long_text_variable = item_three * 3

    a_view = {
        'header': {
            'renderable': True,
            'positioning': plie.Position(vertical='0%', horizontal='50%'),
            'bounds': plie.Bounds(width='100%', height=1),
            'view_object': plie.Text,
            'contents': {
                'text': 'header text goes here',
                'justify': 'left'
            },
            'styles': None,
            'padding': 0,
        },
        'body_left': {
            'renderable': True,
            'positioning': plie.Position(vertical='50%', horizontal='25%'),
            'bounds': plie.Bounds(width='50%', height='100%-2'),
            'view_object': NavigableMenu,
            'contents': {
                'texts': ['menu option one',
                          'menu option two',
                          'menu option three'],
                'bullet_choice': '* ',
                'justify': 'left'},
            'styles': [(plie.borderer, {'border_style': 'rounded'}),],
            'padding': 1,
        },
        'body_right': {
            'renderable': True,
            'positioning': plie.Position(vertical='50%', horizontal='75%'),
            'bounds': plie.Bounds(width='50%', height='100%-2'),
            'view_object': plie.Text,
            'contents': {
                'text': some_long_text_variable,
                'justify': 'left'
            },
            'styles': [
                (plie.borderer, {'border_style': 'default'}),
               (plie.backgrounder, {'background': ' '})
                ],
            'padding': 1,
        },
        'footer': {
            'renderable': True,
            'positioning': plie.Position(vertical='100%', horizontal='50%'),
            'bounds': plie.Bounds(width='100%', height=1),
            'view_object': plie.Text,
            'contents': {
                'text': 'The footer text',
                'justify': 'center'
            },
            'styles': None,
            'padding': 0,

        },
        'util': {
            'renderable': False,
            'contents': [],
        }
    }

    term = blessed.Terminal()
    #nav = Navigable1D(wrap_around=True)
    renderer = plie.Renderer(view=a_view)
    renderer.display()
    for key in handle_keyboard(term):
        renderer.view['body_left']['instance'].handles_input(key)
        renderer.display()
    time.sleep(10)


run()
