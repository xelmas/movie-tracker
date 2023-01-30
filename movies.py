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