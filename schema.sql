-- This file contains all of the SQL commands to create the database, tables and relationships for the Movies Database
DROP VIEW IF EXISTS movie_info;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS cast_assignments;
DROP TABLE IF EXISTS genre_assignments;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS statuses;
DROP TABLE IF EXISTS languages;
DROP TABLE IF EXISTS countries;
drop table if exists genres;
DROP TABLE IF EXISTS people;


CREATE TABLE genres (
    genre_id BIGSERIAL PRIMARY KEY,
    genre_name TEXT NOT NULL
);
CREATE TABLE statuses (
    status_id BIGSERIAL PRIMARY KEY,
    status_name TEXT NOT NULL
);
CREATE TABLE languages (
    language_id BIGSERIAL PRIMARY KEY,
    language_name TEXT NOT NULL
);
CREATE TABLE countries (
    country_id BIGSERIAL PRIMARY KEY,
    country_name TEXT NOT NULL
);
CREATE TABLE people (
    person_id TEXT PRIMARY KEY,
    person_name TEXT NOT NULL
);
CREATE TABLE movies (
    movie_id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    date DATE NOT NULL,
    score NUMERIC NOT NULL,
    overview TEXT NOT NULL,
    original_title TEXT NOT NULL,
    status_id BIGINT NOT NULL 
        REFERENCES statuses(status_id),
    language_id BIGINT NOT NULL 
        REFERENCES languages(language_id),
    budget NUMERIC NOT NULL,
    revenue NUMERIC NOT NULL,
    country_id INT NOT NULL 
        REFERENCES countries(country_id)
);
CREATE TABLE cast_assignments(
    id BIGSERIAL PRIMARY KEY,
    movie_id BIGINT NOT NULL 
        REFERENCES movies(movie_id),
    person_id TEXT NOT NULL 
        REFERENCES people(person_id)
);
CREATE TABLE genre_assignments (
    id BIGSERIAL PRIMARY KEY,
    movie_id BIGINT NOT NULL 
        REFERENCES movies(movie_id),
    genre_id INT NOT NULL 
        REFERENCES genres(genre_id)
);
CREATE TABLE reviews (
    review_id BIGSERIAL PRIMARY KEY,
    movie_id BIGINT NOT NULL 
        REFERENCES movies(movie_id),
    review TEXT NOT NULL
);

CREATE VIEW movie_info AS
    SELECT *
    FROM movies
    JOIN statuses USING (status_id)
    JOIN languages USING (language_id)
    JOIN countries USING (country_id);

INSERT INTO languages (language_name) VALUES
('English'),
('Spanish'),
('Norwegian'),
('Japanese'),
('Korean'),
('Russian'),
('Cantonese'),
('Ukrainian'),
('Italian'),
('German'),
('French'),
('Finnish'),
('Icelandic'),
('Indonesian'),
('Dutch'),
('Portuguese'),
('Telugu'),
('Polish'),
('Danish'),
('Turkish'),
('Chinese'),
('Thai'),
('Romanian'),
('Tagalog'),
('Macedonian'),
('Swedish'),
('Tamil'),
('Vietnamese'),
('Hindi'),
('Arabic'),
('Serbian'),
('No Language'),
('Galician'),
('Greek'),
('Hungarian'),
('Malayalam'),
('Marathi'),
('Oriya'),
('Bengali'),
('Persian'),
('Latvian'),
('Basque'),
('Malay'),
('Central Khmer'),
('Irish'),
('Czech'),
('Gujarati'),
('Kannada'),
('Serbo-Croatian'),
('Latin'),
('Dzongkha'),
('Slovak');

INSERT INTO countries (country_name) VALUES
('AU'),
('US'),
('MX'),
('GB'),
('CL'),
('NO'),
('ES'),
('AR'),
('KR'),
('HK'),
('UA'),
('IT'),
('RU'),
('CO'),
('DE'),
('JP'),
('FR'),
('FI'),
('IS'),
('ID'),
('BR'),
('BE'),
('DK'),
('TR'),
('TH'),
('PL'),
('GT'),
('CN'),
('CZ'),
('PH'),
('ZA'),
('CA'),
('NL'),
('TW'),
('PR'),
('IN'),
('IE'),
('SG'),
('PE'),
('CH'),
('SE'),
('IL'),
('DO'),
('VN'),
('GR'),
('SU'),
('HU'),
('BO'),
('SK'),
('UY'),
('BY'),
('AT'),
('PY'),
('MY'),
('MU'),
('LV'),
('XC'),
('PT'),
('KH'),
('IR');

INSERT INTO genres (genre_name) VALUES
('Fantasy'),
('Science Fiction'),
('Comedy'),
('Family'),
('Animation'),
('Romance'),
('Drama'),
('TV Movie'),
('War'),
('Mystery'),
('Music'),
('Horror'),
('History'),
('Adventure'),
('Documentary'),
('Action'),
('Western'),
('Thriller'),
('Crime');

INSERT INTO statuses (status_name) VALUES
('In Production'),
('Post Production'),
('Released');