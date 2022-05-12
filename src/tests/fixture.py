import pytest
from src.app import create_app


@pytest.fixture
def client():
    app = create_app()

    app.config['TESTING']

    with app.app_context() as api_client:
        yield api_client