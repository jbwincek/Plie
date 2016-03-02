Renderer
========

.. py:currentmodule:: plie

.. py:class:: Renderer(view=None, size=None, term=None, fullscreen=True)

    Composite, renders and manages layout of views and view objects.

    Renderer handles initiating all the view objects.

    Maintains a stack of views. Views are 'translucent' in that blank space in a
    view will cause the view(s) below it to render as well (unless the view has a
    flag telling the renderer to only render that view.

    .. py:method:: __init__()

        :param view view: The initial starting view to display
        :param size: The size to render, if None then it will use the terminal size.
        :type size: None or Tuple or namedtuple
        :param term: An initiated Blessed terminal class to use, if none :py:class:Renderer will
        create it's own, and use that.
        :param boolean fullscreen: whether or not to take over the terminal and return it as it
        was before


    .. py:method:: formulate()

        Formulate converts the internal screen-space representation into a string for printing.

        :return: A string for displaying

    .. py:method:: display()

        Displays the current state of the view. If Renderer size is set to use the Terminal size,
         then it will check ``term.width`` and ``term.height`` before displaying, so it will
         always display to the correct size, even after resizing.

    .. py:method:: push_view(view)

        Adds a view object to the internal stack

    .. py:method:: pop_view(view

        Pops the topmost view off of the internal stack


.. toctree::
    :maxdepth: 3



