Plié: A Python Terminal User Interface Library
==============================================

Plié adds helper functions and context managers to `Curtsies`_ for creating more complex TUIs. One
of my main goals with Plié is to keep it simple, straight forward and Pythonic.

.. _Curtsies: https://github.com/thomasballinger/curtsies

The broad strokes of Plié:
**************************

:py:class:`plie.Text` is the meat and potatoes. It can handle
displaying single line text, multi line text (with different formatting options). If you want
:class:`plie.Text` to be a button, give it a callout function, if you want it to be updateable
give it a callback function.

:class:`plie.MultiText` adds on another layer to :class:`plie.Text` and serves as a container. If
you want a menu of selectable items, use :class:`plie.Multitext`, which is just a list filled
with :class:`plie.Text` as it's items.


:py:class:`plie.Renderer` is where all the action happens.


Ever wish creating a bordered screen in a terminal with a title only took a few lines of Python,
now it does. Lets see:



Currently implemented features:
-------------------------------
    * border: creates a border around an array
    * TitleBar: creates a title at the top of an array
    * array_insert: no more dealing with matching array sizes to slices.

Planned features:
-----------------
    * popup windows that can display text messages for a specified amount of time.
    * menus which contain multiple selectable items for interface control flow.
    * text flow helpers
    * compositing manager
    * support for different border styles
    * footer update-able text like the title


Other useful pages
------------------

.. toctree::
   :maxdepth: 3

   Plié development todo list <development_todo_list.rst>
   _plie_depreciated
   plie
   styles
   glossary
   renderer
   text
   multitext
   api_docs/modules

**Plié is in early alpha currently, all publicly exposed names and attributes may change during
alpha.**


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`



