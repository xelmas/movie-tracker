from flask import render_template, request, redirect
from app import app
import users, movies, series, ratings

@app.route("/")
def index():
    user_id = users.user_id()
    movies_count = movies.count_watched(user_id)
    series_count = series.count_watched(user_id)
    avg_rating_movies = ratings.get_avg(user_id, 0)
    avg_rating_series = ratings.get_avg(user_id, 1)
    top5_movies = ratings.get_top5(0)
    top5_series = ratings.get_top5(1)
    
    return render_template("index.html", movies_count=movies_count, 
                                         series_count=series_count,
                                         avg_movies=avg_rating_movies,
                                         avg_series=avg_rating_series,
                                         top5_movies=top5_movies,
                                         top5_series=top5_series)

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
    return render_template("error.html", message="Wrong password or username")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/search", methods=["GET"])
def search():
    if users.is_user():
        return render_template("search.html")
    return render_template("error.html", message="Request not allowed")

@app.route("/add", methods = ["GET"])
def add():
    if users.is_user():
        return render_template("add.html")
    return render_template("error.html", message="Request not allowed")

@app.route("/watchlist", methods=["GET"])
def watchlist():
    if users.is_user():
        user_id = users.user_id()
        movie_watchlist = movies.watchlist(user_id)
        series_watchlist = series.watchlist(user_id)
        return render_template("watchlist.html", watchlist1=movie_watchlist
                                            , watchlist2=series_watchlist)
    return render_template("error.html", message="Request not allowed")

@app.route("/result", methods=["GET"])
def result():
    if users.is_user():
        query = request.args["query"]
        movie = movies.search_movie(query)

        if len(movie) > 0:
            return render_template("result.html", media=movie, keyword=query)
        if not movie:
            serie = series.search_series(query)
            if len(serie) > 0:
                return render_template("result.html", media=serie, keyword=query)
    
        return render_template("error.html", message="No results", keyword=query)
    return render_template("error.html", message="Request not allowed")
    
@app.route("/create_movie", methods=["POST"])
def create_movie():
    users.check_csrf()
    title = request.form["title"]
    year = request.form["year"]
    user_id = users.user_id()
    
    if movies.add_movie(title, year):
        if "options" in request.form:
            option = request.form["options"]
            movie_id = movies.get_movie_id(title)
            if option == "watched":
                if movies.mark_watched(movie_id, user_id):
                    return redirect("/watched")
            if option == "watchlist":
                if movies.add_watchlist(user_id, movie_id):
                    return redirect("/watchlist")
        else:
            return redirect("/")
    
    return render_template("error.html", message="Movie already in the database")

@app.route("/create_serie", methods=["POST"])
def create_serie():
    users.check_csrf()
    title = request.form["title"]
    year = request.form["year"]
    serie_exists = series.serie_exists(title)
    user_id = users.user_id()
    added = False

    if not serie_exists:
        series.add_serie(title, year)
        added = True
    if serie_exists:
        serie_id = series.get_serie_id(title)
        season_exists = series.season_exists(year, serie_id)
        if not season_exists:
            series.add_season(year, serie_id)
            added = True

    if added:
        if "options" in request.form:
            option = request.form["options"]
            serie_id = series.get_serie_id(title)
            season_id = series.get_season_id(year, serie_id)
            if option == "watched":
                if series.mark_watched(season_id, user_id):
                    return redirect("/watched")
            if option == "watchlist":
                if series.add_watchlist(user_id, season_id):
                    return redirect("/watchlist")
        else:
            return redirect("/")
    
    return render_template("error.html", message="Serie/season already in the database")

@app.route("/add_watchlist", methods=["POST"])
def add_watchlist():
    users.check_csrf()
    title = request.form["title"]
    year = request.form["year"]
    user_id = users.user_id()
    process = request.form["process"]
    media = int(request.form["media"])
    
    if media == 0:
        if movies.movie_exists(title):
            movie_id = movies.get_movie_id(title)

            if process == "Watchlist":
                if movies.add_watchlist(user_id, movie_id):
                    return redirect("/watchlist")
            else:
                if movies.mark_watched(movie_id, user_id):
                    return redirect("/watched")
                
    if media == 1:
        if series.serie_exists(title):
            serie_id = series.get_serie_id(title)
            season_id = series.get_season_id(year, serie_id)

            if process == "Watchlist":
                if series.add_watchlist(user_id, season_id):
                    return redirect("/watchlist")
            else:
                if series.mark_watched(season_id, user_id):
                    return redirect("/watched")
    return render_template("error.html", message="Move/serie already on the watchlist or watched list")

@app.route("/update_watchlist", methods=["GET","POST"])
def update_watchlist():
    users.check_csrf()
    user_id = users.user_id()
    media = int(request.form["media"])
    process = request.form["process"]
    if media == 0:
        movie_id = request.form["id"]
        if process == "Watched":
            movies.mark_watched(movie_id, user_id)
        else:
            movies.delete_watchlist(user_id, movie_id)
        return redirect("/watchlist")
    
    elif media == 1:
        serie_id = request.form["id"]
        if process == "Watched":
            series.mark_watched(serie_id, user_id)
        else:
            series.delete_watchlist(user_id, serie_id)
        return redirect("/watchlist")
        
    return render_template("error.html", message="Could not update the watchlist")

@app.route("/watched", methods=["GET"])
def watched():
    if users.user_id():
        user_id = users.user_id()
        try:
            watched_movies = movies.watched(user_id)
            watched_series = series.watched(user_id)
            movie_ratings = ratings.get_movie_ratings(user_id)
            season_ratings = ratings.get_season_ratings(user_id)
        except:
            return render_template("error.html", message="Watched lists unavailable")

        return render_template("watched.html", watchlist1=watched_movies
                                            , watchlist2=watched_series
                                            , ratings1=movie_ratings
                                            , ratings2=season_ratings)
    return render_template("error.html", message="Request not allowed")

@app.route("/rate", methods=["POST"])
def rate():
    users.check_csrf()
    rating = int(request.form["rating"])
    media_id = request.form["id"]
    media = int(request.form["media"])
    user_id = users.user_id()

    if ratings.rate(user_id, media_id, rating, media):
        return redirect("/watched")

    return render_template("error.html", message="Something went wrong with rating")

@app.route("/media/<media>/<title>/<year>", methods=["GET"])
def media(title, year, media):
    if users.is_user():
        if media == "movie":
            movie_id = movies.get_movie_id(title)
            avg_rating = ratings.get_avg_rating(0, movie_id)
            watchers = movies.count_watchers(title)
            return render_template("/media.html", title=title
                                                , year=year
                                                , movie_id=movie_id
                                                , avg_rating=avg_rating
                                                , watchers=watchers
                                                , media=0)
        if media == "serie":
            serie_id = series.get_serie_id(title)
            season_id = series.get_season_id(year, serie_id)
            season_num = series.get_season_number(title, serie_id, year)
            avg_rating = ratings.get_avg_rating(1, season_id)
            watchers = series.count_watchers(season_id)
            return render_template("/media.html", title=title
                                                , year=year
                                                , season_id=season_id
                                                , season_num=season_num
                                                , avg_rating=avg_rating
                                                , watchers=watchers
                                                , media=1)

    return render_template("error.html", message="Request not allowed")

@app.route("/serie_data/<title>", methods=["GET"])
def data(title):
    if users.is_user():
        serie_id = series.get_serie_id(title)
        seasons_data = series.get_all_seasons(serie_id)
        return render_template("/serie_data.html", seasons_data=seasons_data
                                                 , title=title)
    return render_template("error.html", message="Request not allowed")

