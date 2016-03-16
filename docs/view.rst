View
====

.. py:currentmodule:: plie

.. autoclass:: View
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: Section
    :members:
    :undoc-members:
    :show-inheritance:

.. toctree::
   :maxdepth: 3


What counts as a 'valid view dict'?
-----------------------------------
This grammar specifies what Renderer accepts as a 'valid view dict' in Python's modified
`Backus-Naur form`_.

.. _Backus-Naur form: https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_Form

.. code-block:: ebnf

    valid_view_dict    ::= '{' view_dict_contents '}'

    view_dict_contents ::= (renderable),* [util_section]

    renderable         ::= ('body' | 'header' | 'footer') : Section

    util_section       ::= 'util' : { (util_key : value,)* }

    Section            ::= [bounds,][view_object,][positioning,][styles]

    bounds             ::= 'bounds' : plie.Bounds

    view_object        ::= 'view_object' : plie.Multitext | plie.Text

    positioning        ::= 'positioning' : plie.Position

    styles             ::= 'styles' : [(style,)*]

    style              ::= ('border' : plie.borderer) | ('background' : plie.backgrounder)


    section_pair ::= section_key : '{' section_contents '}'


    section_key ::= "'"("'header'" | "'body'" | "'footer'" | "'util'")"'"
