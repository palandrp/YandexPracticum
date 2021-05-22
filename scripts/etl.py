import sqlite3
import json
import requests

from collections import deque

from request_retry import http


def select(sql):
    return [row for row in cur.execute(sql)]


def select_movie_ids():
    sql = """
            SELECT id
            FROM movies
            """
    return select(sql)


def select_actors():
    sql = """
            SELECT *
            FROM actors
            """
    return select(sql)


def select_writers():
    sql = """
            SELECT *
            FROM writers
            """
    return select(sql)


def select_movie_full(movie_id):
    sql_movie = """
            SELECT m.title, m.imdb_rating, g.*, m.plot
            FROM movies as m
            JOIN movie_genres as g ON m.id=g.movie_id
            WHERE m.id='%s'
            """ % movie_id

    sql_directors = """
            SELECT d.name, md.co_director
            FROM movie_directors as md
            JOIN directors as d ON md.director_id=d.id
            WHERE md.movie_id='%s'
            """ % movie_id

    sql_actors = """
            SELECT a.id, a.name
            FROM movie_actors as ma
            JOIN actors as a ON ma.actor_id=a.id
            WHERE ma.movie_id='%s'
            """ % movie_id

    sql_writers = """
            SELECT w.id, w.name
            FROM movie_writers as mw
            JOIN writers as w ON mw.writer_id=w.id
            WHERE mw.movie_id='%s'
            """ % movie_id
    return {
        'movie_desc': select(sql_movie),
        'directors': select(sql_directors),
        'actors': select(sql_actors),
        'writers': select(sql_writers)
    }


def parse_data(data):
    movie_id = data['movie_desc'][0][2]
    imdb_r = data['movie_desc'][0][1]
    genre = [i for i in data['movie_desc'][0][3:29] if i is not None]
    title = data['movie_desc'][0][0]
    desc = data['movie_desc'][0][-1]
    director = [[j for j in i if j is not None] for i in data['directors']]
    actors_names = [i[1] for i in data['actors']]
    writers_names = [i[1] for i in data['writers']]
    f = lambda i: {'id': i[0], 'name': i[1]}
    actors = [f(i) for i in data['actors']]
    writers = [f(i) for i in data['writers']]
    _dict = {
        "id": movie_id,
        "imdb_rating": imdb_r,
        "genre": genre,
        "title": title,
        "description": desc,
        "director": director,
        "actors_names": actors_names,
        "writers_names": writers_names,
        "actors": actors,
        "writers": writers
    }
    for k, v in _dict.items():
        if type(v) == list and (len(v) == 0 or v == [[]]):
            _dict[k] = None
    return _dict


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


def format_bulk_data(index_name, index_id, new_data: dict, data=None):
    index_addr = json.dumps({"index": {"_index": index_name, "_id": index_id}})
    index_data = json.dumps(new_data, default=set_default)
    formated_data = f'{index_addr}\n{index_data}\n'
    if data:
        return data+formated_data
    else:
        return formated_data


def bulk_elastic_request(data):
    headers = {'Content-type': 'application/x-ndjson'}
    elastic_url = 'http://127.0.0.1:9200/_bulk?filter_path=items.*.error'
    response = http.post(elastic_url, headers=headers, data=data)
    return response.text, response.status_code


if __name__ == '__main__':

    try:
        con = sqlite3.connect('db.sqlite')
        cur = con.cursor()

        bulk = 100

        movies_ids = [i[0] for i in select_movie_ids()]

        q = deque(movies_ids)
        while len(q) > 0:
            f_data = None
            for _ in range(bulk):
                try:
                    _id = q.pop()
                    item = parse_data(select_movie_full(_id))
                    f_data = format_bulk_data('movies', _id, item, f_data)
                except IndexError:
                    break
            text, status = bulk_elastic_request(f_data)
            if status != 200:
                print(text)
            else:
                print(f"Loaded {bulk} records")

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite DB", error)
    finally:
        if con:
            con.close()
            print("Соединение с SQLite DB закрыто")
