
Plié: A Python Terminal User Interface Library
==============================================

Plié helps you create interactive complexly laid out terminal applications with ease.

My main goals with Plié is to keep it simple yet highly flexible, intuitive and Pythonic.

With those goals though comes a willingness to redesign the public facing API significantly for
the purpose of increasing intuitiveness or decreasing boilerplate until at least the 1.0 release.

Currently implemented features:
-------------------------------
    * Nothing because of in progress rewrite from scratch

Planned features / wish list:
-----------------------------
    * ability to handle anything from character fields to flowing text
    * color and style
    * popup windows that can display text messages for a specified amount of time
    * menus which contain multiple selectable items for interface control flow
    * drop down menus and tooltip like widgets
    * multipane layouts
    * support for different border and background styles
    * solid async event integration for handling a variety of events, including keyboard,
    timers and voice commands (via `speech_recognition`_)

.. _speech_recognition: https://pypi.python.org/pypi/SpeechRecognition/

Similar projects and libraries
------------------------------
    * `Blessings`_ by Eric Rose
    * `Blessed`_ by Jeff Quast
    * `Curtsies`_ by Thomas Ballinger (the spiritual predecessor to Plié and where the name derives from)
    * `npyscreen`_ by Nicholas Cole
    * `urwid`_ by Ian Ward et al
    * `picotui`_ by Paul Sokolovsky


.. _Blessings: https://pypi.python.org/pypi/blessings
.. _Blessed: https://pypi.python.org/pypi/blessed
.. _Curtsies: https://github.com/thomasballinger/curtsies
.. _npyscreen: https://pypi.python.org/pypi/npyscreen/
.. _urwid: http://urwid.org/
.. _picotui: https://github.com/pfalcon/picotui


**Plié is in early alpha currently**
The files with mockup or variations there of in the filename in the ``Plie/experimental`` directory, contain writings and experiments on the creation of various components of Plié.