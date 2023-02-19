from db import db

def create_rating(rating):

    sql = "INSERT INTO ratings (rating) VALUES (:rating) RETURNING id"
    result = db.session.execute(sql, {"rating":rating})
    rating_id = result.fetchone()[0]
    return rating_id

def rate(user_id, media_id, rating, media):

    exists = rating_exists(user_id, media_id, media)

    if not exists:
        rating_id = create_rating(rating)

        if media == 0:
            sql = """INSERT INTO movie_ratings (rating_id, user_id, movie_id)
                     VALUES (:rating_id, :user_id, :media_id)"""
            db.session.execute(sql, {"rating_id":rating_id, "user_id":user_id, "media_id":media_id})
            db.session.commit()
            return True
        if media == 1:
            sql = """INSERT INTO season_ratings (rating_id, user_id, season_id)
                     VALUES (:rating_id, :user_id, :media_id)"""
            db.session.execute(sql, {"rating_id":rating_id, "user_id":user_id, "media_id":media_id})
            db.session.commit()
            return True
    elif exists:
        rating_id = get_rating_id(user_id, media_id, media)
        update_rating(rating_id, rating)
        return True

    return False

def get_movie_ratings(user_id):

    sql = """SELECT rating, rating_id, movie_id FROM ratings JOIN movie_ratings
             ON ratings.id = movie_ratings.rating_id WHERE user_id=:user_id"""
    result = db.session.execute(sql, {"user_id":user_id})
    ratings = result.fetchall()
    return ratings

def get_season_ratings(user_id):

    sql = """SELECT rating, rating_id, season_id FROM ratings JOIN season_ratings
             ON ratings.id = season_ratings.rating_id WHERE user_id=:user_id"""
    result = db.session.execute(sql, {"user_id":user_id})
    ratings = result.fetchall()
    return ratings

def update_rating(rating_id, new_rating):

    sql = "UPDATE ratings SET rating = :new_rating WHERE ratings.id =:rating_id"
    db.session.execute(sql, {"new_rating":new_rating, "rating_id":rating_id})
    db.session.commit()

def rating_exists(user_id, media_id, media):

    if media == 0:
        sql = """SELECT EXISTS (SELECT 1 FROM movie_ratings
                 WHERE movie_id= :media_id AND user_id=:user_id)"""
        exists = db.session.execute(sql, {"media_id":media_id, "user_id":user_id})
        exists = exists.fetchone()[0]

    else:
        sql = """SELECT EXISTS (SELECT 1 FROM season_ratings
                 WHERE season_id= :media_id AND user_id=:user_id)"""
        exists = db.session.execute(sql, {"media_id":media_id, "user_id":user_id})
        exists = exists.fetchone()[0]

    return exists

def get_rating_id(user_id, media_id, media):

    if media == 0:
        sql = """SELECT ratings.id FROM ratings JOIN movie_ratings
                ON movie_ratings.rating_id = ratings.id
                WHERE movie_ratings.movie_id=:media_id AND user_id=:user_id"""
        result = db.session.execute(sql, {"user_id":user_id,"media_id":media_id})
        rating_id = result.fetchone()[0]

    else:
        sql = """SELECT ratings.id FROM ratings JOIN season_ratings
                ON season_ratings.rating_id = ratings.id
                WHERE season_ratings.season_id=:media_id AND user_id=:user_id"""
        result = db.session.execute(sql, {"user_id":user_id,"media_id":media_id})
        rating_id = result.fetchone()[0]

    return rating_id

def get_avg(user_id, media):
    rating_avg = 0
    if media == 0:
        sql = """SELECT AVG(rating):: numeric(10,2)
                 FROM ratings JOIN movie_ratings AS M ON M.rating_id=ratings.id
                 WHERE user_id=:user_id"""
        result = db.session.execute(sql, {"user_id":user_id})
        rating_avg = result.fetchone()[0]
    else:
        sql = """SELECT AVG(rating):: numeric(10,2)
                 FROM ratings JOIN season_ratings AS S ON S.rating_id=ratings.id
                 WHERE user_id=:user_id"""
        result = db.session.execute(sql, {"user_id":user_id})
        rating_avg = result.fetchone()[0]
    
    return rating_avg

def get_top5(media):

    if media == 0:

        sql = """SELECT title, year, top.avg
                 FROM 
                    (SELECT movie_id, AVG(rating):: numeric(10,2)
                    FROM ratings
                    JOIN movie_ratings AS mov
                    ON mov.rating_id=ratings.id
                    GROUP BY movie_id
                    ORDER BY avg DESC
                    LIMIT 5)
                    AS top
                 JOIN movies ON top.movie_id=movies.id ORDER BY top.avg DESC"""
        result = db.session.execute(sql)
        result_top5 = result.fetchall()
    
    else:
        sql = """SELECT season.title, season.year, top.avg
                 FROM 
                    (SELECT season_id, AVG(rating):: numeric(10,2)
                    FROM ratings
                    JOIN season_ratings AS s
                    ON s.rating_id=ratings.id
                    GROUP BY season_id
                    ORDER BY avg DESC
                    LIMIT 5)
                    AS top
                 JOIN
                    (SELECT s.id, title, year
                    FROM seasons AS s
                    JOIN series
                    ON s.serie_id=series.id)
                    AS season
                 ON top.season_id=season.id"""
        result = db.session.execute(sql)
        result_top5 = result.fetchall()

    return result_top5


