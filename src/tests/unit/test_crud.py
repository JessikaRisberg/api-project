import requests


url = 'http://127.0.0.1:5000' # The root url of the flask app


def test_create_dog():
    r = requests.get(url + '/dog/create')
