import pytest
from api_framework.client import APIClient

@pytest.fixture(scope="session")
def client():
    return APIClient()
