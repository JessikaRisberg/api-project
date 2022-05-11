from ..fixture import client


def test_home_page():
    response = client.get('/user')
    assert response.status_code == 200