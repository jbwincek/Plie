import plie
import time

item_three = """item three is significantly longer than the others, it shows that MultiText
can handle multiple lines well, including making sure the indent is right when a list is
bulleted. """

def run():
    a_view_dict = {
        'header' : {
            'bounds': plie.Bounds(width='100%', height=1),
            'view_object': plie.Text('title text', justify='right')
            },
        'body' : {
            'bounds': plie.Bounds(width='100%', height='50%'),
            'view_object': plie.MultiText(texts=('one','two two two', item_three),
                                          justify='left', bullet_choice='* '),
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


if __name__ == '__main__':
    run()