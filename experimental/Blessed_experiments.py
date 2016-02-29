
from blessed import Terminal
from collections import defaultdict
import time

term = Terminal()
render_plane = {}

def experiment_1():
    """
    Doesn't print to the last row.
    But term. handles wrapping so fills the screen otherwise

    """
    with term.fullscreen():
        with term.hidden_cursor():
            output = ''
            for y in range(term.height+1):
                for x in range(term.width):
                    output += render_plane.get((x,y), 'x')
            print(output)
            time.sleep(1.5)

def experiment_2():
    """
    Doesn't print to the last row either

    """
    with term.fullscreen():
        with term.hidden_cursor():
            output = ''
            for y in range(term.height):
                output += term.move_down()
                for x in range(term.width):
                    output += render_plane.get((x,y), 'x')
            print(output)
            time.sleep(1.5)

def experiment_3():
    """
      * * * * * * * * * * * * * * * * * * * * * * * * *
      *                                               *
      *    PRINT NEEDS END='' OTHERWISE IT WILL       *
      *    PROHIBIT FROM PRINTING TO THE LAST LINE    *
      *                                               *
      * * * * * * * * * * * * * * * * * * * * * * * * *
    """
    with term.fullscreen(), \
         term.hidden_cursor(), \
         term.raw(), \
         term.location(x=0, y=term.height):
                output = ''
                output += 'x' * term.width
                print(output, end = '', flush=True)
                time.sleep(1.5)



def experiment_4():
    """
    Doesn't print to the last row.
    But term. handles wrapping so fills the screen otherwise

    """
    with term.fullscreen():
        with term.hidden_cursor():
            output = ''
            for y in range(term.height):
                if y>0:
                    output += term.move_down
                for x in range(term.width):
                    output += render_plane.get((x,y), '.')
            print(output, end='')
            time.sleep(1.5)


def experiment_5():
    output = ''
    width = 10
    height = 10
    for y in range(height):
        if y > 0:
            output += term.move_down
        for x in range(width):
            output += render_plane.get((x, y), '.')
    print(len(output))
    print(output)




experiment_5()