from plie import CellSpace

test_cells = {
    (0, 0): ' ',
    (0, 1): ' ',
    (0, 2): ' ',
    (1, 0): ' ',
    (1, 1): 'a',
    (1, 2): ' ',
    (2, 0): ' ',
    (2, 1): ' ',
    (2, 2): ' ',
}


def test_basic_assignment_and_slice():
    c = CellSpace()
    for x, y in [(x, y) for y in range(10) for x in range(10)]:
        c[(x, y)] = (x*3)*(y*7)
    assert c[3:4,3:4][(0,0)] == 189


def test_unbounded_slicing():
    c = CellSpace()
    for x, y in [(x, y) for y in range(10) for x in range(10)]:
        c[(x, y)] = (x * 3) * (y * 7)
    got = c[:,:]
    assert len(got) == len(c)
    assert got == c


def test_whole_column():
    c = CellSpace()
    for x, y in [(x, y) for y in range(3) for x in range(3)]:
        c[(x, y)] = x + y*10
    got = c[0,:]
    for key in got.keys():
        # make sure we actually got the left most column
        assert got[key] % 10 == 0
    # and that we got the right number of items
    assert len(got) == 3


def test_whole_row():
    c = CellSpace()
    for x, y in [(x, y) for y in range(3) for x in range(3)]:
        c[(x, y)] = x*10 + y
    got = c[:, 0]
    for key in got.keys():
        # make sure we actually got the left most column
        assert got[key] % 10 == 0
    # and that we got the right number of items
    assert len(got) == 3


def test_partial_column_slice_gets_right_amount_of_items():
    c = CellSpace()
    for x, y in [(x, y) for y in range(10) for x in range(10)]:
        c[(x, y)] = x + y * 10
    got = c[0,2:8]
    assert len(got) == 6


def test_partial_row_slice_gets_right_amount_of_items():
    c = CellSpace()
    for x, y in [(x, y) for y in range(10) for x in range(10)]:
        c[(x, y)] = x + y * 10
    got = c[2:8, 0]
    assert len(got) == 6


def test_height_and_width():
    c = CellSpace()
    for x, y in [(x, y) for y in range(10) for x in range(10)]:
        c[(x, y)] = x + y * 10
    assert c.height == 10
    assert c.width == 10


def test_stride_basic():
    c = CellSpace()
    for x, y in [(x, y) for y in range(10) for x in range(10)]:
        c[(x, y)] = x + y * 10
    got = c[::2,::2]
    assert got.width == 5
    assert got.width == 5


def test_inverse():
    c = CellSpace()
    for x, y in [(x, y) for y in range(3) for x in range(3)]:
        c[(x, y)] = x * 10 + y
    got = c[::-1, ::-1]
    assert got[(0,0)] == 22