import sqlite3



def open_db(db_url):
    db = sqlite3.connect(db_url)
    db.row_factory = sqlite3.Row # если этого не указать, то все ответы будут возвращаться в виде tuple, а это плохо
    return db

def get_movies(db_url, page=1):
    db = open_db(db_url)
    lid = db.cursor().lastrowid
    # lid = 0
    # for row in db.cursor().execute('SELECT id from movies ORDER BY id'):
    #     lid = lid + 1
    limit = 5
    offset = limit * (page - 1)
    movies = db.cursor().execute(
        'SELECT id, name, category, genre, tags, poster, likes FROM movies LIMIT  :limit OFFSET  :offset',
    {'limit': limit, 'offset': offset}
    ).fetchall()
    db.close()
    print(lid)
    return movies


def add_movie(db_url, name, category, genre, tags, poster):
    db = open_db(db_url)
    lid = '''SELECT id FROM movies WHERE rowid=last_insert_rowid()'''
    # vid = lid + 1
    sql = '''INSERT INTO movies(id, name, category, genre, tags, poster) VALUES (?, ?, ?, ?, ?, ?)'''
    # lid = db.cursor().lastrowid
    # print(lid)
    db.cursor().execute(sql, (int(lid + 1), name, category, genre, tags, poster))
    db.commit()
    db.close()
    return lid



def update_movie(db_url, movie_id, name, category, genre, tags, poster):
    db = open_db(db_url)
    sql = '''UPDATE movies SET name = ?, category = ?, genre = ?, tags= ?, poster = ? WHERE id = ?'''
    db.cursor().execute(sql, (name, category, genre, tags, poster, movie_id))
    db.commit()
    db.close()
    return movie_id


def search_movie_by_id(db_url, movie_id):
    db = open_db(db_url)
    movie = db.cursor().execute(
        'SELECT id, name, category, genre, tags, poster, likes FROM movies WHERE id = :id',
        {'id': movie_id}
    ).fetchone()
    db.close()
    return movie

def search_movies(db_url, search):
    db = open_db(db_url)
    # search_lowercased = search.strip().lower()
    # movie = db.cursor().execute(
    #     'SELECT id, name, category, genre, tags, poster, likes FROM movies WHERE name = :search OR category = :search OR genre = :search OR tags = :search',
    #     {'name': name, 'category': category, }
    # ).fetchmany()


    sql_search = 'SELECT id, name, category, genre, tags, poster, likes FROM movies WHERE name = :search'
    db.cursor().execute(sql_search, search)
    movies = db.cursor().fetchall()
    print(search)
    db.close()
    return movies

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
