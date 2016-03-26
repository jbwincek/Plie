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

"""
Experiment 2:
"""


def main_loop():
    renderer = plie.Renderer(a_view_dict)
    renderer.display()
    for key in handle_keyboard(renderer.term):
        renderer.view.util['handles_input'].send(key)



"""
Notes on experiment 2:
    * I like how it is action based. this decouples the event loop from the actual renderer
    * I don't like how verbose it is
        * What about an attribute that does a cachable search for a handles input attribute?
            * Would leave the current 'handles_input' key there
            * but would also make an option like renderer.input_handler which would just be a
              property for the 'handles_input' key
                * input_handler might not be the best name though
    * I don't like how 'handles_input' needs to be synchronized with what's handling input
        * Because it relies on the user, it means Plié doesn't have to handle logic of where to
          send the keyboard input. So this aspect is both a minus and a plus.
    * This feels more low level
        * Like although I see the benefits of having some direct keypress/action based system
          this:
            A.) requires the user to roll their own event loop
            B.) requires the user to worry about keyboard stuff when they might rather be thinking
                about their own app, layout, and design. (This is the bigger issue)
                * Does it though:
                    * No, because once the loop is established, if Plié has good features to
                      automatically handle normal keyboard input for things like menus and the
                      like, then most of it happens seamlessly.
                    * Yes, because every revolves around the keyboard loop, tightly couples with
                      the keyboard (What about an API for menus, like up(), down(), left(),
                      right(), select(), back()?)
                    * Yes, but the action loop has been fundamental to the design of Plié since
                      almost the beginning.
    * What about a menu API?
        * Core questions:
            * What does API mean in this specific context?
                * Some way of interacting with interactive things, more specifically:
                    * An abstraction layer between input (either keyboard or other) and how built
                      in Plié objects expect information to be passed to them
            * Could I craft an API that captures the majority of the use cases?
            * What will Plié lose in using an API here?
                * A simplicity, it forces the user to learn the api, and forces me to program,
                  document and maintain an API
            * What will Plié gain in using an API here?
                * less coupling with keyboard as the only input mechanism
                * some explicitness about the actions
            * counter thoughts:
                * if the user has their own event handler, based off of some system other than the
                  keyboard, and if the keyboard input for navigation is well specified, the user
                  could then just send blessed keyboard commands to whatever is expecting the
                  commands. Like why rely on making some new api, when Blessed has a format for up
                  down and etc keyboard keys already. Using that as the 'API' doesn't seem too
                  obtuse.
            * Is creating an API here a good idea?
                * It doesn't seem like it.


"""


