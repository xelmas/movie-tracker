from app import app
from db import db
import users, movies, series, ratings
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

@app.route("/add", methods = ["GET"])
def add():
    return render_template("add.html")

@app.route("/watchlist", methods=["GET"])
def watchlist():
    user_id = users.user_id()
    movie_watchlist = movies.watchlist(user_id)
    series_watchlist = series.watchlist(user_id)
    return render_template("watchlist.html", watchlist1=movie_watchlist, watchlist2=series_watchlist)

@app.route("/result", methods=["GET"])
def result():
    query = request.args["query"]
    movie = movies.search_movie(query)

    if not movie:
        serie = series.search_series(query)
        return render_template("result.html", media=serie, keyword=query)

    return render_template("result.html", media=movie, keyword=query)

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
        movies.add_watchlist(user_id, movie_id)
        return redirect("/search")

    if series.serie_exists(title):
        serie_id = series.get_serie_id(title)
        season_id = series.get_season_id(year, serie_id)
        series.add_watchlist(user_id, season_id)
        return redirect("/search")

    return render_template("error.html", message="Move/serie already on the watchlist or watched")

@app.route("/update_watchlist", methods=["GET","POST"])
def update_watchlist():

    user_id = users.user_id()
    delete = request.form.getlist("delete")
    watched = request.form.getlist("watched")
    
    if len(delete) > 0:
        for item in delete:
            item = item.split("-")
            id = item[0]
            media = int(item[1])
            if media == 0:
                movies.delete_watchlist(user_id, id)
            else:
                series.delete_watchlist(user_id, id)
                        
    if len(watched) > 0:
        for item in watched:
            item = item.split("-")
            id = item[0]
            media = int(item[1])
            if media == 0:
                movies.mark_watched(id, user_id)
            else:
                series.mark_watched(id, user_id)
                          
    return redirect("/watchlist")
    

@app.route("/watched", methods=["GET"])
def watched():
    user_id = users.user_id()
    try:
        watched_movies = movies.watched(user_id)
        watched_series = series.watched(user_id)
        movie_ratings = ratings.get_movie_ratings(user_id)
        season_ratings = ratings.get_season_ratings(user_id)
    except:
        return render_template("error.html", message="Watched lists unavailable")

    return render_template("watched.html", watchlist1=watched_movies, watchlist2=watched_series, ratings1=movie_ratings, ratings2=season_ratings)

@app.route("/rate", methods=["POST"])
def rate():

    rating = int(request.form["rating"])
    id = request.form["id"]
    media = int(request.form["media"])
    user_id = users.user_id()

    if ratings.rate(user_id, id, rating, media):
        return redirect("/watched")

    return render_template("error.html", message="Something went wrong with rating")