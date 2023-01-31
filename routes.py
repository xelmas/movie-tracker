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


@app.route("/watchlist", methods=["GET"])
def watchlist():

    sql = "SELECT movies.id, title, year FROM movies_watchlist JOIN movies ON movies_watchlist.movie_id = movies.id"
    result = db.session.execute(sql)
    movie_watchlist = result.fetchall()

    sql = "SELECT t.id, title, year FROM (SELECT S.id, title, year FROM seasons AS S JOIN series ON S.serie_id=series.id) AS t JOIN series_watchlist ON t.id=series_watchlist.season_id"
    result = db.session.execute(sql)
    series_watchlist = result.fetchall()
    return render_template("watchlist.html", watchlist1=movie_watchlist, watchlist2=series_watchlist)

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

@app.route("/add_watchlist", methods=["POST"])
def add_watchlist():

    title = request.form["title"]
    year = request.form["year"]
    user_id = users.user_id()

    if movies.movie_exists(title):
        movie_id = movies.get_movie_id(title)
        if movies.add_watchlist(user_id, movie_id):
            return redirect("/search")

    if series.serie_exists(title):
        serie_id = series.get_serie_id(title)
        season_id = series.get_season_id(year, serie_id)
        if series.add_watchlist(user_id, season_id):
            return redirect("/search")

    return render_template("error.html", message="Move/serie already on the watchlist")

@app.route("/delete_watchlist", methods=["POST"])
def delete_watchlist():

    media = request.form["media"]
    id = request.form["id"]
    user_id = users.user_id()

    if media == "movie":
        movies.delete_watchlist(user_id, movie_id=id)
        return redirect("/watchlist")
    if media == "serie":
        series.delete_watchlist(user_id, season_id=id)
        return redirect("/watchlist")

    return render_template("error.html", message="Deleting item from the list was not successful")