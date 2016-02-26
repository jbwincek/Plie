Plié: A Python Terminal User Interface Library
==============================================

Plié adds helper functions and context managers to `Curtsies`_ for creating more complex TUIs.

.. _Curtsies: https://github.com/thomasballinger/curtsies

Ever wish creating a bordered screen in a terminal with a title only took a few lines of Python,
now it does. Lets see::

    from curtsies import FullscreenWindow, FSArray
    from plie import border, TitleBar

    def run():
        with FullscreenWindow() as win:
            base_array = FSArray(15, 30)
            with border(base_array):
                with TitleBar(base_array, text='The Title') as title_bar:
                    win.render_to_terminal(base_array)
                    time.sleep(1.5)
                    title_bar.text = 'New Updated Title'
                    win.render_to_terminal(base_array)
                    time.sleep(1.5)


Currently implemented features:
    * border: creates a border around an array
    * TitleBar: creates a title at the top of an array
    * array_insert: no more dealing with matching array sizes to slices. 