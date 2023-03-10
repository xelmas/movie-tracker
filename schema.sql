CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);
CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title TEXT UNIQUE,
    year INTEGER,
    media INTEGER DEFAULT 0
);
CREATE TABLE series(
    id SERIAL PRIMARY KEY,
    title TEXT UNIQUE
);
CREATE TABLE seasons(
    id SERIAL PRIMARY KEY,
    year INTEGER,
    serie_id INTEGER REFERENCES series,
    media INTEGER DEFAULT 1
);
CREATE TABLE ratings(
    id SERIAL PRIMARY KEY,
    rating INTEGER
);
CREATE TABLE movie_ratings (
    id SERIAL PRIMARY KEY,
    rating_id INTEGER REFERENCES ratings,
    user_id INTEGER REFERENCES users,
    movie_id INTEGER REFERENCES movies
);
CREATE TABLE season_ratings (
    id SERIAL PRIMARY KEY,
    rating_id INTEGER REFERENCES ratings,
    user_id INTEGER REFERENCES users,
    season_id INTEGER REFERENCES seasons
);
CREATE TABLE movies_watchlist(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    movie_id INTEGER REFERENCES movies,
    status INTEGER DEFAULT 0
);
CREATE TABLE series_watchlist(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    season_id INTEGER REFERENCES seasons,
    status INTEGER DEFAULT 0
);

