#!/usr/bin/env python3
import plie


"""Method 1: the speech_recognition background listening example"""

import speech_recognition as sr

# this is called from the background thread
def sr_example_callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    print(recognizer, audio)
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said " + recognizer.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def run_1():
    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening

    # start listening in the background (note that we don't have to do this inside a `with` statement)
    stop_listening = r.listen_in_background(m, sr_example_callback)
    # `stop_listening` is now a function that, when called, stops background listening

    # do some other computation for 5 seconds, then stop listening and keep doing other computations
    import time
    for _ in range(50): time.sleep(0.1) # we're still listening even though the main thread is doing other things
    stop_listening() # calling this function requests that the background listener stop listening
    while True: time.sleep(0.1)

# run_1()

"""
Notes on method 1:
    * recognizer.recognize_wit is the one to use for wit.ai
    * The callback gets called with a speech_recognition recognizer instance, and an AudioData
    instance.
        * They seem to be passed as positional arguments, and therefore a universal event handler
        would need to accept arbitrary positional arguments, and sort out the arguments by
        isinstance()-ing things. that would work though.
"""



"""
Method 2: wit.ai and speech-recognition
"""
#
# with open('wit_key', 'r') as key_file:
#     KEY = key_file.read().strip()


def wit_example_callback(recognizer, audio_data):
    print('processing audio..')
    print(recognizer.recognize_wit(audio_data, KEY, show_all=True))


def run_2():
    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source)
    import time
    stop_listening = r.listen_in_background(m, wit_example_callback)
    print('listening...')
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        stop_listening()
        quit()

# run_2()

"""
Notes on method 2:
    * It's a bit slow, there's almost a second long delay for processing
    * works pretty well though, except for the slowness
    * using a non-background listener in some fashion might work a bit better since it would be
    tunable

"""



"""
Notes on method 3: Unified event handling (but actually not)
"""
import asyncio
from blessed import Terminal
from functools import partial

#
# with open('wit_key', 'r') as key_file:
#     KEY = key_file.read().strip()

@asyncio.coroutine
def handle_keyboard(future):
    term = Terminal()
    with term.cbreak():
        keypress = term.inkey()
    #print('got: {}'.format(keypress))
    future.set_result(keypress)


async def handle_audio():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio_data = await recognizer.listen(source)
    print('listening...')
    response = await recognizer.recognize_wit(audio_data, KEY, show_all=True)
    print('got: {}'.format(response))


def run_3():

    loop = asyncio.get_event_loop()
    future = asyncio.Future()

    #loop.create_task(handle_audio())
    asyncio.ensure_future(handle_keyboard(future))
    loop.run_until_complete(future)
    print('got: {}'.format(future.result()))
    loop.close()

#run_3()



"""
Notes on method 3:
    * NOTE: method 3 only does keyboard input handling
    * Works perfectly well for running something once, does exactly what it should, so that's nice.
    * quick experimentation into alternative methods to get it to loop seemed tricky.
"""



"""
Method 4:
"""



@asyncio.coroutine
def handle_keyboard(future):
    term = Terminal()
    with term.cbreak():
        keypress = term.inkey()
    #print('got: {}'.format(keypress))
    future.set_result(keypress)

def run_4():

    loop = asyncio.get_event_loop()


    #loop.create_task(handle_audio())

    while True:
        future = asyncio.Future()
        asyncio.ensure_future(handle_keyboard(future))
        loop.run_until_complete(future)
        result = future.result()
        print('got: {}'.format(result))
        if result == 'q':
            break
    loop.close()

# run_4()

"""
Notes on Method 4:
    * So this works as a way to get keyboard input
    * I suspect it's blocking though, and that it didn't accomplish any async magic,
    like it seems just the same as a regular event loop with a lot of boilerplate around it instead
"""


"""
Method 5: trying for unified handling again with looping keyboard input
"""



@asyncio.coroutine
def wit_example_callback(recognizer, audio_data, future=None):
    print('processing audio..')
    result = recognizer.recognize_wit(audio_data, KEY, show_all=True)
    future.set_result(result)


@asyncio.coroutine
def handle_keyboard(future):
    term = Terminal()
    with term.cbreak():
        keypress = term.inkey()
    #print('got: {}'.format(keypress))
    future.set_result(keypress)


def run_5():
    loop = asyncio.get_event_loop()
    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source)

    audio_future = asyncio.Future()
    stop_listening = r.listen_in_background(m, partial(wit_example_callback, future=audio_future))


    while True:
        keyboard_future = asyncio.Future()
        asyncio.ensure_future(handle_keyboard(keyboard_future))
        loop.run_until_complete(keyboard_future)
        result = keyboard_future.result()
        print('got: {}'.format(result))
        if result == 'q':
            break
    loop.close()


"""
Notes on method 5:
    No notes for right now
"""


"""
Method 6: actually using Plié for text display
"""

test_view = {
    'header': {
        'contents': {
            'justify': 'left',
            'text': 'input handler test'
        }
    },
    'body': {
        'contents': {
            'text' : ''
        }
    },
    'footer': {
        'contents' : {
            'text' : 'The footer text'
        }
    }
}

@asyncio.coroutine
def handle_keyboard(future):
    term = Terminal()
    with term.cbreak():
        keypress = term.inkey()
    #print('got: {}'.format(keypress))
    future.set_result(keypress)

def run_6():
    loop = asyncio.get_event_loop()
    renderer = plie.Renderer(view=test_view)
    display_string = ''
    while True:
        renderer.display()
        future = asyncio.Future()
        asyncio.ensure_future(handle_keyboard(future))
        loop.run_until_complete(future)
        result = future.result()
        display_string += result
        renderer.view['body']['instance'].update(text=display_string)
        if result == 'q':
            break
    loop.close()

#run_6()

""" Notes on method 6:
    * works
    * is a bit slow (actually about the same speed as typing in PyCharm) so reasonable for just text
      editing or similar activities.
        * seems related to all the steps required for updating the screen via a Text instance
    * the cursor isn't in the right position
"""

""" Experiment 7: striving for keyboard interactivity
"""

from blessed import keyboard
from functools import partial

LEFT = (0, -1)
RIGHT = (0, 1)
UP = (-1, 0)
DOWN = (1, 0)

@asyncio.coroutine
def handle_keyboard_input(future, term):

    with term.cbreak():
        keypress = term.inkey()
        future.set_result(keypress)

def process_result(result, term, location):
    """
    Args:
        result: the input key to be processed
        term: the terminal where this is happening
        location: the current location of the cursor

    Returns: an updated location

    """
    #print('got: {}'.format(repr(result)))
    if result.code in (term.KEY_UP, term.KEY_DOWN, term.KEY_LEFT, term.KEY_RIGHT):
        if result.code == term.KEY_UP:
            location = (sum(x) for x in zip(location, UP))
        elif result.code == term.KEY_DOWN:
            location = (sum(x) for x in zip(location, DOWN))
        elif result.code == term.KEY_LEFT:
            location = (sum(x) for x in zip(location, LEFT))
        else:
            location = (sum(x) for x in zip(location, RIGHT))
    return location


def run_7():
    term = Terminal()
    loop = asyncio.get_event_loop()
    #renderer = plie.Renderer(view=test_view)
    current_loc = (10,10)
    with term.fullscreen():
        while True:
            #renderer.display()
            future = asyncio.Future()
            asyncio.ensure_future(handle_keyboard_input(future, term))
            loop.run_until_complete(future)
            current_loc = process_result(future.result(), term, current_loc)
            with term.location(*current_loc):
                print('x',end='')

#run_7()

""" Notes about experiment 7
    * Doesn't move the cursor, the cursor stays in the location put at the beginning
"""

""" Experiment 8:
"""

def process_result(result, term):
    """
    Args:
        result: the input key to be processed
        term: the terminal where this is happening
        location: the current location of the cursor

    Returns: an updated location

    """
    #print('got: {}'.format(repr(result)))
    if result.code in (term.KEY_UP, term.KEY_DOWN, term.KEY_LEFT, term.KEY_RIGHT):
        if result.code == term.KEY_UP:
            return UP
        elif result.code == term.KEY_DOWN:
            return DOWN
        elif result.code == term.KEY_LEFT:
            return LEFT
        else:
            return RIGHT
    else:
        return (0,0)


def run_8():
    term = Terminal()
    current_loc = (10, 10)
    loop = asyncio.get_event_loop()
    while True:
        future = asyncio.Future()
        asyncio.ensure_future(handle_keyboard_input(future, term))
        loop.run_until_complete(future)
        move_where = process_result(future.result(), term)
        current_loc = (sum(x) for x in zip(current_loc, move_where))
        with term.fullscreen(), term.location(*current_loc):
            print(move_where)



# run_8()

""" Notes on experiment 8:
    * this doesn't work, and idk why.
    * it doesn't even go full screen
"""

"""
Experiment 9:
"""

@asyncio.coroutine
def handle_keyboard(future):
    term = Terminal()
    with term.cbreak():
        keypress = term.inkey()
    #print('got: {}'.format(keypress))
    future.set_result(keypress)

async def c_handle_keyboard(loop, future, current_loc, term):
    await asyncio.ensure_future(handle_keyboard(future))
    loop.run_until_complete(future)
    result = await future.result()
    move_where = process_result(future.result(), term)
    current_loc = (sum(x) for x in zip(current_loc, move_where))
    with term.fullscreen(), term.location(*current_loc):
        print(move_where)
    return result

def process_result_b(result, term):
    """
    Args:
        result: the input key to be processed
        term: the terminal where this is happening
        location: the current location of the cursor

    Returns: an updated location

    """
    #print('got: {}'.format(repr(result)))
    if result.code in (term.KEY_UP, term.KEY_DOWN, term.KEY_LEFT, term.KEY_RIGHT):
        if result.code == term.KEY_UP:
            return UP
        elif result.code == term.KEY_DOWN:
            return DOWN
        elif result.code == term.KEY_LEFT:
            return LEFT
        else:
            return RIGHT
    else:
        return (0,0)

def run_9():
    term = Terminal()
    current_loc = (10, 10)
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    future = asyncio.Future()
    loop.create_task(c_handle_keyboard(loop, future, current_loc, term))


# run_9()

"""
Task was destroyed but it is pending!
"""


"""
Experiment 10
"""


def d_handle_keyboard(term):
    print('d_handle_keyboard() entered')
    try:
        with term.cbreak():
            while True:
                #print('looped')
                yield term.inkey()
    except KeyboardInterrupt:
        exit()

def run_10():
    term = Terminal()
    with term.fullscreen():
        for key in d_handle_keyboard(term):
            print(key, end='', flush=True)

# run_10()

"""
Notes on experiment 10:
    * it works
    * stripped down to it's core
    * the flush=True for print statement is VERY IMPORTANT
        * it won't print without it, and look like something is going horribly wrong
    * term being passed around in this context seems okay
"""


"""
Experiment 11:
"""

def e_handle_keyboard(term):
    try:
        with term.cbreak():
            while True:
                yield term.inkey()
    except KeyboardInterrupt:
        exit()

def run_11():
    renderer = plie.Renderer(view=test_view)
    display_string = ''
    renderer.display()
    for key in e_handle_keyboard(renderer.term):
        display_string += key
        renderer.view['body']['instance'].update(text=display_string)
        renderer.display()


run_11()

"""
Notes on Experiment 11:
    * It works.
    * puts a lot of business logic in the main run loop
    * doesn't handle special/control characters well (like arrow keys allow you to change stuff
    in the title)
    * yanking the Terminal instance out of renderer seems like an okay idea at least, not great,
    but okay

"""










"""
Version of Method 3 that didn't work but saving it just in case
"""


#
# import asyncio
# from blessed import Terminal
# from functools import partial
#
#
# # with open('wit_key', 'r') as key_file:
# #     KEY = key_file.read().strip()
#
# @asyncio.coroutine
# def handle_keyboard(future):
#     term = Terminal()
#     with term.cbreak():
#         keypress = term.inkey()
#     #print('got: {}'.format(keypress))
#     future.set_result(keypress)
#
#
# async def handle_audio():
#     recognizer = sr.Recognizer()
#     microphone = sr.Microphone()
#     with microphone as source:
#         recognizer.adjust_for_ambient_noise(source)
#         audio_data = await recognizer.listen(source)
#     print('listening...')
#     response = await recognizer.recognize_wit(audio_data, KEY, show_all=True)
#     print('got: {}'.format(response))
#
# async def b_handle_keyboard(loop):
#     future = asyncio.Future()
#     asyncio.ensure_future(handle_keyboard(future))
#     loop.run_until_complete(future)
#     result = await future.result()
#     return result
#
# def run_3():
#     loop = asyncio.get_event_loop()
#
#     loop.create_task(b_handle_keyboard(loop))

# run_3()

