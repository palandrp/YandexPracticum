import sqlite3
import json
import requests

from collections import deque

from request_retry import http


class ESLoader:
    def __init__(self, url: str):
        self.url = url

    def format_bulk_data(self, index_name: str, index_id: str, new_data: dict, data=None):
        '''
        This makes a json string for elastic request. If we give this one more formed string,
        that will plus it to formatted output. So we can call this many times in a loop to
        format a large bulk request. 
        :param index_name: the name of the index into which the data will be loaded
        :param index_id: index id, set equal to movie id
        :param new_data: dict with data to be formatted
        :param data: already formed data that you want to add to your new_data
        '''
        def set_default(obj):
            if isinstance(obj, set):
                return list(obj)
            raise TypeError
        index_addr = json.dumps(
            {"index": {"_index": index_name, "_id": index_id}})
        index_data = json.dumps(new_data, default=set_default)
        formated_data = f'{index_addr}\n{index_data}\n'
        if data:
            return data+formated_data
        else:
            return formated_data

    def load_to_es(self, data: str):
        headers = {'Content-type': 'application/x-ndjson'}
        elastic_url = self.url
        response = http.post(elastic_url, headers=headers, data=data)
        return response.text, response.status_code


class ETL:
    def __init__(self, conn: sqlite3.Connection, es_loader: ESLoader):
        self.es_loader = es_loader
        self.conn = conn
        self.cur = conn.cursor()
        self.bulk = 250

    def select_movie_ids(self):
        sql = """
                SELECT id
                FROM movies
                """
        return [row for row in self.cur.execute(sql)]

    def extract_movie_full(self, movie_id: str):
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
            'movie_desc': [row for row in self.cur.execute(sql_movie)],
            'directors': [row for row in self.cur.execute(sql_directors)],
            'actors': [row for row in self.cur.execute(sql_actors)],
            'writers': [row for row in self.cur.execute(sql_writers)]
        }

    def transform_data(self, data: dict):
        movie_id = data['movie_desc'][0][2]
        imdb_r = data['movie_desc'][0][1]
        genre = [i for i in data['movie_desc'][0][3:29] if i is not None]
        title = data['movie_desc'][0][0]
        desc = data['movie_desc'][0][-1]
        director = [[j for j in i if j is not None] for i in data['directors']]
        actors_names = [i[1] for i in data['actors']]
        writers_names = [i[1] for i in data['writers']]
        def f(i): return {'id': i[0], 'name': i[1]}
        actors = [f(i) for i in data['actors']]
        writers = [f(i) for i in data['writers']]
        _dict = {
            "id": movie_id,
            "imdb_rating": imdb_r,
            "genre": genre,
            "title": title,
            "description": desc,
            "director": director[0],
            "actors_names": actors_names,
            "writers_names": writers_names,
            "actors": actors,
            "writers": writers
        }
        for k, v in _dict.items():
            if type(v) == list and (len(v) == 0 or v == [[]]):
                _dict[k] = None
        return _dict

    def load(self):
        '''
        This uses the bulk parameter from the class field, calls the transform_data and
        format_bulk_data methods to completely build the data for the elasticsearch query.
        It first gets all movie IDs from SQLite, queues them up, and iterates over them.
        When the data has been formatted, it calls load_to_es to send it to elasticsearch. 
        '''
        try:
            movies_ids = [i[0] for i in self.select_movie_ids()]
            q = deque(movies_ids)
            while len(q) > 0:
                bulk_data = None
                i = 0
                for _ in range(self.bulk):
                    try:
                        _id = q.pop()
                        movie_item = self.transform_data(
                            self.extract_movie_full(_id))
                        bulk_data = self.es_loader.format_bulk_data(
                            'movies', _id, movie_item, bulk_data)
                        i += 1
                    except IndexError:
                        break
                text, status = self.es_loader.load_to_es(bulk_data)
                if status != 200:
                    print(text)
                else:
                    print(f"Loaded {i} records")
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite DB", error)
        finally:
            if self.conn:
                self.conn.close()
                print("Соединение с SQLite DB закрыто")


if __name__ == "__main__":

    ETL(

        sqlite3.connect('db.sqlite'),
        ESLoader('http://127.0.0.1:9200/_bulk?filter_path=items.*.error')

    ).load()
