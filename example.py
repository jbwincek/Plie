from curtsies import FullscreenWindow, FSArray
from plie._plie_depreciated import border, TitleBar
import time

def run():
    with FullscreenWindow() as win:
        base_array = FSArray(15, 30)
        with border(base_array, border_style='rounded'):
            with TitleBar(base_array, text='The Title') as title_bar:
                win.render_to_terminal(base_array)
                time.sleep(5)
                title_bar.text = 'new title'
                win.render_to_terminal(base_array)
                time.sleep(1.5)


if __name__ == '__main__':
    run()