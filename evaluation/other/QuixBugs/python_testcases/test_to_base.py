import pytest
from load_testdata import load_json_testcases

if pytest.use_correct:
    from correct_python_programs.to_base import to_base
else:
    from python_programs.to_base import to_base


testdata = load_json_testcases(to_base.__name__)


@pytest.mark.parametrize("input_data,expected", testdata)
def test_to_base(input_data, expected):
    assert to_base(*input_data) == expected
