Plié: A Python Terminal User Interface Library
==============================================

Plié helps you create interactive complexly laid out terminal applications with ease.


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





Currently implemented features:
-------------------------------
    * Basic layouts, with a header, body and footer
    * rendering text to the screen, and updating text
    * formatting helpers for fitting text in limited or tall spaces


Planned features:
-----------------
    * popup windows that can display text messages for a specified amount of time.
    * menus which contain multiple selectable items for interface control flow.
    * support for different border styles
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



