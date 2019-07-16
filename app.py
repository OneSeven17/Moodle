import os

import waitress
from flask import Flask, render_template, redirect, url_for, request
from werkzeug.utils import secure_filename

import db


def start():
    DATABASE_URL = 'db.sqlite'
    UPLOAD_FOLDER = '/'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'])

    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    @app.route('/')
    def index():
        movies = db.get_movies(DATABASE_URL)
        return render_template('index.html', movies=movies)

    @app.route('/search', methods=['POST'])
    def movie_search():
        search = request.form.get("search")
        results = db.search_movies(DATABASE_URL, search)
        return render_template('movie-search.html', movies=results, search=search)

    @app.route('/<id>', methods=['GET', 'POST'])
    def movie_details(id):
        movie = db.search_movie_by_id(DATABASE_URL, id)
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

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    @app.route('/new/add', methods=['POST'])
    def movie_add():
        name = request.form['name']
        category = request.form['category']
        genre = request.form['genre']
        tags = request.form['tags']
        poster = request.form['poster']
        movie = db.add_movie(DATABASE_URL, name, category, genre, tags, poster)
        # if request.method == 'POST':
        #     file = request.files['file']
        #     if file and allowed_file(file.filename):
        #         filename = secure_filename(file.filename)
        #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #         return redirect(url_for('movie_details',
        #                                 id=movie, filename=filename))
        return redirect(url_for('movie_details', id=movie))

    @app.route('/<id>/remove', methods=['POST'])
    def movie_remove(id):
        db.remove_movie_by_id(DATABASE_URL, id)
        movies = db.get_movies(DATABASE_URL)
        return render_template('index.html', movies=movies)

    @app.route('/search', methods=['POST'])
    def movies_search_by_tags():
        search = request.form.get("action")
        results = db.search_movies_by_tags(DATABASE_URL, search)
        return render_template('movie-search.html', movies=results, search=search)


    # @app.route('/upload')
    # def upload_file():
    #     return render_template('movie-add.html')
    #
    # @app.route('/uploader', methods=['GET', 'POST'])
    # def upload_file():
    #     if request.method == 'POST':
    #         f = request.files['file']
    #         f.save(secure_filename(f.filename))
    #         return 'file uploaded successfully'

    print(os.getenv('APP_ENV'))
    print(os.getenv('PORT'))
    if os.getenv('APP_ENV') == 'PROD' and os.getenv('PORT'):
        waitress.serve(app, port=os.getenv('PORT'))
    else:
        app.run(port=9876, debug=True)


if __name__ == '__main__':
    start()
