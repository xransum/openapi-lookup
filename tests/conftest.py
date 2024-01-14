"""Config file for pytest."""
import os
import pytest


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data")


@pytest.fixture
def test_data_dir() -> str:
    """Return test data directory."""
    return TEST_DATA_DIR
