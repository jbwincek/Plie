import plie

def test_section_empty_counts_as_false():
    section = plie.Section()
    if not section:
        assert True
    else:
        raise AssertionError

def test_section_filled_counts_as_true():
    section = plie.Section(bounds=(25,25))
    if section:
        assert True
    else:
        raise AssertionError

def test_section_repr():
    # This is probably a dumb test, but it assures repr formatting for Section is precisely accurate
    from plie import Section
    evaluabte = "Section(bounds=(25, 25), positioning=('centered', 'centered'), view_object=None, styles=[])"
    s = eval(evaluabte)
    assert repr(s) == evaluabte

