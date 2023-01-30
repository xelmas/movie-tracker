from app import app
from db import db
import users
from flask import render_template, request, redirect


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Passwords are not equal")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Registering not successful")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Wrong password or username")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/search", methods=["GET"])
def search():
    return render_template("search.html")

@app.route("/result", methods=["GET"])
def result():
    query = request.args["query"]
    sql = "SELECT title, year FROM movies WHERE title LIKE :query"
    result = db.session.execute(sql, {"query": "%"+query+"%"})
    media = result.fetchall()
    return render_template("result.html", media=media)