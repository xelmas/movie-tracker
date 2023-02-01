from db import db


def search_series(query):
    sql = "SELECT title, year FROM seasons JOIN series ON seasons.serie_id = series.id WHERE title LIKE :query"
    result = db.session.execute(sql, {"query": "%"+query+"%"})
    results = result.fetchall()
    return results

def serie_exists(title):
    sql = "SELECT EXISTS (SELECT 1 FROM series WHERE title = :title)"
    exists = db.session.execute(sql, {"title":title})
    exists = exists.fetchone()[0]
    return exists

def season_exists(year, serie_id):
    sql = "SELECT EXISTS (SELECT 1 FROM seasons WHERE year = :year AND serie_id=:serie_id)"
    exists = db.session.execute(sql, {"year":year,"serie_id":serie_id})
    exists = exists.fetchone()[0]
    return exists

def add_serie(title, year):
    sql = "INSERT INTO series (title) VALUES (:title) RETURNING id"
    result = db.session.execute(sql, {"title":title})
    serie_id = result.fetchone()[0]
    add_season(year, serie_id)
    return True

def add_season(year, serie_id):
    sql = "INSERT into seasons (year, serie_id) VALUES (:year, :serie_id)"
    db.session.execute(sql, {"serie_id":serie_id, "year":year})
    db.session.commit()
    return True

def get_serie_id(title):
    sql = "SELECT id FROM series WHERE title= :title"
    result = db.session.execute(sql, {"title":title})
    serie_id = result.fetchone()[0]
    return serie_id

def get_season_id(year, serie_id):
    sql = "SELECT seasons.id FROM seasons JOIN series ON seasons.serie_id = series.id WHERE year =:year AND series.id = :serie_id"
    result = db.session.execute(sql, {"year":year, "serie_id":serie_id})
    season_id = result.fetchone()[0]
    return season_id

def add_watchlist(user_id, season_id):

    sql = "SELECT EXISTS (SELECT 1 FROM series_watchlist WHERE season_id = :season_id)"
    exists = db.session.execute(sql, {"season_id":season_id})
    exists = exists.fetchone()[0]

    if not exists:
        sql = "INSERT INTO series_watchlist (user_id, season_id) VALUES (:user_id, :season_id)"
        db.session.execute(sql, {"user_id":user_id, "season_id":season_id})
        db.session.commit()
        return True
    return False

def delete_watchlist(user_id, season_id):
    try:
        sql = "DELETE FROM series_watchlist WHERE user_id=:user_id AND season_id=:season_id"
        db.session.execute(sql, {"user_id":user_id, "season_id":season_id})
        db.session.commit()
    except:
        return False
    return True

def mark_watched(season_id, user_id):
    sql = "UPDATE series_watchlist SET status=1 WHERE series_watchlist.season_id=:season_id AND series_watchlist.user_id=:user_id"
    db.session.execute(sql, {"season_id":season_id, "user_id":user_id})
    db.session.commit()
