import pytest
from load_testdata import load_json_testcases

if pytest.use_correct:
    from correct_python_programs.lis import lis
else:
    from python_programs.lis import lis


testdata = load_json_testcases(lis.__name__)


@pytest.mark.parametrize("input_data,expected", testdata)
def test_lis(input_data, expected):
    assert lis(*input_data) == expected
