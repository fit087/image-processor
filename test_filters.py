import filters

def test_denominator():
  denominator = filters.denominator(9,3)
  assert denominator == 11
