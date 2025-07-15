import pytest


@pytest.fixture(scope="session")
def sample_data():
    return [
        {"name": "Test1", "value": "10"},
        {"name": "Test2", "value": "20"}
    ]