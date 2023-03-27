import pytest
from load_testdata import load_json_testcases

if pytest.use_correct:
    from correct_python_programs.sqrt import sqrt
else:
    from python_programs.sqrt import sqrt


testdata = load_json_testcases(sqrt.__name__)


@pytest.mark.parametrize("input_data,expected", testdata)
def test_sqrt(input_data, expected):
    # assert sqrt(*input_data) == pytest.approx(expected, abs=input_data[-1])
    # Can also be written w/o pytest dependency:
    assert abs(sqrt(*input_data) - expected) <= input_data[-1]
