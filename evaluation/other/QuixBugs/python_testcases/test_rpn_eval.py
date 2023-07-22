import pytest
from load_testdata import load_json_testcases

if pytest.use_correct:
    from correct_python_programs.rpn_eval import rpn_eval
else:
    from python_programs.rpn_eval import rpn_eval


testdata = load_json_testcases(rpn_eval.__name__)


@pytest.mark.parametrize("input_data,expected", testdata)
def test_rpn_eval(input_data, expected):
    assert rpn_eval(*input_data) == expected
