import pytest
from load_testdata import load_json_testcases

if pytest.use_correct:
    from correct_python_programs.next_palindrome import next_palindrome
else:
    from python_programs.next_palindrome import next_palindrome


testdata = load_json_testcases(next_palindrome.__name__)


@pytest.mark.parametrize("input_data,expected", testdata)
def test_next_palindrome(input_data, expected):
    assert next_palindrome(*input_data) == expected
