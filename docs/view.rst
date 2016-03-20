View
====

.. toctree::
   :maxdepth: 3


What counts as a 'valid view dict'?
-----------------------------------
This grammar specifies what Renderer accepts as a 'valid view dict' in Python's modified
`Backus-Naur form`_.

.. _Backus-Naur form: https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_Form

.. code-block:: ebnf

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
    horizontal_choice = 'left' | 'middle' | 'right'

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

In case that means little or nothing to you, or if you just want that in plain english:

    * a valid view dict is made up of sections
        * sections can be either renderable or not (specified by whether the ``'renderable'`` key in
          the section points to ``True`` or ``False``
        * Sections are dictionaries.
    * renderable sections contain any of the following keys ``'renderable'``, ``'positioning'``,
      ``'bounds'``, ``'view_object'``, ``'contents'``, ``'styles'``, ``'padding'``
        * ``'renderable'`` points to a boolean, which for a renderable section must be True
        * ``'positioning'`` describes where in the available space the output should be put.
            * :class:`plie.Position` provides a convenient way to store positioning information.
            * positioning has options, it be specified either as percentages or text choices:
                * for the vertical component:
                    * ``'top'``, ``'center'``, ``'bottom'`` are the three text choices
                    * percentages in this case mean that 0% is first row of the terminal and 100%
                      is the last row.
                * for the horizontal component:
                    * ``'left'``, ``'center'``, ``'right'`` are the three text choices
                    * percentages in this case mean that 0% is first column of the terminal and 100%
                      is the last column.
                * percentages can have an optional addition or subtraction of cells to specify a
                  precise offset. Example: ``'100%-1'`` would be the penultimate row or column.
        * ``'bounds'`` specifies how big an object is. :class:`plie.Bounds` provides a convenient
          way to store bounding information. Bounds are in the ``(width, height)`` format, where
          there are options for how width and height are represented:
            * percentage based: 100% means take up the whole screen, 0% is nothing. Percentages
              have an optional addition or subtraction of cells. Example: ``'100%-1'`` means in
              that direction the object should be as big as the screen minus one cell.
            * cell based: a cell is the basic unit of the screen, it's usually a character. Cell
              based sizes specify in cells how big the object should be. Example: ``50`` (that's
              just an integer) would mean the object in that direction should be 50 cells big.
        * ``'view_object'`` points to the class of the view object that's going to be rendered here,
          without actually initializing it.
        * ``'contents'`` points to the arguments that should be passed to the view_object
          constructor. This uses keyword arguments, and just passes them as ``**kwargs`` so any
          error in naming will cause an error.
        * ``'styles'`` points to a list of style tuples that should be applied to this view_object
            * style tuples contain the style callable and then any arguments that it should call
              with.
        * ``'padding'`` points to a specification for how much padding (in cells) should go around
          the view_object. This padding gets applied to the size of the view_object to squeeze
          it down to a smaller size than bounds. Useful for applying borders.
    * ``nonrenderable`` sections contain other stuff, but I'm not exactly sure what yet. They don't
      get executed or processed in any way currently (version 0.4.0)

