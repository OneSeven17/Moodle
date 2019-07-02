import sqlite3


def open_db(db_url):
    db = sqlite3.connect(db_url)
    db.row_factory = sqlite3.Row # если этого не указать, то все ответы будут возвращаться в виде tuple, а это плохо
    return db

def get_movies(db_url, page=1):
    db = open_db(db_url)
    limit = 5
    offset = limit * (page - 1)
    movies = db.cursor().execute(
        'SELECT id, name, category, genre, tags, poster, likes FROM movies LIMIT  :limit OFFSET  :offset',
    {'limit': limit, 'offset': offset}
    ).fetchall()
    db.close()
    return movies


def search_movies(db_url, name):
    pass


def add_movie(db_url, movie_id):
    db = open_db(db_url)
    db.cursor().execute(
        'INSERT INTO movies (id, name, category, genre, tags, poster) VALUES (:id, :name, :category, :genre, :tags, :poster)',
        {'id': movie_id},

    )
    db.commit()
    db.close()



def update_movie(db_url, movie):
    pass

def search_movie_by_id(db_url, movie_id):
    db = open_db(db_url)
    movie = db.cursor().execute(
        'SELECT id, name, category, genre, tags, poster, likes FROM movies WHERE id = :id',
        {'id': movie_id}
    )
    db.close()
    return movie

def remove_movie_by_id(db_url, movie_id):
    db = open_db(db_url)
    db.cursor().execute(
        'DELETE FROM movies WHERE id = :id',
        {'id': movie_id}
                        )
    db.commit()
    db.close()


def like_movie_by_id(db_url, movie_id):
    pass


def dislike_movie_by_id(db_url, movie_id):
    pass
