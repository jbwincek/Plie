import sys
import os
sys.path.insert(0, os.path.abspath('../'))
import plie
import blessed


class Navigable1D:
    def __init__(self, cursor_location=0, list_size=5, wrap_around = False):
        self.cursor_location = cursor_location
        self.list_size = list_size
        self.wrap_around = wrap_around
        self.not_handled = ('KEY_LEFT', 'KEY_RIGHT', 'KEY_DELETE')

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
            print(key, end='', flush=True)

    def up(self):
        if self.cursor_location > 0:
            self.cursor_location -= 1
        else:
            if self.wrap_around:
                self.cursor_location = self.list_size
            else:
                pass

    def down(self):
        if self.cursor_location < self.list_size:
            self.cursor_location += 1
        else:
            if self.wrap_around:
                self.cursor_location = 0
            else:
                pass

    def select(self):
        print("selected cursor location {}".format(self.cursor_location))


class NavigableMenu(plie.MultiText, Navigable1D):
    def __init__(self, *args, **kwargs):
        pass



def handle_keyboard(term):
    try:
        with term.cbreak():
            while True:
                yield term.inkey()
    except KeyboardInterrupt:
        exit()

term = blessed.Terminal()
nav = Navigable1D(wrap_around=True)
for key in handle_keyboard(term):
    nav.handles_input(key)