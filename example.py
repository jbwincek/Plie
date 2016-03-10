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