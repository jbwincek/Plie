from blessed import Terminal


class Renderer():
    def __init__(self, size=(10,10), view=None):
        self.term = Terminal
        self.size = size
        self.dict = {}
    def formulate(self):
        output_list = []
        for y in range(self.size[1]):
            if y > 0:
                output_list.append('\n')
            output_list.extend([self.dict.get((x, y), ' ') for x in range(self.size[0])])
        return ''.join(output_list)
    def display(self):
        pass
