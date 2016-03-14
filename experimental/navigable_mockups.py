""" Method 1: Multiple inheritance based navigable text menus
"""


import plie
import time

def func_1():
    a_view.header.view_object.update('choice one selected')
    renderer.display()

def func_2():
    a_view.header.view_object.update('choice two selected')
    renderer.display()

def func_3():
    a_view.header.view_object.update('choice three selected')
    renderer.display()


choices = [('option one', func_1),
           ('option two', func_2),
           ('option three', func_3)]

a_view_dict = {
    'header' : {
        'bounds': plie.Bounds(width='100%', height=1),
        'view_object': plie.Text('title text')
        },
    'body' : {
        'bounds': plie.Bounds(width='100%', height='50%'),
        'view_object': plie.NavigableMultiText(choices, justify='centered'),
        'styles': []
        },
    'footer' : {
        'bounds': plie.Bounds(width='100%', height=2),
        'view_object': plie.Text("The footer...")
        },
    'util' : {'handles_input': 'body'}
}

a_view = plie.View(a_view_dict)

renderer = plie.Renderer(view=a_view)
renderer.display()

term = blessed.Terminal()
with term.cbreak:
    kb = True
    while kb != 'q':
        kb = term.inkey()
        a_view.util['handles_input'].send(kb)

"""
Notes on method 1:
    * plie.Navigable is a new thing
        * accepts a list of tuples of format ('text to display', func_to_call_when_chosen())
        * Navigable keeps track of some internal state, like where the pointer (selector) is
        * Navigable also accepts stuff from .send() which it then bases actions on
        * default possible options, are down arrow to move down, up arrow to move up, and enter
          to select an item.
    * keyboard_input context manager, in a blessed style
    * a_view.util['handles_input'].send(kb) implies a generator based coroutine

Possible implications
    * plie.navigable:
        * self referencing objects is weird. Like in a way I'd love for super(object) or
          something similar like object.parent() to work instead of having to do something like
          this: a_view.header.view_object.update() because how in a different function would you
          always know which view it is to update, and then that implies keeping track of some
          global view state.
            * renderer.view_on_top.header.view_object.update() might work, but that is almost a
              line long, and makes renderer into a choreographer of Views. Which I suppose it is
              already so that wouldn't be too much of a problem, but it still has the ongoing
              global variable issue, which is maybe unavoidable #nothaskell
            * using Renderer as the choreographer makes sense as it is already doing that with
              maintaining a view stack, and then the names of the specific View instances don't
              matter as much as their position in the stack, which is more relevant to the program
              anyways.
    * coroutine based:
        * Will this mess up how Renderer handles things?
            * Renderer currently calls .update() on the view_object, then uses it's .as_cells()
              method.
            * So if the coroutine for handling input, updates the internal state after doing it's
              action, then everything should be okay. Since although we are using a generator, we're
              not iterating over it's output, only using it for its coroutine functionality.
    * keyboard input context manager:
        *
* Inheritance, classes, and how I would want it set up:
    * MultiText as a base class for formatting lists of text, could be used for all sorts
      of things
    * Navigable (or something similarly named) as a base for handling keyboard
    navigation, it would keep an state about where the pointer/cursor/selector is,
    and then use keyboard commands to navigate based off of that.
    * Then something like menu, or NavigableMultiText, or some attractive name:
        * Which would use the list based text formatting from MultiText and the
        navigation handling from Navigable.

"""


