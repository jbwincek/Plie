import plie
import time

def run():
    a_view_dict = {
        'header' : {
            'bounds': plie.Bounds(width='100%', height=1),
            'view_object': plie.Text('title text')
            },
        'body' : {
            'bounds': plie.Bounds(width='100%', height='50%'),
            'view_object': plie.MultiText(texts=('one','two two two', 'three three'),
                                          justify='left'),
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