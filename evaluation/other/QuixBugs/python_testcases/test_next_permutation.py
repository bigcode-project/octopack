import pytest
from load_testdata import load_json_testcases

if pytest.use_correct:
    from correct_python_programs.next_permutation import next_permutation
else:
    from python_programs.next_permutation import next_permutation


testdata = load_json_testcases(next_permutation.__name__)


@pytest.mark.parametrize("input_data,expected", testdata)
def test_next_permutation(input_data, expected):
    assert next_permutation(*input_data) == expected
