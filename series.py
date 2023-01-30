from db import db
from flask import request

def search_series(query):
    sql = "SELECT title, year FROM seasons JOIN series ON seasons.serie_id = series.id WHERE title LIKE :query"
    result = db.session.execute(sql, {"query": "%"+query+"%"})
    results = result.fetchall()
    return results