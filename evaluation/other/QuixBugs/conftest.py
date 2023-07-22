import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--correct", action="store_true", help="run tests on the correct version"
    )
    parser.addoption("--runslow", action="store_true", help="run slow tests")


def pytest_configure(config):
    pytest.use_correct = config.getoption("--correct")
    pytest.run_slow = config.getoption("--runslow")
