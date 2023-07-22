import pytest
from load_testdata import load_json_testcases

if pytest.use_correct:
    from correct_python_programs.find_in_sorted import find_in_sorted
else:
    from python_programs.find_in_sorted import find_in_sorted


testdata = load_json_testcases(find_in_sorted.__name__)


@pytest.mark.parametrize("input_data,expected", testdata)
def test_find_in_sorted(input_data, expected):
    assert find_in_sorted(*input_data) == expected
