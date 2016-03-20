Plié: A Python Terminal User Interface Library
==============================================

Plié helps you create interactive complexly laid out terminal applications with ease.
Plié can be used to create single pane, or multi-pane layouts. It strives to be fast and precise
enough that you could use it for a rogue like rpg, while still being easy enough to pick up in
a few minutes.


The broad strokes of Plié:
**************************

:py:class:`plie.Text` is the meat and potatoes. It can handle
displaying a single line text or whole paragraphs of text. If you want
:class:`plie.Text` to be a button, give it a callout function, if you want it to be updateable
give it a callback function.

:class:`plie.MultiText` adds on another layer to :class:`plie.Text` and serves as a container. If
you want a menu of selectable items, use :class:`plie.Multitext`, which is just a list filled
with :class:`plie.Text` as it's items.

Both :py:class:`plie.Text` and :class:`plie.MultiText` have ``update()`` methods, which allow you
 to update the contents of them, and have the updated contents be shown the next time the screen
 is rendered.

:py:class:`plie.Renderer` is where all the action happens. :class:`plie.Renderer` takes what is
called a 'valid view dict' which represents a layout of everything on the screen, and displays it
 to the terminal.





Currently implemented features:
-------------------------------
    * Basic layouts, with a header, body and footer
    * rendering text to the screen, and updating text
    * support for different border styles


Planned features:
-----------------
    * popup windows that can display text messages for a specified amount of time.
    * menus which contain multiple selectable items for interface control flow.
    * solid asyncio event integration for handling a variety of events, including keyboard, timers and voice commands (via `speech_recognition`_)

.. _speech_recognition: https://pypi.python.org/pypi/SpeechRecognition/


Other useful pages
------------------

.. toctree::
   :maxdepth: 3

   plie
   renderer
   text
   multitext
   view
   styles
   glossary
   Plié development todo list <development_todo_list.rst>

**Plié is in early alpha currently, all publicly exposed names and attributes may change during
alpha.**


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`



