from flask import session, abort, request
from werkzeug.security import check_password_hash, generate_password_hash
import os
from db import db


def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def login(username, password):
    sql = "SELECT id,password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user_name"] = username
            session["csrf_token"] = os.urandom(16).hex()
            return True
    return False

def logout():
    del session["user_id"]
    del session["user_name"]

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
        
def user_id():
    return session.get("user_id",0)

def is_user():
    id = user_id()
    if id == 0:
        return False
    return True