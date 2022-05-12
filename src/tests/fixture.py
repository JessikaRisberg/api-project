import pytest
from src.app import create_app


@pytest.fixture
def client():
    url = 'http://127.0.0.1:5000' # The root url of the flask app

    return url