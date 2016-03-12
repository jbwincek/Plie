"""view mockups"""

"""Method 1: """

from collections import namedtuple

Bounds = namedtuple('Bounds', 'width height')
Position = namedtuple('Position', 'vertical horizontal')

this_view = {'header': {
                        'bounds': Bounds(width=term.width, height=1),
                        'view_object': plie.Text('title text')
                        },
             'body': {
                        'bounds': Bounds(width=term.width, height=term.height//2),
                        'view_object' : plie.Text('some text\n second line', justify='centered'),
                        'positioning' : Position(vertical='centered', horizontal='centered')
                        },
            'footer': {
                        'bounds': Bounds(width=term.width, height=1),
                        'view_object' : plie.Text('The footer')
                        }
            }

"""
Notes on method 1:
    * Can one even extract the positioning information from this?
        * header: doable because headers are attached to the top, and so then bounds plus top edge
          can give total coordinates for all four corners of the header.
        * body: if header is rendered first, and the bottom coordinates of the header are
          remembered, then the top of the available free area is known. The same applies to if
          footer is rendered first as well.
            * If body can have an optional 'positioning tuple, then this allows for choosing of
              where the view object (if it doesn't take up the full available area) should be
              positioned.
                * possible format could look like:
                    * vertical = 'top', 'centered' or 'bottom'
                    * horizontal = 'left', 'centered or 'bottom'
                * if a positioning key is not provided, then 'centered centered' will be used
                    * note: this refers to the positioning of the view object, not the layout of
                      the contents of the view object.
        * footer positioning is knowable for the same reason as header.

Issues and questions:
    * I don't really like the way size gets utilized. Like maybe there should default sizes,
      So the user doesn't have to specify it so much when it's not relevant.
        * And I wish there were a better way to handle relative sizes. Like something like 1 for
          full width, then fractions for partial width like 1/2 or 3/4, would be neat, but how to
          handle the case of a title that should be 1 cell tall. Unless 1 cell in that case is the
          full height. This only makes sense if things have a specific full width or full height,
          that 1 refers to, so if you want it to be that size you don't have to specify it,
          but if you want it a different size, than you could use fractional notation. Which sorta
          works for the 'body' section, but for 'header' and 'footer' height it seems weird,
          since it would not be a fraction unless you write it as '2/1' for two lines. Which I
          guess could be abbreviated to just '2', but still is that overly complicated? As it
          would force the user to learn some other layout scheme.
        * What about something as simple as %, if you give size a number it treats that as number of
          cells, but if you give it a string of regex format \d{1,3}% it will treat that as a
          percentage of full possible span (height or width).
    * If size is done this way (having size outside of the view object's namespace), then the
      view object will either have to look up it's own size in the view, OR renderer could pass the
      current / calculated size to the view object.
        * Using the plie.text signature from mock_ups.py:
            * This has size in the parameter list, but what does that size mean, and how should
            it be?
                - It makes sense for renderer to pass that size to it, so then what should the
                  default size be? (0,0) doesn't really make sense, unless as a way to specify
                  that it must be set to be drawn. Would that be better than None? Because it at
                  least shows the type/format of the kwarg? probably...
            * Is that a call once function, generator or class? Explore:
                * call once: Lots of initialization, but makes sense with updating the size,
                  would the callouts and callbacks still work? Well the callout would, since it
                  exists in the view, but the callback probably wouldn't. Though it would get
                  around the need for a callback, as another function could just update the entry
                  in the view, and then when the renderer re-renders it would see the updated
                  version. That implies some sort of global state though, well at least the view
                  as a global variable that could get changed from anywhere.
                * generator: initialized only once, would keep some internal state, callout works
                  fine, callback is more of a send() method to it, updating stuff about the state
                  could be done the same way. Though using send() for updating gets convoluted
                  quickly, maybe a mockup dealing with that would be wise...
                * class: initialized only once, would keep some internal state, call out works fine,
                  callback could be done somehow, maybe an update() method, which could function
                  similarly to the generator's send() method, but with a lot more straightforward
                  ease. Could contain a display() or output() or show() method, something along
                  those lines, to take the internal state and transform it into a dictionary for
                  outputting to the Renderer.
                    * drawbacks of class method: slightly heavier, that's about all I can think
                    of at this time, so it seems like the way to go.



"""

"""
Method 2: examining the use of percentages in bounds labeling
"""

from collections import namedtuple

Bounds = namedtuple('Bounds', 'width height')
Position = namedtuple('Position', 'vertical horizontal')

a_view = {'header': {
                        'bounds': Bounds(width='100%', height=1),
                        'view_object': plie.Text('title text')
                        },
             'body': {
                        'bounds': Bounds(width='100%', height='50%'),
                        'view_object' : plie.Text('some text\n second line', justify='centered'),
                        'positioning' : Position(vertical='centered', horizontal='centered')
                        },
            'footer': {
                        'bounds': Bounds(width='100%', height=2),
                        'view_object' : plie.Text('The footer, \n Footer's second line)
                        },
            'util' : {'handles_input': 'body'},
            'styles' : {'body':plie.border(border_style='rounded')}
            }




"""
Notes on method 2:
    * preliminary side notes:
        *'bounds' and 'positioning' only need tuple-likes, but namedtuples are strongly recommended
        * a_view could be any variable name
        *
    * utilizes percentages for width and height in spots:
        * all view fields have a default size, like for a header 100% wide of the terminal width's
          and 1 cell tall.
        * The percentages can be modified with +n or -n where n is the number of cells to trim
          off or add to the percentage. The regex \d{1,3}%([-+]\d+)* is used (see note below) for
          validating the strings. Then it looks if there's anything after the % sign, if there is,
          validate that it is a plus or minus, remember it, then validate that the next number
          can be converted to an integer. (all of that is already done by the regex, so it only
          needs to be parsed and converted to an int). Throw an error if any of that goes wrong.
        * means there will have to be a table of definitive defaults, though it seems like it
          will follow the rule of thumb that it takes up the full space where ever possible,
          except for headers and footers which default to a height of 1. pip3

        * (NOTE: this regex has been updated to \d{1,4}%( *[-+] *\d+)* to account for spaces
        before and after the + or - sign.
        * (NOTE: this regex has subsequently been updated again to be:
            (?P<percent>\d{1,4})%( *(?P<operator>[-+]) *(?P<amount>\d+)){0,1}
            * Notes about this regex, because it gets complicated:
                * the ?P<some_label> syntax means that if it get matched, the python match object
                will have an attribute with some_label for easily accessing that part.
                * this regex matches any size precentage up to 9999%, and an arbitrarily large
                subtraction or addition of cells to the end, including spaces before or after the
                operator, but it does not handle spaces between the percent number and % sign
"""

"""
Method 3: view as a class
"""

a_view = View()
a_view.header = {
    'bounds': Bounds(width='100%', height=1),
    'view_object': plie.Text('title text')
}
a_view.body = {
    'bounds': Bounds(width='100%', height='50%'),
    'view_object': plie.Text('some text\n second line', justify='centered'),
    'positioning': Position(vertical='centered', horizontal='centered'),
    'styles': [plie.border(border_style='rounded']
}
a_view.footer = {
    'bounds': Bounds(width='100%', height=2),
    'view_object': plie.Text('The footer, \n Footer's second line)
}
a_view.util = {'handles_input': 'body'},


"""
Notes on method 3:
    * Using a class gives a little more structure to the user automatically, so less to remember.
    * But using a class like this also makes it take up more space/lines
    * Could more be refactored into classes?
        * what about like a_view.body.view_object how would that work?
            * this needs experimenting, see view_as_class_mockups.py
        * if more was refactored into classes, could there still be a way to construct it such
        that if someone wanted to use the dict style set up to do it all in one go they could?
            * probably, just have there be an optional argument in the initialization that would
            convert the whole dict into the class property layout
    * Styles have been moved to within each section

"""

"""
Method 4: not really a method, but notes on handling multiple body elements

* (1) What we have currently:
    * header takes up a specific amount of space, subtracts that from space_left_over_for_body
    * footer takes up a specific amount of space, subtracts that from space_left_over_for_body
    * body then takes up the space_left_over_for_body amount of space
    * only one body element is possible with this method
* (2) where to go next:
    * header: use information from section.bounds to figure out how much space is needed,
    then subtract that from space_left_over_for_body
    * footer: use information from section.bounds to figure out how much space is needed,
    then subtract that from space_left_over_for_body
    * body: body then takes up the space_left_over_for_body amount of space
* (3) Then the next step is:
    * header: records height in from_top_offset
    * body:
        * iterate through each body element
        * use information from section.bounds to figure out how much space is needed,
        then subtract that from space_left_over_for_body, place this body element at
        from_top_offset, but respecting positioning (1), then it's height to from_top_offset

* Isssues with the last step:
    * This doesn't allow for horizontally arrayed text objects, like a paned window view
    * Should positioning just be absolute? Like specify an upper left corner and a bounds? Then
    just composite overlapping things (aka, the fuckit let the user handle it method)
        * This keeps the renderer and the parsing syntax simple, since with some flow formatting
        layout html div esque thing creating rules for how exactly things should go would be
        complicated and require a lot of decisions.
        * But for simple layouts, it would probably add boilerplate and complication, as well as
        going against the paradigms developed lately.
        * a potential work around would be for section to contain a top_left_corner style
        attribute that would let the user explicitly specify the location, this could be used to
        overload the default layout engine thing.
        * I don't even like the idea of a layout engine, maybe it's what is needed, but sheesh,
        seems like a can of worms.

* What do I want with regards to layout, views and rendering
    * simple for the user for basic layouts
    * flexibility to create precise or complex layouts if wanted


* Instead of step (3) coming after step (2), a revision could be made so that
space_left_over_for_body has both a height and width dimension. That seems like it'll open new
options in a good way.

"""