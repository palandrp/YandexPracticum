import sqlite3


def select(sql):
    return [row for row in cur.execute(sql)]


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
        .replace(']', '')
    title = data['movie_desc'][0][0]
    desc = data['movie_desc'][0][-1]
    director = str([[j for j in i if j is not None] for i in data['directors']]) \
        .replace('[', '') \
        .replace(']', '') \
        .replace('(', '') \
        .replace(')', '') \
        .replace("'", '') \
        .replace(', co-director', ' - co-director') \
        .replace(',', '\n')
    actors_names = str([i[1] for i in data['actors']]) \
        .replace('[', '') \
        .replace(']', '') \
        .replace("'", '') \
        .replace(',', '\n')
    writers_names = str([i[1] for i in data['writers']]) \
        .replace('[', '') \
        .replace(']', '') \
        .replace("'", '') \
        .replace(',', '\n')
    element = {
        "id": {
            movie_id
        },
        "imdb_rating": {
            imdb_r
        },
        "genre": {
            genre
        },
        "title": {
            "raw": {
                title
            }
        },
        "description": {
            desc
        },
        "director": {
            director
        },
        "actors_names": {
            actors_names
        },
        "writers_names": {
            writers_names
        }
    }
    return element


if __name__ == '__main__':

    try:
        con = sqlite3.connect('db.sqlite')
        cur = con.cursor()

        print(parse_data(select_movie_full('tt8696442')))

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite DB", error)
    finally:
        if con:
            con.close()
            print("Соединение с SQLite DB закрыто")
