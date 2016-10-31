from plie import MultiText

class Navigable():
    """Navigable ABC
        (note: not currently actually abstract 9/1/16)"""
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


class NavigableMenu(Navigable1D, MultiText):
    def __init__(self, *args, highlight='--', term=None, **kwargs):
        if term:
            self.term = term
            self.highlight = term.blue
            self.normal = term.normal
        else:
            self.highlight = highlight
            self.normal = ''  # r'\\x1b(B\\x1b[m'

        super(NavigableMenu, self).__init__(**kwargs)

    def __str__(self):
        lines = []
        for which, text_elem in enumerate(self.texts):  # process each text element
            if which == self.cursor_location:  # handles the selected menu element case
                for i, line in enumerate(str(text_elem).split('\n')):
                    if i == 0:  # the first line gets bulleted
                        lines.append(self.bullet_choice + self.highlight + line + self.normal)
                    else:  # remainders are just indented
                        blank_space = ' ' * self.term.length(self.bullet_choice)
                        lines.append(blank_space + self.highlight + line + self.normal)
            else:
                for i, line in enumerate(str(text_elem).split('\n')):
                    if i == 0:
                        lines.append(self.bullet_choice + line)
                    else:
                        blank_space = ' ' * len(self.bullet_choice)
                        lines.append(blank_space + line)
        return '\n'.join(lines)


class NavigableMultiText(MultiText):
    def __init__(self, texts=(), bullet_choice='', justify='left', bounds=None,
                 cursor_location=0, wrap_around=False):
        super(NavigableMultiText, self).__init__(texts=texts,bullet_choice=bullet_choice,
                                                 justify=justify, )

