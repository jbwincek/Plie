"""
This file contains mock-ups for how Plié could work for handling more complex screen layouts.
"""
from plie import plie

"""
Method 1: first draft
"""

from functools import  partial

contents = {
    'header' : partial(plie.simple_title, text='title bar'),
    'styles' : partial(plie.border),
    'body' : [partial(plie.multiselect, choices=[
                    partial(plie.selectable_text, text ='option1', function_to_call_upon_select),
                    partial(plie.selectable_text, text ='option2', option2_func),]),
              partial(plie.fit_text, text = SOME_lONG_TEXt), ],
    'footer' : partial(plie.status_bar, text ='status bar', text_update_call_back)
}


with FullscreenWindow as win:
    win.render(contents)

"""
What all that might mean:
    * Plié could handle rendering windows roughly like html layouts.
    * Four fields could be available:
        * header: renders on top of other things, attached to the top
        * styles: for all style related choices, like borders and text colors that apply to
          everything.
        * body: anything that should be rendered in the middle, would be at a lower virtual
          z-depth than the header or the footer
        * footer: attached the bottom
    * Any category of field could take one or more options as a list
        * Sometimes this makes sense, like a body with a menu and some help text, other times
          not, like two overlapping headers, but two offset headers would make sense as well,
          so worth keeping the flexibility in.
        * Early items in the list get rendered on top of later items when there's overlap

What I like about this method:
    * It lays out everything neatly, puts it all in one place, and seems fairly semantically
      terse and intuitive.
    * It allows for complex nested layouts

What I don't like about this method:
    * All of the partials, it would be better to not have everything as a functools.partial

Possible improvements:
    * Does title_bar and status_bar need to be different objects?
        * could one object––like universal_text––display text, and be able to register a call
        back so that if someone wanted to update the text they could, and if they didn't it would
        remain static.
    * instead of functions, these could all be generators, which goes back to earlier drafts of Plié
      and would probably get around
"""



"""
Method two: more generator esque, less partials
"""
layout_dict = {
    'header' : plie.text(text='title bar'),
    'styles' : plie.border(border_style='heavy'),
    'body' : [plie.multiselect( choices=[
                                        plie.text(text ='option1', callout=function_to_call_upon_select),
                                        plie.text(text ='option2', callout=option2_func, )]),
            plie.text(text = SOME_lONG_TEXt, justify='centered'),
            ],
    'footer' : plie.text(text ='status bar')
}


with FullscreenWindow as win:
    contents = intialize(layout_dict)
    render(contents)

"""
Notes about this method:
    * text became universal:
        * if you want to change it you can send() into it by addressing it in the dict
            * like layout_dict['footer'].update('some new text for the footer')
        * if upon selection it should call a function add a callout kwarg, and it'll call that
        * text that's one line works just fine, text that's many lines works just fine too
    * each item is a generator or a function that displays text upon being called
    * I don't know how keyboard input would be handled
    * nested screens would be handled by:
        * when a selectable item is selected, the callout is called
        * upon entering the new function, another layout_dict could be loaded and rendered
        * when that function terminates, state would return to the old layout dict
        * (would this require a dict stack?)

What I like about this method:
    * Less boilerplate than method 1
    * less versions of text to remember
"""



"""
Method 3: view stack for rendering and input handling
"""

layout_view = {
    'header' : plie.text(text='title bar'),
    'styles' : plie.border(border_style='heavy'),
    'body' : [plie.multitext( choices=[
                                        plie.text(text ='option1', callout=nested_view),
                                        plie.text(text ='option2', callout=option2_func, )],
                            stacking='vertical'),
            plie.text(text = SOME_lONG_TEXt, justify='centered'),
            ],
    'footer' : plie.text(text ='status bar'),
    'util' : {'handles_input' : body.0},

}


def nested_view(renderer):
    changes_view = {
        'body' : plie.text(text = TEXT_TO_DISPLAY_ON_THE_NESTED_VIEW),
        'util' : {'blank' : True}
    }
    renderer.add(changes_view) # add a new view dict to the stack
    r.display()
    time.sleep(1)
    return


with FullscreenWindow as win:
    r = Renderer(win, layout_view)
    with Input as input:
    r.display(i)


"""
Notes on method 3:
    * This code snippet would show a menu, if option one is chosen then nested_view gets called,
      which then shows only TEXT_TO_DISPLAY_ON_THE_NESTED_VIEW, for 1 second, then display
      switches back to the main view
    * added a Renderer, which takes the window and an initial layout view:
        * Renderer handles all the initializing of things in the view
        * Renderer works like a stack, views can be added to it and popped from it
        * The topmost view gets rendered
        * If there's anything missing from the top view, the Renderer will look at lower items on
          the stack for things in each category to render, unless in 'util': 'blank' is set to True,
          then all other fields will remain blank (good for popups)
        * if a callout function gets called, when it returns the screen should re-render
        * if blank = True, or there's no definition anywhere in the stack for a section/field
          then it will still render just all that will be blank.
    * added the 'util' category to the view:
        * 'handles_input' specifies which object in the view should have input passed to it
            * if something has no use for input, it just ignores it rather than raising an error
            * handles_input can point to an object in the view or another function that isn't
              part of the view to process input more complexly than view objects can handle.
    * added multitext:
        * has options for select one, and select multiple
        * holds items as a list
        * calls the callout function for the selected item
        * option to display vertically or horizontally


Glossary:
    * view: a dictionary containing items to render to the screen (as shown above
    * Renderer: a class to handle rendering
    * view object: something that gets displayed in the view, text,
    * text: universal text displaying object, than can handle changes from other places,
            single lines, multiple lines, and callout functions
    * multitext: a sequence of text objects for creating menus
    * field/section: 'header', 'body', 'footer', 'styles', 'util' in the view dict

Possible issues and questions:
    * how to refer to items in the view, specifically for handles_input
    * what about multiple sources of input?
    * is input tied to views really the best idea?
        * if input can be handled by a non-shown processor function, which can dispatch to a view
          object, add new views to render stack, or update existing views
    * is the universal text too complex? Specifically with regards to using it as a menu selectable
        * the callout functionality is more like a tag or attribute, the multitext would handle
          actually selecting, and calling it, so that does pull away some of the complexity from
          text itself
    * what about text fields?
        * Should plie.text handle that, or should editable text fields be another object?
    * is plie.multitext the best name?
        * selector, selectron, selectromatic, multiselect, menu, choice,
    * there's no buttons yet
        * buttons could be handled by plie.multitext

What I like about this method:
    * The possibility for some async input handler to update dispatch input, which updates the
    renderer, and then renders upon each input, which is very close to my original vision.
    * view stacks with compositing seems cool
    * things seem very built out of small pieces which seems good
    * inheriting from views below seems useful for cutting down typing, but blanking seems nice for
      keeping things simple if wanted.

What I don't like about this method:
    * The view dictionary has potential for getting very complicatedly nested
    * plie.text has a possibility of getting very complex
"""



"""
Method 4: examining string compositing, the dict that gets rendered

"""

def plie.text(text='', callout=None, justify='left', position='centered', size = (20,40)):
    _text = text
    _position = 'centered'
# ...

"""
Notes on Method 4:
    * Each view object can't handle terminal resizing during creation of a frame (should be short)
        * Like other forms of input, a resize could call a Renderer.display()
    * view objects are generators and yield a dict that represents the text on the screen in an (
      x,y) matrix
    * text handles three position types: centered, left, right
        * centered:
            * top left corner: term.width/2 - x_size/2, term.height/2 - y_size/2
            * bottom right corner: term.width/2 + x_size/2, term.height/2 + y_size/2
        * left:
            * top left corner: 0, term.height/2 - y_size/2
            * bottom right corner: x_size, term.height/2 + y_size/2
        * right:
            * top left corner: term.width - x_size, term.height/2 - y_size
            * bottom left corner: term.width, term.height/2 + y_size
        * doing it this way puts positioning into plie.text as something to handle, rather than
        leaving that for plie.Renderer
            * I don't know if I like that.
            * like what about the case where position is set to 'left' and there's a border
            around the whole window.
            * one way to get around some of the complication, would be to use a bounds nameTuple
              of format like bounds['l'], which would return the left most possible cell. So that
              for 'left' justified mode, instead of using 0, it would use bounds['l'].
              Plie.Renderer could handle supplying each view object with a bounds, and let the
              view objects decide what it wants to do with the space in the bounds. Then upon
              yielding, it could yield a dict the size of bounds, that plie.Render could
              composite into the right position.
"""



"""
Method 5:
"""
from collections import namedtuple

# creates namedtuple with four fields, top, right, left, bottom
Bounds = namedtuple('Bounds', ['top right bottom left'])

b = Bounds(top=5, right=term.width-1, bottom=term.height-2, left=term.width-1) # example of setting

def plie.text(text='lorem ipsum',
              callout=None,
              justify='left',
              horizontal_position='centered',
              vertical_position='centered',
              bounds = None):
    _text = text
    _position = 'centered'
# ...


"""
Notes on method 5:
    * Plie.Renderer passes a Bounds namedtuple to each view object
        * this tuple can have static attributes (like top=5) or can have window size dependent
         attributes (like right=term.width-1). This was when the screen changes size the view
         object can intelligently adjust its size.
    * view objects yield dicts of size Bounds, leaving compositing and final positioning up to
      plie.Renderer
    * each view object is in it's own little world essentially, limited to the size of Bounds,
      but with free reign over what happens within Bounds.
    * Positioning in this method:
        * centered:
            * call to blessed.Terminal.center(a_line, width=Bounds[right])

Issues and questions:
    * Does bounds need to be top,right,bottom,left or could it just get away with width,height
        * I think width,height might be fine?
            * if plie.Renderer handles all the positioning, and so while rendering might render
              0,0 of some view object at actually 3,3 of terminal space, then each view object
              only needs a width,height
            *

"""

"""
Method 6: Renderer calling format updates
"""

layout_view = {
    'header' : plie.text(text='title bar'),
    'styles' : plie.border(border_style='heavy'),
    'body' : [plie.multitext( choices=[
                                        plie.text(text ='option1', callout=nested_view),
                                        plie.text(text ='option2', callout=option2_func, )],
                            stacking='vertical'),
            plie.text(text = SOME_lONG_TEXt, justify='centered'),
            ],
    'footer' : plie.text(text ='status bar'),
    'util' : {'handles_input' : body.0},

}


def nested_view(renderer):
    changes_view = {
        'body' : plie.text(text = TEXT_TO_DISPLAY_ON_THE_NESTED_VIEW),
        'util' : {'blank' : True}
    }
    renderer.add(changes_view) # add a new view dict to the stack
    r.display()
    time.sleep(1)
    return

from blessed import Terminal
from collections import namedtuple

TerminalSize = namedtuple('TerminalSize', ['width height'])

def run()
    term = Terminal()
    with term.fullscreen():
        size = TerminalSize(width=term.width, height=term.height)
        r = Renderer(size=size, view=layout_view)
        with Input as input:
            r.display(input)


"""
Notes on method 6:
    * plie.Renderer.display is a wrapper around something like plie.Renderer.forumulate,
    formulate returns a string that could be printed to cover the entire terminal, display just
    clears the display, and then prints that string.
        * This makes it easy to test plie.Renderer since one can just string match, as opposed to
          trying to read the terminal or some other hack like that.
"""

"""
Mock Up 7: Renderer as a context manager
"""

from plie import Renderer

def handle_keyboard(terminal):
    # a generator that yields key-presses
    with terminal.cbreak():
        yield terminal.inkey()

# Renderer as a context manager
with Renderer(a_view_dict) as r:
    for key in handle_keyboard(r.term):
        # do something

"""
Notes on Mock-up 7:
    * I imagine it is an optional context manager
        * The user could still use it the old way
"""