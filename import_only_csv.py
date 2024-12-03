"""A script to import all of the movies in imdb_movies.csv into the database"""

import pandas as pd
from sqlalchemy import create_engine, text
import sqlalchemy

def re_init_db(conn: sqlalchemy.Connection):
    with open('schema.sql', 'r') as fp:
        commands = fp.read()
    command_list = commands.split(';')
    for command in command_list:
        if not command:
            continue
        sql_command = text(command)
        conn.execute(sql_command)

def import_movies_to_database(conn) -> None:
    l_df = pd.read_sql('SELECT * FROM languages', conn)
    languages = {x[1]['language_name']: x[1]['language_id'] for x in l_df.iterrows()}
    c_df = pd.read_sql('SELECT * FROM countries;', conn)
    countries = {x[1]['country_name']: x[1]['country_id'] for x in c_df.iterrows()}
    s_df = pd.read_sql('SELECT * FROM statuses', conn)
    statuses = {x[1]['status_name']: x[1]['status_id'] for x in s_df.iterrows()}
    movies = pd.read_csv('imdb_movies.csv', usecols=['names', 'date_x', 'score',
        'overview', 'score', 'overview', 'orig_title', 'status', 'orig_lang',
        'budget_x', 'revenue', 'country'])
    movies.columns = ['title', 'date', 'score', 'overview', 'original_title', 'status_id', 
        'language_id', 'budget', 'revenue', 'country_id']
    movies['language_id'] = movies['language_id'].apply(lambda x: languages[x.strip()])
    movies['country_id'] = movies['country_id'].apply(lambda x: countries[x])
    movies['status_id'] = movies['status_id'].apply(lambda x: statuses[x.strip()])
    movies.to_sql('movies', conn, if_exists='append', index=False)
    conn.commit()
    movie_id_table = pd.read_sql('SELECT title, movie_id FROM movies;', conn)
    movie_id_dict = {x[1]['title']: x[1]['movie_id'] for x in movie_id_table.iterrows()}
    genre_info = pd.read_sql('SELECT * FROM genres;', conn)
    genre_dict = {x[1]['genre_name']: x[1]['genre_id'] for x in genre_info.iterrows()}
    movie_genres = pd.read_csv('imdb_movies.csv', usecols=['names', 'genre'])
    movie_genres.columns = ['title', 'genre']
    movie_genres['title'] = movie_genres['title'].apply(lambda x: movie_id_dict[x])
    movies_genres_info = []
    for movie in movie_genres:
        if not isinstance(movie, dict):
            continue
        movies_genres_info.extend({movie['title']: genre_dict[x] for x in movie['genre'].split()})
    genre_df = pd.DataFrame(movies_genres_info)
    genre_df.to_sql('genres', conn, if_exists='append')
    conn.commit()
    return movie_id_dict


def main():
    engine = create_engine("postgresql://stern:@localhost:5432/movies")
    conn = engine.connect()
    re_init_db(conn)
    import_movies_to_database(conn)
    conn.close()
    engine.dispose()


if __name__ == "__main__":
    main()
