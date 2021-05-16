import sqlite3
import json
import requests

from collections import deque

from req_retr import http


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
    genre = str([i for i in data['movie_desc'][0][3:29] if i is not None]) \
        .replace('[', '') \
        .replace("'", '') \
        .replace(']', '')
    title = data['movie_desc'][0][0]
    desc = data['movie_desc'][0][-1]
    director = str([[j for j in i if j is not None] for i in data['directors']]) \
        .replace('[', '') \
        .replace(']', '') \
        .replace('(', '') \
        .replace(')', '') \
        .replace("'", '') \
        .replace(', co-director', ' - co-director')
    actors_names = str([i[1] for i in data['actors']]) \
        .replace('[', '') \
        .replace(']', '') \
        .replace("'", '')
    writers_names = str([i[1] for i in data['writers']]) \
        .replace('[', '') \
        .replace(']', '') \
        .replace("'", '')
    item = {
        "id": movie_id,
        "imdb_rating": imdb_r,
        "genre": genre,
        "title": title,
        "description": desc,
        "director": director,
        "actors_names": actors_names,
        "writers_names": writers_names
    }
    return item


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
    return response.text


if __name__ == '__main__':

    try:
        con = sqlite3.connect('db.sqlite')
        cur = con.cursor()

        bulk = 100

        movies_ids = [i[0] for i in select_movie_ids()]
        actors = select_actors()
        writers = select_writers()

        _dict = {'actors': actors, 'writers': writers, 'movies': movies_ids}
        for key, val in _dict.items():
            q = deque(val)
            while len(q) > 0:
                f_data = None
                for _ in range(bulk):
                    try:
                        if key == 'movies':
                            _id = q.pop()
                            item = parse_data(select_movie_full(_id))
                        else:
                            item = q.pop()
                            _id = item[0]
                            item = {'id': _id, 'name': item[1]}
                        f_data = format_bulk_data(key, _id, item, f_data)
                    except IndexError:
                        break
                r = bulk_elastic_request(f_data)
                print(r)

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite DB", error)
    finally:
        if con:
            con.close()
            print("Соединение с SQLite DB закрыто")
