import uuid

from flask import Flask, render_template, redirect, url_for, request

import db

DATABASE_URL = 'db.sqlite'

app = Flask(__name__)


@app.route('/')
def index():

    movies = db.get_movies(DATABASE_URL)
    return render_template('index.html', movies=movies)

@app.route('/search', methods=['POST'])
def movie_search():
    print(request.form.get("search"))
    search = request.form.get("search")
    results = db.search_movies(DATABASE_URL, search)
    return render_template('movie-search.html', movies=results, search=search)


@app.route('/<id>', methods=['GET', 'POST'])
def movie_details(id):
    movie = db.search_movie_by_id(DATABASE_URL, id)
    print(id)
    return render_template('movie-details.html', movie=movie)

@app.route('/<id>/edit', methods=['POST'])
def movie_edit(id):
    movie = db.search_movie_by_id(DATABASE_URL, id)
    return render_template('movie-edit.html', movie=movie)

@app.route('/<id>/save', methods=['POST'])
def movie_update(id):

    name = request.form['name']
    category = request.form['category']
    genre = request.form['genre']
    tags = request.form['tags']
    poster = request.form['poster']
    movie = db.update_movie(DATABASE_URL, id, name, category, genre, tags, poster)
    return redirect(url_for('movie_details', id=movie))

@app.route('/new', methods=['GET'])
def movie_new():

    return render_template('movie-add.html')

@app.route('/new/add', methods=['POST'])
def movie_add():

    name = request.form['name']
    category = request.form['category']
    genre = request.form['genre']
    tags = request.form['tags']
    poster = request.form['poster']
    movie = db.add_movie(DATABASE_URL, name, category, genre, tags, poster)
    # return render_template('movie-details.html', movie=movie)
    return redirect(url_for('movie_details', id=movie))

@app.route('/<id>/remove', methods=['POST'])
def movie_remove(id):
    db.remove_movie_by_id(DATABASE_URL, id)
    movies = db.get_movies(DATABASE_URL)
    return render_template('index.html', movies=movies)
    # return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
