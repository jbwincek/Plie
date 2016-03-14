import plie

def test_basic():
    m = plie.MultiText(texts=['a','b','c'], bullet_choice='* ',bounds=(4,4))
    expected_output