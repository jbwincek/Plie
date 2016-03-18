import plie

default_sections = {
    'header': {
        'renderable': True,
        'positioning': plie.Position(vertical='0%', horizontal='50%'),
        'bounds': plie.Bounds(width='100%', height=1),
        'view_object': plie.Text,
        'contents': {
            'text': 'The header text',
            'justify': 'left'
        },
        'styles': None,
        'padding': 0,
    },
    'body': {
        'renderable': True,
        'positioning': plie.Position(vertical='50%', horizontal='50%'),
        'bounds': plie.Bounds(width='100%', height='100%-2'),
        'view_object': plie.Text,
        'contents': {},
        'styles': None,
        'padding': 0,
    },
    'footer': {
        'renderable': True,
        'positioning': plie.Position(vertical='100%', horizontal='50%'),
        'bounds': plie.Bounds(width='100%', height=1),
        'view_object': plie.Text,
        'contents': {
            'text': 'The footer text',
            'justify': 'center'
        },
        'styles': None,
        'padding': 0,
    },
    'util': {
        'renderable': False
    }
}
