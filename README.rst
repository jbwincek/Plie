
Plié: A Python Terminal User Interface Library
==============================================

Plié helps you create interactive complexly laid out terminal applications with ease.



.. code-block:: Python

    import plie
    import time


    a_view_dict = {
        'header' : {
            'bounds': plie.Bounds(width='100%', height=1),
            'view_object': plie.Text('title text')
            },
        'body' : {
            'bounds': plie.Bounds(width='100%', height='50%'),
            'view_object': plie.Text('some text second line', justify='centered'),
            'positioning': plie.Position(vertical='centered', horizontal='centered'),
            'styles': []
            },
        'footer' : {
            'bounds': plie.Bounds(width='100%', height=2),
            'view_object': plie.Text("The footer...")
            },
        'util' : {'handles_input': 'body'}
    }

    a_view = plie.View(a_view_dict)

    renderer = plie.Renderer(view=a_view)
    renderer.display()
    time.sleep(2)

    a_view.body[0].view_object.update(text='look, the text changed')
    renderer.display()
    time.sleep(1)


My main goals with Plié is to keep it simple yet highly flexible, intuitive and Pythonic.

With those goals though comes a willingness to redesign the public facing API significantly for
the purpose of increasing intuitiveness or decreasing boilerplate until at least the 1.0 release.

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
    * solid asyncio event integration for handling a variety of events, including keyboard,
    timers and voice commands (via `speech_recognition`_)

.. _speech_recognition: https://pypi.python.org/pypi/SpeechRecognition/

Similar projects and libraries
------------------------------
    * `Blessings`_ by Eric Rose
    * `Blessed`_ by Jeff Quast
    * `Curtsies`_ by Thomas Ballinger (the spiritual predecessor to Plié and where the name derives from)
    * `npyscreen`_ by Nicholas Cole
    * `urwid`_ by Ian Ward et al


.. _Blessings: https://pypi.python.org/pypi/blessings
.. _Blessed: https://pypi.python.org/pypi/blessed
.. _Curtsies: https://github.com/thomasballinger/curtsies
.. _npyscreen: https://pypi.python.org/pypi/npyscreen/
.. _urwid: http://urwid.org/


**Plié is in early alpha currently**
The files with mockup or variations there of in the filename in the ``Plie/experimental`` directory, contain writings and experiments on the creation of various components of Plié.