from db import db

def create_rating(rating):
    sql = "INSERT INTO ratings (rating) VALUES (:rating) RETURNING id"
    result = db.session.execute(sql, {"rating":rating})
    rating_id = result.fetchone()[0]
    return rating_id


def rate(user_id, media_id, rating, media):

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
    return False