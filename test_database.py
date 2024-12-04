#pylint: skip-file

from unittest.mock import patch
import pytest
from datetime import date

from database import (get_movies, get_movie_by_id, create_movie, 
                      get_genre_id, get_country_id, get_status_id,
                      get_language_id)


@pytest.fixture(autouse=True)
def mock_connection():
    with patch('psycopg2.connect') as mock_connect:
        mock_con = mock_connect.return_value
        mock_cur = mock_con.cursor.return_value
        yield mock_con, mock_cur
        assert mock_con.close.called, "Connection not closed."


@pytest.mark.parametrize("sort_by,sort_order",
                         [
                            ('foo', 'ASC'),
                            ('bar', 'DESC'),
                            ('title', 'foo'),
                            ('date', 'score'),
                            ('genre', 'status'), 
                            ('language', 'budget'),
                            ('revenue', 'country')
                         ])
def test_get_movies_rejects_bad_input_values(sort_by, sort_order):
    with pytest.raises(ValueError):
        get_movies(sort_by=sort_by, sort_order=sort_order)

def test_get_movies_return(mock_connection):
    _, mock_cur = mock_connection
    mock_cur.fetchall.side_effect = [
        [{'movie_id': 1}],  # First call
        [{'genre_name': 'sci-fi'}]  # Second call
    ]
    assert get_movies() == [{'movie_id': 1, 'genres': ['sci-fi']}]

def test_get_movie_by_id_value_reject(mock_connection):
    _, mock_cur = mock_connection
    mock_cur.fetchone.return_value = None
    with pytest.raises(ValueError):
        get_movie_by_id(1)

@pytest.mark.parametrize('inp',
                        [
                            3.14,
                            "Hello, Sigma!",
                            [1, 2, 3],
                            (4, 5, 6),
                            {1, 2, 3},
                            {"key": "value"},
                            None,
                            True,
                        ])
def test_get_movie_by_id_type_reject(inp):
    with pytest.raises(TypeError):
        get_movie_by_id(inp)

def test_get_movie_by_id_good(mock_connection):
    _, mock_cur = mock_connection
    mock_cur.fetchone.return_value = {'foo': 'bar'}
    movie = get_movie_by_id(1)
    assert movie == {'foo': 'bar'}

def test_get_genre_id(mock_connection):
    _, mock_cur = mock_connection
    mock_cur.fetchone.return_value = {}
    with pytest.raises(ValueError):
        get_genre_id(1)

def test_get_status_id(mock_connection):
    _, mock_cur = mock_connection
    mock_cur.fetchone.return_value = {}
    with pytest.raises(ValueError):
        get_status_id(1)

def test_get_language_id(mock_connection):
    _, mock_cur = mock_connection
    mock_cur.fetchone.return_value = {}
    with pytest.raises(ValueError):
        get_language_id(1)

def test_get_country_id(mock_connection):
    _, mock_cur = mock_connection
    mock_cur.fetchone.return_value = {}
    with pytest.raises(ValueError):
        get_country_id(1)




@pytest.mark.parametrize('title,release_date,genre,overview,status,budget,revenue,country,language,orig_title',
                        [
                            ("A title", "WrongType", "Genre", "Overview", "Status", 1000000, 2000000, "Country", "Language", "Original Title"), # Incorrect type for release_date
                            ("A title", None, "Genre", "Overview", "Status", 1000000, 2000000, "Country", "Language", "Original Title"), # release_date is None
                            ("A title", date.today(), 123, "Overview", "Status", 1000000, 2000000, "Country", "Language", "Original Title"), # Incorrect type for genre
                            ("A title", date.today(), "Genre", "Overview", {}, 1000000, 2000000, "Country", "Language", "Original Title"), # Incorrect type for status
                            ("A title", date.today(), "Genre", "Overview", "Status", "One million", 2000000, "Country", "Language", "Original Title"), # Incorrect type for budget
                            ("A title", date.today(), "Genre", "Overview", "Status", 1000000, None, "Country", "Language", "Original Title"), # revenue is None
                            ("A title", date.today(), "Genre", "Overview", "Status", 1000000, 2000000, [], "Language", "Original Title"), # Incorrect type for country
                            ("A title", date.today(), "Genre", "Overview", "Status", 1000000, 2000000, "Country", 1234, "Original Title"), # Incorrect type for language
                            (None, date.today(), "Genre", "Overview", "Status", 1000000, 2000000, "Country", "Language", "Original Title"), # Title is None
                            ("A title", date.today(), "Genre", "Overview", "Status", "Budget", "Revenue", "Country", "Language", 1234), # Incorrect types for budget and revenue
                            ("A title", date.today(), "Genre", "Overview", "Status", 1000000, 2000000, True, "Language", "Original Title"), # Incorrect type for country
                            ("A title", (2023, 10, 23), "Genre", "Overview", "Status", 1000000, 2000000, "Country", "Language", "Original Title"), # Incorrect type for release_date
                            ("A title", date.today(), "Genre", 5.5, "Status", 1000000, 2000000, "Country", "Language", "Original Title"), # Incorrect type for overview
                        ])
def test_create_movie_rejects_bad_type(title, release_date, genre, overview, status, budget, revenue, country, language, orig_title):
    with pytest.raises(TypeError):
        create_movie(title, release_date, genre, overview, status, budget, revenue, country, language, orig_title)


def test_create_movie_returns_correctly(mock_connection):
    _, mock_cur = mock_connection
    mock_cur.fetchone.side_effect = [
                                        {'genre_id': 1},
                                        {'status_id': 1}, 
                                        {'country_id': 1}, 
                                        {'language_id': 1},
                                        {'movie_id': 1}
                                    ]
    movie = create_movie(title = "Inception",
    release_date = date(2010, 7, 16),
    genre = "Science Fiction",
    overview = "A mind-bending thriller where dream invasion is possible.",
    status = "Released",
    budget = 160000000,
    revenue = 829895144,
    country = "USA",
    language = "English",
    orig_title = "Inception")
    assert movie == {
        "title": "Inception",
        "release_date": date(2010, 7, 16),
        "genre": "Science Fiction",
        "overview": "A mind-bending thriller where dream invasion is possible.",
        "status": "Released",
        "budget": 160000000,
        "revenue": 829895144,
        "country": "USA",
        "language": "English",
        "orig_title": "Inception",
        "movie_id": 1
    }
