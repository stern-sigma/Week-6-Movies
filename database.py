#pylint: disable=unused-variable
from typing import Any
import psycopg2
import psycopg2.extras
from psycopg2 import sql
from psycopg2.extensions import connection, cursor
from datetime import date
from rich.progress import Progress, TextColumn, BarColumn, MofNCompleteColumn
from os import environ
from dotenv import load_dotenv

load_dotenv()

def __connection(func):
    def inner(*args, **kwargs):
        conn = psycopg2.connect(
            user = environ["DATABASE_USERNAME"],
            password = environ["DATABASE_PASSWORD"],
            host = environ["DATABASE_IP"],
            port = environ["DATABASE_PORT"],
            database = environ["DATABASE_NAME"]
        )
        curr = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        kwargs['conn'] = conn
        kwargs['curr'] = curr
        try:
            return func(*args, **kwargs)
        finally:
            curr.close()
            conn.close()
    return inner


@__connection
def get_movies(search: str = '', sort_by: str = '', sort_order: str = 'ASC',
               **kwargs) -> list[dict]:
    curr = kwargs.get('curr')
    if search:
        search = f"%{search}%"
    if not (search or sort_by):
        print(sort_order, sort_by)
        curr.execute('''SELECT * FROM movie_info;''')
    elif search and not sort_by:
        curr.execute('''SELECT *
FROM movie_info
WHERE title ILIKE %s;''',
(search,))
    else:
        print(sort_by, sort_order)
        match sort_by:
            case 'movie_id':
                sql_sort_by = 'movie_id'
            case 'title':
                sql_sort_by = 'title'
            case 'score':
                sql_sort_by = 'score'
            case 'budget':
                sql_sort_by = 'budget'
            case 'revenue':
                sql_sort_by = 'revenue'
            case _:
                raise ValueError('sort_by value not recognized')
        match sort_order:
            case 'ASC':
                sql_sort_order = 'ASC'
            case 'DESC':
                sort_order = 'DESC'
            case _:
                raise ValueError('sort_order value not recognized')
        if search:
            q = 'SELECT * FROM movie_info WHERE title LIKE %s ORDER BY {} {};'
        else:
            q = 'SELECT * FROM movie_info ORDER BY {} {};'
        q = sql.SQL(q)
        q = q.format(sql.Identifier(sql_sort_by), sql.SQL(sql_sort_order))
        if search:
            curr.execute(q, (search,))
        else:
            curr.execute(q)
    movies = curr.fetchall()
    progress = Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    MofNCompleteColumn(),
    transient=True
)
    with progress:
        tracker = progress.add_task("Loading genres...", total=len(movies))
        for movie in movies:
            curr.execute('''SELECT genre_name
FROM genre_assignments 
JOIN genres 
    ON (genre_assignments.genre_id=genres.genre_id) 
WHERE movie_id=%s;''',
(movie['movie_id'],))
            genres = curr.fetchall()
            movie['genres'] = [genre['genre_name'] for genre in genres]
            progress.update(tracker, advance=1)
    return movies


@__connection
def get_genre_id(genre_name: str, **kwargs):
    curr = kwargs.get('curr')
    curr.execute('SELECT genre_id FROM genres WHERE genre_name=%s;', (genre_name,))
    genre_id = curr.fetchone()
    if not genre_id:
        raise ValueError('Genre not recognized')
    return genre_id['genre_id']


@__connection
def get_status_id(status_name: str, **kwargs):
    curr = kwargs.get('curr')
    curr.execute('SELECT status_id FROM statuses WHERE status_name=%s;', (status_name,))
    status_id = curr.fetchone()
    if not status_id:
        raise ValueError('Status not recognized')
    return status_id['status_id']


@__connection
def get_language_id(language_name: str, **kwargs):
    curr = kwargs.get('curr')
    curr.execute('SELECT language_id FROM languages WHERE language_name=%s;', (language_name,))
    language_id = curr.fetchone()
    if not language_id:
        raise ValueError('Language not recognized')
    return language_id['language_id']


@__connection
def get_country_id(country_name: str, **kwargs):
    curr = kwargs.get('curr')
    curr.execute('SELECT country_id FROM countries WHERE country_name=%s;', (country_name,))
    country_id = curr.fetchone()
    if not country_id:
        raise ValueError('Country not recognized')
    return country_id['country_id']


@__connection
def get_movie_by_id(movie_id: int, **kwargs) -> dict[str, Any]:
    curr = kwargs.get('curr')
    if not isinstance(movie_id, int) or isinstance(movie_id, bool):
        raise TypeError("'movie_id' must be of type int")
    curr.execute('''SELECT *
FROM movies
JOIN statuses ON (movies.status_id=statuses.status_id)
JOIN languages ON (movies.language_id=languages.language_id)
JOIN countries ON (movies.country_id=countries.country_id)
JOIN genre_assignments ON (movies.movie_id=genre_assignments.movie_id)
JOIN genres ON (genre_assignments.genre_id=genres.genre_id)
WHERE movies.movie_id=%s;''',
(movie_id,))
    movie = curr.fetchone()
    if not movie:
        raise ValueError('No movie with that id was found')
    return movie


@__connection
def create_movie(title: str, release_date: date, genre: str, overview: str,
                status: str, budget: int, revenue: int, country: str, language: str,
                orig_title: str, **kwargs) -> dict:
    if not isinstance(title, str):
        raise TypeError('title must be of type str')
    if not isinstance(release_date, date):
        raise TypeError('release_date must be of type date')
    if not isinstance(genre, str):
        raise TypeError('genre must be of type str')
    if not isinstance(overview, str):
        raise TypeError('overview must be of type str')
    if not isinstance(status, str):
        raise TypeError('status must be of type str')
    if not isinstance(budget, int):
        raise TypeError('budget must be of type int')
    if not isinstance(revenue, int):
        raise TypeError('revenue must be of type int')
    if not isinstance(country, str):
        raise TypeError('country must be of type str')
    if not isinstance(language, str):
        raise TypeError('language must be of type str')
    if not isinstance(orig_title, str):
        raise TypeError('orig_title must be of type str')
    genre_id = get_genre_id(genre)
    status_id = get_status_id(status)
    country_id = get_country_id(country)
    language_id = get_language_id(language)
    curr = kwargs.get('curr')
    conn = kwargs.get('conn')
    curr.execute('''
INSERT INTO movies
(title, release_date, overview, status_id, budget, revenue, country_id, language_id, orig_title)
VALUES
(%s, %s, %s, %s, %s, %s, %s, %s, %s);
''', (title, release_date, overview, status_id, budget, revenue, country_id,
     language_id, orig_title))
    conn.commit()
    curr.execute("SELECT pg_get_serial_sequence('movies', 'movie_id');")
    movie_id = curr.fetchone()['movie_id']
    curr.execute('INSERT INTO genre_assignments (movie_id, genre_id) VALUES (%s, %s);',
                  (movie_id, genre_id))
    conn.commit()
    return {
        'movie_id': movie_id,
        'title': title,
        'genre': genre,
        'release_date': release_date,
        'overview': overview,
        'status': status,
        'budget': budget,
        'revenue': revenue,
        'country': country,
        'language': language,
        'orig_title': orig_title
    }


@__connection
def delete_movie(movie_id: int, **kwargs) -> bool:
    curr = kwargs.get('curr')
    conn = kwargs.get('conn')
    if not isinstance(movie_id, int) or isinstance(movie_id, bool):
        raise TypeError('movie_id must be of type int')
    curr.execute('DELETE FROM movies WHERE movie_id=%s RETURNING count', (movie_id,))
    conn.commit()
    return curr.fetchone()['count'] > 0


@__connection
def get_movies_by_genre(genre_id: int, **kwargs) -> list[dict[str, Any]]:
    if not isinstance(genre_id, int) or isinstance(genre_id, bool):
        raise TypeError('genre_id must be of type int')
    curr = kwargs.get('curr')
    curr.execute('''
SELECT * FROM genre_assignments
JOIN genres ON (genre_assignment.genre_id=genres.genre_id)
JOIN movies ON (genre_assignment.movie_id=movies.movie_id)
JOIN statuses ON (statuses.status_id=movies.status_id)
JOIN languages ON (languages.language_id=movies.language_id)
JOIN countries ON (countries.country_id=movies.country_id)
WHERE genre_id=%s
''', (genre_id,))
    return curr.fetchall()


@__connection
def get_movie_by_country(country_code: str, sort_by: str = None, sort_order: str = None,
                         **kwargs) -> list[dict]:
    curr = kwargs.get('curr')
    if not sort_by:
        curr.execute('''
SELECT * FROM movie_info
WHERE country_name=%s;
''', (country_code,))
    else:
        sql_sort_by = ''
        match sort_by:
            case 'movie_id':
                sql_sort_by = 'movie_id'
            case 'title':
                sql_sort_by = 'title'
            case 'score':
                sql_sort_by = 'score'
            case 'budget':
                sql_sort_by = 'budget'
            case 'revenue':
                sql_sort_by = 'revenue'
            case _:
                raise ValueError('sort_by value not recognized')
        sql_sort_order = 'DESC'
        if sort_order == 'ASC':
            sql_sort_order = 'ASC'
        q = 'SELECT * FROM movie_info WHERE country_name=%s ORDER BY {} {}'
        q = sql.SQL(q)
        q.format(sql.Identifier(sql_sort_by), sql.SQL(sql_sort_order))
        curr.execute(q, (country_code,))

    movies = curr.fetchall()
    for movie in movies:
        curr.execute('''SELECT genre_name 
                     FROM genre_assignments 
                     JOIN genres 
                        ON (genre_assignment.genre_id=genres.genre_id) 
                     WHERE movie_id=%s;''',
                      (movie['movie_id']))
        genres = curr.fetchall()
        movie['genres'] = [genre['genre_name'] for genre in genres]
    return movies


@__connection
def create_review(movie_id: int, review_text: str) -> None:
    ...


@__connection
def read_reviews(movie_id: int) -> list[int]:
    ...


@__connection
def count_reviews(movie_id: int) -> int:
    ...


@__connection
def update_review(review_id: int) -> None:
    ...


@__connection
def delete_review(review_id: int) -> None:
    ...

