import pytest
from load_testdata import load_json_testcases

if pytest.use_correct:
    from correct_python_programs.hanoi import hanoi
else:
    from python_programs.hanoi import hanoi


testdata = load_json_testcases(hanoi.__name__)
testdata = [[inp, [tuple(x) for x in out]] for inp, out in testdata]


@pytest.mark.parametrize("input_data,expected", testdata)
def test_hanoi(input_data, expected):
    assert hanoi(*input_data) == expected
