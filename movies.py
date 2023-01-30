from db import db
from flask import request

def search_movie(query):
    sql = "SELECT title, year FROM movies WHERE title LIKE :query"
    result = db.session.execute(sql, {"query": "%"+query+"%"})
    results = result.fetchall()
    return results
