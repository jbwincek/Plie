import plie

def test_basic():
    m = plie.MultiText(texts=['a','b','c'], bullet_choice='* ',bounds=(4,4))
    expected_output = \
"""* a
* b
* c"""
    assert str(m) == expected_output

def test_multiline_texts():
    test_texts = ['abc def', '123 456']
    m = plie.MultiText(texts=test_texts, bullet_choice='* ', bounds=(6,6))
    expected_output = \
"""* abc
  def
* 123
  456"""
    assert str(m) == expected_output


def test_basic_as_cells():
    m = plie.MultiText(texts=['a','b'], bullet_choice='',bounds=(4,4))
    expected_cells = {
        (0,0): 'a',
        (1,0): '',
        (0,1): 'b',
        (1,1): '',
    }
    got_cells = m.as_cells()
    for cell, value in expected_cells.items():
        assert got_cells[cell] == value

def test_basic_as_cells_with_bullet():
    m = plie.MultiText(texts=['a','b'], bullet_choice='* ',bounds=(4,4))
    expected_cells = {
        (0,0): '*',
        (1,0): ' ',
        (2,0): 'a',
        (0,1): '*',
        (1,1): ' ',
        (2,1): 'b',
    }
    got_cells = m.as_cells()
    for cell, value in expected_cells.items():
        assert got_cells[cell] == value

def test_iterating_over_containing_Texts():
    m = plie.MultiText(texts=['a','b','c','d'])
    for text in m:
        assert isinstance(text, plie.Text)

def test_iterating_contains_right_stuff():
    test_list = ['a','b','c','d']
    m = plie.MultiText(texts=test_list)
    for i, text in enumerate(m):
        assert test_list[i] == str(text)