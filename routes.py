from app import app
from db import db
import users, movies, series
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

@app.route("/add_movie", methods=["GET"])
def Add_movie():
    return render_template("add_movie.html")

@app.route("/add_serie", methods=["GET"])
def Add_serie():
    return render_template("add_serie.html")

# @app.route("/result", methods=["GET"])
# def result():
#     query = request.args["query"]
#     sql = "SELECT title, year FROM movies WHERE title LIKE :query"
#     result = db.session.execute(sql, {"query": "%"+query+"%"})
#     media = result.fetchall()
#     return render_template("result.html", media=media)

@app.route("/result", methods=["GET"])
def result():
    query = request.args["query"]
    media_movies = movies.search_movie(query)

    if not media_movies:
        series_media = series.search_series(query)
        return render_template("result.html", media=series_media)

    return render_template("result.html", media=media_movies)

@app.route("/create_movie", methods=["POST"])
def create_movie():
    title = request.form["title"]
    year = request.form["year"]
    if movies.add_movie(title, year):
        return redirect("/")
    return render_template("error.html", message="Movie already in the database")
    

@app.route("/create_serie", methods=["POST"])
def create_serie():
    title = request.form["title"]
    year = request.form["year"]
    serie_exists = series.serie_exists(title)
    if not serie_exists:
        series.add_serie(title, year)
        return redirect("/")
    elif serie_exists:
        serie_id = series.get_serie_id(title)
        season_exists = series.season_exists(year, serie_id)
        if not season_exists:
            series.add_season(year, serie_id)
            return redirect("/")
        
    return render_template("error.html", message="Serie/season already in the database")
    