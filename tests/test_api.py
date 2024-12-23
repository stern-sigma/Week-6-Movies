#pylint: skip-file
import pytest
from stern_movies_api.app import app
from unittest.mock import patch


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_endpoint_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to the Movie API"}


@patch('stern_movies_api.app.get_movies')
def test_endpoint_get_movies(mock_movies, client):
    response = client.get("/movies")
    assert response.status_code == 200


@patch('stern_movies_api.app.get_movie_by_id')
def test_endpoint_get_movie(mock_movies, client):
    response = client.get("/movies/1")
    assert response.status_code == 200
