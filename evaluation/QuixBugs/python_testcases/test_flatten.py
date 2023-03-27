import pytest
from load_testdata import load_json_testcases

if pytest.use_correct:
    from correct_python_programs.flatten import flatten
else:
    from python_programs.flatten import flatten


testdata = load_json_testcases(flatten.__name__)


@pytest.mark.parametrize("input_data,expected", testdata)
def test_flatten(input_data, expected):
    assert list(flatten(*input_data)) == expected
