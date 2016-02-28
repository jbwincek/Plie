Plié: A Python Terminal User Interface Library
==============================================

Plié adds helper functions and context managers to `Curtsies`_ for creating more complex TUIs. One
of my main goals with Plié is to keep it simple, straight forward and Pythonic.

.. _Curtsies: https://github.com/thomasballinger/curtsies

Ever wish creating a bordered screen in a terminal with a title only took a few lines of Python,
now it does. Lets see:

.. code-block:: Python

    from curtsies import FullscreenWindow, FSArray  # Plié is built on curtsies
    from plie import border, TitleBar
    import time

    def run():
        with FullscreenWindow() as win:  # Create a window to render to
            base_array = FSArray(15, 30)  # Arrays are where all the text goes
            with border(base_array):  # add a border onto the array we just made
                with TitleBar(base_array, text='The Title') as title_bar: # add a title as well
                    win.render_to_terminal(base_array) # render the array
                    time.sleep(1.5)  # if this wasn't here, all this would happen in a flash
                    title_bar.text = 'New Updated Title' # change the title text
                    win.render_to_terminal(base_array)
                    time.sleep(1.5)


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
   plie
   styles


**Plié is in early alpha currently, all publicly exposed names and attributes may change during
alpha.**


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`



