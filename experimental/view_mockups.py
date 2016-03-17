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

"""
Method 5: describing valid view dicts in EBNF
"""

valid_view_dict = section_list , renderable_sections , utility_section
section_list = '[' (section_label ',')* ']'
section_label = "'"string_literal"'"
renderable_sections = (section_label ':' renderable_section_contents ',')*
renderable_section_contents  =  [affinity]
                                [bounds]
                                [positioning]
                                [view_object]
                                [contents]
                                [styles]
                                [rules]
                                [padding]
utility_secction = (util_key ':' util_val ',')*


"""
What that grammer is saying:
    * There's a first section in a view, that lists all the renderable section labels
    * renderable_sections are sections that can be rendered, each renderable section has any of
      following:
        * affinity : where the section should stick to (like top for header, or bottom for footer)
        * bounds : a bounding box for the section (either in percent or cells)
        * positioning : where in the available space should the object be placed
        * view_object : an uninitialized class of the type wanted for this section
        * contents : what should go in the view_object
        * styles : styles that should be applied to the output of the view_object
        * rules : I'm not exactually sure, but this is for the renderer, and earlier it seemed
                  useful, so come back to this. <-------
        * padding : how many cells of padding that are wanted, in html form, where:
            * single number, means that on all sides,
            * two numbers means the first is top/bottom, and the second is right/left
            * three numbers means top, right, bottom
            * four numbers means top, right, bottom, left
    * keep the utility_section, because it might be useful

What this means:
    * Sections will have defaults. There will be the default_view in Plié somewhere, if a section
      does not have a specific part of it specified, then the renderer will fall back to the
      default.
    * users can create their own defaults
    * the stock default will mimic the current functionality of Views
    * I can use ChainMap for overlaying views, and getting view inheritence/transparency
    * Less stuff needs to be specified by the user if they're just doing basic things
    * higher extensibility and greater flexibility due to the added optional specifications

What renderer needs to render something:
    * The space available to use up for the something
    * The size of the something
    * What the something produces when it does it's thing
    * How to modify that production in accordance to the style
        * A breif aside, what is a style:
            * a rule the gets applied before the something does it's producing
            * a pure function that takes in the produced something, and returns something with
              the style applied.
    * Where to position the thing the something produced

"""

"""
Method 6: a slightly refined grammer for views
"""

valid_view_dict = sections
sections = renderable_sections | non_renderable_sections
renderable_sections = (section_label ':' renderable_section_contents ',')*
renderable_section_contents  =  renderable_True, [affinity], [bounds], [view_object],
                                [contents], [styles], [padding]
rederable_True = "'renderable' : True, "
section_label = "'"?string_literal?"'"

affinity = "'affinity' :" affinity_contents
affinity_contents = affinity_tuple | affinity_namedtuple
affinity_tuple = '(' vertical_option ',' horizontal_option ')'
affinity_namedtuple = 'Affinity(vertical=' vertical_option ', horizontal=' horizontal_option ')'
vertical_option = 'top' | 'middle' | 'bottom'
horizontal_option = 'left' | 'middle' | 'bottom'

bounds = "'bounds' : " bounds_contents
bounds_contents = bounds_tuple | bounds_namedtuple
bounds_tuple = '(' bounds_measure ',' bounds_measure ')'
bounds_namedtuple = 'Bounds(width=' bounds_measure ', height=' bounds_measure ')'
bounds_measure = bounds_percent | integer
bounds_percent = integer '%' ['+' | '-' integer]
integer = nonzerodigit digit* | '0'+
nonzerodigit = '1'...'9'
digit = '0'...'9'

view_object = ?renderable_callable?

contents = '[' (key_value_argument_pairs)* ']'
key_value_argument_pairs = ?string_literal? ':' contents_value
contents_value = ?list? | ?tuple? | ?mapping? | integer | "'"?string_literal?"'"

styles = '[' (style_tuple',')* ']'
style_tuple = ?style_function? [',' key_value_argument_pairs]

padding = padding_all_around | padding_two_sides | padding_three_sides | padding_four_sides
padding_all_around = integer
padding_two_sides =  '(' integer ',' integer ')'
padding_three_sides = '(' integer ',' integer ',' integer ')'
padding_four_sides = '(' integer ',' integer ',' integer ',' integer ')'

non_renderable_sections = renderable_False , (extra_data_utils)*
renderable_False = "'renderable' : False"

"""
Notes on method 6:
    * This expands on what was started in method 6 with some changes
    * a valid view dict is made up of sections
        * sections can be either renderable or not (specified by whethere the 'renderable' key in
          the section points to True or False
        * (this means there's no longer a list of sections, instead sections are found by iterating
          through the keys, and checking if they're renderable)
    * Sections are dicts
    * renderable sections contain any of the following keys 'renderable', 'affinity' (see note),
      'bounds', 'view_object', 'contents', 'styles', 'padding'
        * 'renderable' points to a boolean, which for a renderable section must be True
        * 'affinity' used to be called positioning, affinity describes where in the available
           space the output should be put.
        * 'bounds' is like bounds from before, and specifies how big an object is, has the same
          percentage and cells versions of specifying
        * 'view_object' points to the class of the view object that's going to be rendered here,
          without actually initializing it.
        * 'contents' points to the arguments that should be passed to the view_object constructor
        * 'styles' points to a list of style tuples that should be applied to this view_object
            * style tuples contain the style callable and then any arguments that it should call
              with
        * 'padding' points to a specification for how much padding (in cells) should go around
          the view_object). This padding gets applied to the size of the view_object to squeeze
          it down to a smaller size than bounds. Useful for applying borders.
    * nonrenderable sections contain other stuff, but I'm not exactly sure what yet.


* Questions, concerns:
    * should affinity be called positioning?
    * should affinity accept percentage based positioning as opposed to the three options base
      positioning?
    * what about a positioning, that has both an absolute and a relative option, the relative option
      would be like the current affinity three choice thing (maybe with percentages), but the
      absolute option would let the user specify the top left corner of the view_object.
      
"""

"""
Method 7: affinity -> positioning: percentage based, specifier choice, or absolute, 
"""

valid_view_dict = sections
sections = renderable_sections | non_renderable_sections
renderable_sections = (section_label ':' renderable_section_contents ',')*
renderable_section_contents  =  renderable_True, [positioning], [bounds], 
                                [view_object], [contents], [styles], [padding]
rederable_True = "'renderable' : True, "
section_label = "'"?string_literal?"'"

positioning = "'positioning' :" positioning_contents
positioning_contents = positioning_tuple | positioning_nt
positioning_tuple = '(' vertical_option ',' horizontal_option ')'
positioning_nt = 'Positioning(vertical=' vertical_option ', horizontal=' horizontal_option ')'
vertical_option = percent | vertical_choice | positioning_int_pair
horizontal_option = percent | vertical_choice | positioning_int_pair
positioning_int_pair = '(' integer ',' integer ')'
vertical_choice = 'top' | 'middle' | 'bottom'
horizontal_choice = 'left' | 'middle' | 'bottom'

bounds = "'bounds' : " bounds_contents
bounds_contents = None | bounds_tuple | bounds_namedtuple
bounds_tuple = '(' bounds_measure ',' bounds_measure ')'
bounds_namedtuple = 'Bounds(width=' bounds_measure ', height=' bounds_measure ')'
bounds_measure = percent | integer
percent = integer '%' ['+' | '-' integer]
integer = nonzerodigit digit* | '0'+
nonzerodigit = '1'...'9'
digit = '0'...'9'

view_object = ?renderable_callable?

contents = '[' (key_value_argument_pairs)* ']'
key_value_argument_pairs = ?string_literal? ':' contents_value
contents_value = ?list? | ?tuple? | ?mapping? | integer | "'"?string_literal?"'"

styles = '[' (style_tuple',')* ']' | style_tuple
style_tuple = ?style_function? [',' key_value_argument_pairs]

padding = padding_all_around | padding_two_sides | padding_three_sides | padding_four_sides
padding_all_around = integer
padding_two_sides =  '(' integer ',' integer ')'
padding_three_sides = '(' integer ',' integer ',' integer ')'
padding_four_sides = '(' integer ',' integer ',' integer ',' integer ')'

non_renderable_sections = renderable_False , (extra_data_utils)*
renderable_False = "'renderable' : False"

"""
Notes about method 7:
    * Positioning changes:
        * Now that sections have padding, which can be specified on four
          sides, and more options. Positioning will now be global rather than
          relavant to the size of the space that the object is in. Global in
          this case means the position is relative to the size of the whole
    * Styles picked up a None option, to signify when no styles should be applied. A close contender was an empty tuple, that might come back.
    * 

"""
"""
Method 7: continued: this time as actual syntax
"""

a_view = {
    'header' : {
        'renderable' : True,
        'positioning' : plie.Positioning(vertical='0%', horizontal='50%')
        'bounds' : plie.Bounds(width='100%', height=1)
        'view_object' : plie.Text
        'contents' : {
            'text': 'header text goes here',
          'justify': 'left'
         },
        'styles' : None,
        'padding' : 0,
    },
    'body_left' : {
        'renderable' : True,
        'positioning' : plie.Positioning(vertical='50%', horizontal='25%')
        'bounds' : plie.Bounds(width='50%', height='100%-2')
        'view_object' : plie.MultiText 
        'contents' : {
            'text_list': ['menu option one',
                          'menu option two',
                          'menu option three'],
            'bullet_choice' : '*'    
            'justify': 'left'
            }
        'styles' : (plie.borderer, {'border_style' : 'rounded'})
        'padding' : 1

    }
    'body_right' : {
        'renderable' : True,
        'positioning' : plie.Positioning(vertical='50%', horizontal='75%')
        'bounds' : plie.Bounds(width='50%', height='100%-2')
        'view_object' : plie.Text 
        'contents' : {
            'text': some_long_text_variable,
            'justify': 'left'
            }
        'styles' : [
                    (plie.borderer, {'border_style' : 'rounded'}),
                    (plie.backgrounder, {'background' = '.'})
                    ]
        'padding' : 1

    }
    'footer' : {
        'renderable': True,
        'positioning': plie.Positioning(vertical='100%', horizontal='50%')
        'bounds': plie.Bounds(width='100%', height=1)
        'view_object': plie.Text
        'contents': {
            'text': 'The footer text',
            'justify': 'center'
        }
        'styles': None
        'padding': 0

    }
    'util' : {
        'renderable' : False,
        'contents' : []
  }
}

""" Notes about method 7: continued
    * Does positioning refer to where the top left corner goes, or where the 
      center of the object is?

"""

"""
Method 8: more refinements
"""

valid_view_dict = sections
sections = renderable_sections | non_renderable_sections
renderable_sections = (section_label ':' renderable_section_contents ',')*
renderable_section_contents  =  renderable_True, [positioning], [bounds],
                                [view_object], [contents], [styles], [padding], [VO_instance]
rederable_True = "'renderable' : True, "
section_label = "'"?string_literal?"'"

positioning = "'positioning' :" positioning_contents
positioning_contents = positioning_tuple | positioning_nt
positioning_tuple = '(' vertical_option ',' horizontal_option ')'
positioning_nt = 'Positioning(vertical=' vertical_option ', horizontal=' horizontal_option ')'
vertical_option = percent | vertical_choice | positioning_int_pair
horizontal_option = percent | vertical_choice | positioning_int_pair
positioning_int_pair = '(' integer ',' integer ')'
vertical_choice = 'top' | 'middle' | 'bottom'
horizontal_choice = 'left' | 'middle' | 'bottom'

bounds = "'bounds' : " bounds_contents
bounds_contents = None | bounds_tuple | bounds_namedtuple
bounds_tuple = '(' bounds_measure ',' bounds_measure ')'
bounds_namedtuple = 'Bounds(width=' bounds_measure ', height=' bounds_measure ')'
bounds_measure = percent | integer
percent = integer '%' ['+' | '-' integer]
integer = nonzerodigit digit* | '0'+
nonzerodigit = '1'...'9'
digit = '0'...'9'

view_object = ?renderable_callable?

contents = '[' (key_value_argument_pairs)* ']'
key_value_argument_pairs = ?string_literal? ':' contents_value
contents_value = ?list? | ?tuple? | ?mapping? | integer | "'"?string_literal?"'"

styles = '[' (style_tuple',')* ']' | style_tuple
style_tuple = ?style_function? [',' key_value_argument_pairs]

padding = padding_all_around | padding_two_sides | padding_three_sides | padding_four_sides
padding_all_around = integer
padding_two_sides =  '(' integer ',' integer ')'
padding_three_sides = '(' integer ',' integer ',' integer ')'
padding_four_sides = '(' integer ',' integer ',' integer ',' integer ')'

VO_instance = "'instance' :" ?instance of the view object?

non_renderable_sections = renderable_False , [blanking] (extra_data_utils)*
renderable_False = "'renderable' : False"\
banking = "'blanking' :" boolean
boolean = 'True' | 'False'


"""
Notes on method 8:
    * Sections can now contain instances of the view object class
    * the util section contains a blanking flag, to specify whether there should be a blank view
      placed undernear this view.
