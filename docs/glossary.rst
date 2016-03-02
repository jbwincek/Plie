Glossary
========

.. glossary::

    **View**:
        A dictionary containing items (view objects) to render to the screen)

    **Field**:
        The various sections of a view. 'header', 'body', 'footer', 'styles' and 'util' are all fields.

    **View Object**:
        Something that gets displayed to the screen, makes up the view, gets put into view fields

    **Renderer**:
        A class to handle rendering, compositing of views and arranging view objects into screen space

    **Text**:
        A universal text displaying view object, that can handle changes from other places (via a
        callback), single line and multiple line displaying, text formatting. Also has an attribute
        for a callout where if the text is selected by another view object (like a menu) the function
        referenced in the callout will be called.

    **Multitext**:
        a sequence of text objects for creating menus



.. toctree::
   :maxdepth: 2
