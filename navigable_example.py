import blessed
import plie
import time


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
            'view_object': plie.NavigableMenu,
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
                (plie.borderer, {'border_style': 'default'}),],
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
    renderer = plie.Renderer(view=a_view, terminal=term)
    renderer.display()
    for key in handle_keyboard(term):
        renderer.view['body_left']['instance'].handles_input(key)
        renderer.display()
    time.sleep(10)


run()
