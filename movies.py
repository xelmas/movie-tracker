from db import db
from flask import request

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
    sql = "INSERT INTO movies_watchlist (user_id, movie_id) VALUES (:user_id, :movie_id)"
    db.session.execute(sql, {"user_id":user_id, "movie_id":movie_id})
    db.session.commit()
    return True


def get_movie_id(title):
    sql = "SELECT id FROM movies WHERE title = :title"
    result = db.session.execute(sql, {"title":title})
    movie_id = result.fetchone()[0]
    return movie_id