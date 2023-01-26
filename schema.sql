CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);
CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title TEXT,
    year INTEGER
);
CREATE TABLE series(
    id SERIAL PRIMARY KEY,
    title TEXT
);
CREATE TABLE seasons(
    id SERIAL PRIMARY KEY,
    year INTEGER,
    serie_id INTEGER REFERENCES series
);
CREATE TABLE ratings(
    id SERIAL PRIMARY KEY,
    rating INTEGER
);
CREATE TABLE movie_ratings (
    id SERIAL PRIMARY KEY,
    rating_id INTEGER REFERENCES ratings,
    user_id INTEGER REFERENCES users,
    movie_id INTEGER REFERENCES movies,
);
CREATE TABLE season_ratings (
    id SERIAL PRIMARY KEY,
    rating_id INTEGER REFERENCES ratings,
    user_id INTEGER REFERENCES users,
    season_id INTEGER REFERENCES seasons
);
CREATE TABLE watchlist(
    id SERIAL PRIMARY KEY,
    user_id REFERENCES users,
    season_id REFERENCES seasons,
    movie_id REFERENCES movies,
    status INTEGER
);
