from db import db

def search_movie(query):
    sql = "SELECT title, year FROM movies WHERE title LIKE :query"
    result = db.session.execute(sql, {"query": "%"+query+"%"})
    results = result.fetchall()
    return results

def add_movie(title, year):
    try:
        sql = "INSERT INTO movies (title, year) VALUES (:title, :year)"
        db.session.execute(sql, {"title":title, "year":year})
        db.session.commit()
    except:
        return False
    return True

def add_watchlist(user_id, movie_id):

    sql = "SELECT EXISTS (SELECT 1 FROM movies_watchlist WHERE movie_id = :movie_id)"
    exists = db.session.execute(sql, {"movie_id":movie_id})
    exists = exists.fetchone()[0]

    if not exists:
        sql = "INSERT INTO movies_watchlist (user_id, movie_id) VALUES (:user_id, :movie_id)"
        db.session.execute(sql, {"user_id":user_id, "movie_id":movie_id})
        db.session.commit()
        return True
    return False

def delete_watchlist(user_id, movie_id):

    try:
        sql = "DELETE FROM movies_watchlist WHERE user_id=:user_id AND movie_id=:movie_id"
        db.session.execute(sql, {"user_id":user_id, "movie_id":movie_id})
        db.session.commit()
    except:
        return False
    return True

def get_movie_id(title):
    sql = "SELECT id FROM movies WHERE title = :title"
    result = db.session.execute(sql, {"title":title})
    movie_id = result.fetchone()[0]
    return movie_id

def movie_exists(title):
    sql = "SELECT EXISTS (SELECT 1 FROM movies WHERE title = :title)"
    exists = db.session.execute(sql, {"title":title})
    exists = exists.fetchone()[0]
    return exists

def mark_watched(movie_id, user_id):
    try:
        sql = "UPDATE movies_watchlist SET status = 1 WHERE movies_watchlist.movie_id=:movie_id AND movies_watchlist.user_id=:user_id"
        db.session.execute(sql, {"movie_id":movie_id, "user_id":user_id})
        db.session.commit()
    except:
        return False
    return True

def watched():
    sql = "SELECT movies.id, title, year, status, movies.media FROM movies_watchlist JOIN movies ON movies_watchlist.movie_id = movies.id WHERE status = 1"
    result = db.session.execute(sql)
    watched_movies = result.fetchall()
    return watched_movies

def watchlist():
    sql = "SELECT movies.id, title, year, status, movies.media FROM movies_watchlist JOIN movies ON movies_watchlist.movie_id = movies.id WHERE status = 0"
    result = db.session.execute(sql)
    movie_watchlist = result.fetchall()
    return movie_watchlist