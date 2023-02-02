from db import db

def create_rating(rating):
    sql = "INSERT INTO ratings (rating) VALUES (:rating) RETURNING id"
    result = db.session.execute(sql, {"rating":rating})
    rating_id = result.fetchone()[0]
    return rating_id


def rate(user_id, media_id, rating, media):

    if not exists(user_id, media_id, media):
        rating_id = create_rating(rating)

        if media == 0:
            sql = "INSERT INTO movie_ratings (rating_id, user_id, movie_id) VALUES (:rating_id, :user_id, :media_id)"
            db.session.execute(sql, {"rating_id":rating_id, "user_id":user_id, "media_id":media_id})
            db.session.commit()
            return True
        if media == 1:
            sql = "INSERT INTO season_ratings (rating_id, user_id, season_id) VALUES (:rating_id, :user_id, :media_id)"
            db.session.execute(sql, {"rating_id":rating_id, "user_id":user_id, "media_id":media_id})
            db.session.commit()
            return True
    
    elif exists:
        rating_id = get_rating_id(user_id, media_id, media)
        if update_rating(rating_id, rating):
            return True

    return False

def get_movie_ratings(user_id):

    sql = "SELECT rating, rating_id, movie_id FROM ratings JOIN movie_ratings ON ratings.id = movie_ratings.rating_id WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    ratings = result.fetchall()
    return ratings

def get_season_ratings(user_id):
    sql = "SELECT rating, rating_id, season_id FROM ratings JOIN season_ratings ON ratings.id = season_ratings.rating_id WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    ratings = result.fetchall()
    return ratings

def update_rating(rating_id, new_rating):
    sql = "UPDATE ratings SET rating = :new_rating WHERE ratings.id =:rating_id"
    db.session.execute(sql, {"new_rating":new_rating, "rating_id":rating_id})
    db.session.commit()
    return True

def exists(user_id, media_id, media):

    if media == 0:
        sql = "SELECT EXISTS (SELECT 1 FROM movie_ratings WHERE movie_id= :media_id AND user_id=:user_id)"
        exists = db.session.execute(sql, {"media_id":media_id, "user_id":user_id})
        exists = exists.fetchone()[0]
    
    if media == 1:
        sql = "SELECT EXISTS (SELECT 1 FROM season_ratings WHERE season_id= :media_id AND user_id=:user_id)"
        exists = db.session.execute(sql, {"media_id":media_id, "user_id":user_id})
        exists = exists.fetchone()[0]
    
    return exists

def get_rating_id(user_id, media_id, media):
    
    if media == 0:
        sql = "SELECT ratings.id FROM ratings JOIN movie_ratings ON movie_ratings.rating_id = ratings.id WHERE movie_ratings.movie_id=:media_id AND user_id=:user_id"
        result = db.session.execute(sql, {"user_id":user_id,"media_id":media_id})
        rating_id = result.fetchone()[0]
        return rating_id

    if media == 1:
        sql = "SELECT ratings.id FROM ratings JOIN season_ratings ON season_ratings.rating_id = ratings.id WHERE season_ratings.season_id=:media_id AND user_id=:user_id"
        result = db.session.execute(sql, {"user_id":user_id,"media_id":media_id})
        rating_id = result.fetchone()[0]
        return rating_id
