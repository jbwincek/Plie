from collections import UserDict
from numbers import Integral


class CellSpace(UserDict):
    """ CellSpace adds 2D slicing and bounds information to dicts of (x,y) coordinate pairs.

    Notes: CellSpace does not support assigning by slice at this point.
           Height and width are not absolute measures of how many cells CellSpace contains in
           either direction. Instead they show the max labeled cell, this can be considered
           either a bug or a feature. Max labeled cell in this case means the cell with the
           largest index in that direction (height or width).
    """

    def __init__(self, *args, **kwargs):
        self.width = 1
        self.height = 1
        super().__init__(*args, **kwargs)


    def __setitem__(self, key, item):
        self.data[key] = item
        if isinstance(key,(tuple,list,set)):
            if key[0] >= self.width:
                self.width = key[0] + 1
            if key[1] >= self.height:
                self.height = key[1] + 1

    def __getitem__(self, index):
        cls = type(self)
        new_cells = cls()
        width = self.width
        height = self.height

        try:
            # handle the case where both items are integers [int,int] aka cell case
            return self.data[(index[0], index[1])]

        except TypeError:
            if isinstance(index, tuple) and isinstance(index[0], slice) and isinstance(index[1],
                                                                                        slice):
                # handle the case where both items are slices aka box case
                x_s = index[0].indices(width) # indices returns a (start, stop, stride) tuple
                y_s = index[1].indices(height)
                for y_index, y in enumerate(range(*y_s)):
                    for x_index, x in enumerate(range(*x_s)):
                        new_cells[(x_index, y_index)] = self.data[(x, y)]
                return new_cells

            elif isinstance(index, tuple) and isinstance(index[0], slice) and isinstance(index[1], Integral):
                # handle the case where x is a slice, but y is an integer [int:int, int] aka row case
                x_s = index[0].indices(width)
                for x_index, x in enumerate(range(*x_s)):
                    new_cells[(x_index, 0)] = self.data[(x, index[1])]
                return new_cells

            elif isinstance(index, tuple) and isinstance(index[0], Integral) and isinstance(index[1], slice):
                # handle the case where x is an integer, but y is a slice [int, int:int] aka column case
                y_s = index[1].indices(height)
                for y_index, y in enumerate(range(*y_s)):
                    new_cells[(0, y_index)] = self.data[(index[0], y)]
                return new_cells

            else:
                msg = '{cls.__name__} indices must be integers'
                raise TypeError(msg.format(cls=cls))