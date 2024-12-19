from typing import Any
import pytest  # type: ignore


def pytest_addoption(parser: Any) -> None:
    parser.addoption('--slow', action='store_true', dest="slow", default=False, help="Run slow tests")


def pytest_configure(config: Any) -> None:
    config.addinivalue_line("markers", "slow: mark test as slow test")


def pytest_collection_modifyitems(config: Any, items: Any) -> None:
    slow = config.getoption("--slow")
    skip_slow = pytest.mark.skip(reason="need --slow option to run")
    for item in items:
        if not slow and "slow" in item.keywords:
            item.add_marker(skip_slow)
