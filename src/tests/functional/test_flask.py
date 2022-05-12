"""
Functional test on http://127.0.0.1/5000 routes
"""
import requests

url = 'http://127.0.0.1:5000' # The root url of the flask app

def test_index_page():
    """
    Test the HTTP status code for index page
    :return: None
    """
    r = requests.get(url+'/') # Assumses that it has a path of "/"
    assert r.status_code == 200 # Assumes that it will return a 200 response


def test_user_page():
    """
    Test the HTTP status code for user page
    :return: None
    """
    r = requests.get(url+'/user')
    assert r.status_code == 200