import pytest
from load_testdata import load_json_testcases

if pytest.use_correct:
    from correct_python_programs.bitcount import bitcount
else:
    from python_programs.bitcount import bitcount


testdata = load_json_testcases(bitcount.__name__)


@pytest.mark.parametrize("input_data,expected", testdata)
def test_bitcount(input_data, expected):
    assert bitcount(*input_data) == expected
