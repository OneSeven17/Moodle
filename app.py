from flask import Flask, render_template, redirect, url_for, request

import db

DATABASE_URL = 'db.sqlite'

app = Flask(__name__)


@app.route('/')
def index():
    # 1.шаблон
    # 2. данные из БД
    movies = db.get_movies(DATABASE_URL)
    return render_template('index.html', movies=movies)

@app.route('/<id>', methods=['GET', 'POST'])
def movie_details(id):
    movie = db.search_movie_by_id(DATABASE_URL, id)
    return render_template('movie-details.html', movie=movie)

@app.route('/<id>/edit', methods=['POST'])
def movie_edit(id):
    movie = db.search_movie_by_id(DATABASE_URL, id)
    return render_template('movie-edit.html', movie=movie)

@app.route('/<id>/save', methods=['POST'])
def movie_save(id):
    name = request.form['name']
    category = request.form['category']
    genre = request.form['genre']
    tags = request.form['tags']
    poster = request.form['poster']
    db.remove_movie_by_id(DATABASE_URL, id)
    movie = db.add_movie(DATABASE_URL, id)

    return redirect(url_for('movie_details', id=movie['id']))


@app.route('/<id>/remove', methods=['POST'])
def movie_remove(id):
    db.remove_movie_by_id(DATABASE_URL, id)
    movies = db.get_movies(DATABASE_URL)
    return render_template('index.html', movies=movies)
    # return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
