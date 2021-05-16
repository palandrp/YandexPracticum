import sqlite3
import re
import hashlib

from sqlite3 import IntegrityError


def insert_multiple_records(sql, records):
    sqlite_insert_query = sql
    cur.executemany(sqlite_insert_query, records)
    con.commit()
    print("Записи успешно вставлены в таблицу", cur.rowcount)


def get_directors():
    d = {}
    for row in cur.execute('SELECT director FROM movies WHERE director is not null ORDER BY id'):
        for r in row:
            for i in r.split(','):
                if i.startswith(' '):
                    i = i[1:]
                i = i.replace('(co-director)', '')
                d[i] = 1
    return [(v,) for v in d.keys()]


def get_movie_director():
    li = []
    directors = {}
    for row in cur.execute('SELECT * FROM directors'):
        directors[row[1]] = row[0]
    for row in cur.execute('SELECT id, director FROM movies WHERE director is not null ORDER BY id'):
        for i in row[1].split(','):
            if i.startswith(' '):
                i = i[1:]
            if i.endswith('(co-director)'):
                i = i.replace('(co-director)', '')
                _id = hashlib.sha1(
                    (row[0]+str(directors[i])+'co-director').encode()).hexdigest()
                li.append((_id, row[0], directors[i], 'co-director'))
            else:
                _id = hashlib.sha1(
                    (row[0]+str(directors[i])).encode()).hexdigest()
                li.append((_id, row[0], directors[i], None))
    return li


def get_genres():
    genres = []
    for row in cur.execute('SELECT genre FROM movies WHERE genre is not null ORDER BY id'):
        li = row[0].replace("'", "").replace(" ", "").split(',')
        genres = genres + li
    su_genres = sorted(set(genres))
    return su_genres


def get_movie_genre():
    genres = get_genres()
    genre_movie = []
    for row in cur.execute('SELECT id, genre FROM movies WHERE genre is not null ORDER BY id'):
        li = [row[0]]
        g = row[1].replace(' ', '').split(',')
        for i in genres:
            if i in g:
                li.append(i)
            else:
                li.append(None)
        genre_movie.append(tuple(li))
    return genre_movie


def get_movie_writers():
    li = []
    _dict = {}
    for w in ['writer', 'writers']:
        for row in cur.execute(f"SELECT id, {w} FROM movies WHERE writer is not '' AND writer is not null ORDER BY id"):
            li.append(row)
    pattern = re.compile('[0-9a-z]{40}')
    for i in li:
        if type(i[1]) == list:
            for j in i[1:]:
                for k in re.findall(pattern, j):
                    sql = f"SELECT id, name FROM writers WHERE writer_id='{k}'"
                    for row in cur.execute(sql):
                        _id = hashlib.sha1(
                            (i[0]+str(row[0])).encode()).hexdigest()
                        _dict[_id] = (i[0], row[0])
        else:
            sql = f"SELECT id, name FROM writers WHERE writer_id='{i[1]}'"
            for row in cur.execute(sql):
                _id = hashlib.sha1((i[0]+str(row[0])).encode()).hexdigest()
                _dict[_id] = (i[0], row[0])
    return [(k, v[0], v[1]) for k, v in _dict.items()]


def remove_na():
    print("Убираем N/A в actors")
    cur.execute("UPDATE actors SET name=null WHERE name='N/A'")
    print("Убираем N/A в writers")
    cur.execute("UPDATE writers SET name=null WHERE name='N/A'")
    print("Убираем N/A в director")
    cur.execute("UPDATE movies SET director=null  WHERE director='N/A'")
    print("Убираем N/A в plot")
    cur.execute("UPDATE movies SET plot=null  WHERE plot='N/A'")
    con.commit()


def recreate_movie_actors_t():
    mov_act = []
    mov_act_d = {}
    print("Выбираем таблицу movie_actors")
    for row in cur.execute("SELECT * FROM movie_actors"):
        _id = hashlib.sha1((row[0]+row[1]).encode()).hexdigest()
        mov_act_d[_id] = (row[0], int(row[1]))
    for _id, val in mov_act_d.items():
        mov_act.append((_id, val[0], val[1]))
    print("Дропаем старую таблицу movie_actors")
    cur.execute("DROP TABLE movie_actors")
    print("Создаем новую таблицу с автоинкрементом и новым типом поля actor_id")
    print("Преобразуем тип actor_id в integer, для соответствия FK")
    cur.execute("""
        CREATE TABLE movie_actors(
        id text primary key,
        movie_id text,
        actor_id int
        )""")
    print("Пушим данные в таблицу movie_actors")
    insert_sql = "INSERT INTO movie_actors (id, movie_id, actor_id) values (?, ?, ?)"
    insert_multiple_records(insert_sql, mov_act)


def create_directors_table():
    print("Создаем таблицу directors")
    cur.execute("""
        CREATE TABLE directors(
        id integer primary key autoincrement,
        name text
        )""")
    print("Парсим режисеров из таблицы movies")
    directors = get_directors()
    print("Пушим режисеров в новую таблицу directors")
    insert_sql = "INSERT INTO directors (name) values (?)"
    insert_multiple_records(insert_sql, directors)


def create_movie_directors_t():
    print("Создаем таблицу movie_directors")
    cur.execute("""
        CREATE TABLE movie_directors(
        id text primary key,
        movie_id text,
        director_id integer,
        co_director text
        )""")
    print("Парсим режисеров из таблицы movies")
    mov_dir = get_movie_director()
    print("Пушим режисеров в новую таблицу movie_directors")
    insert_sql = "INSERT INTO movie_directors (id, movie_id, director_id, co_director) values (?, ?, ?, ?)"
    insert_multiple_records(insert_sql, mov_dir)


def recreate_writers_t():
    wrts = []
    print("Выбираем таблицу writers")
    for row in cur.execute("SELECT * FROM writers"):
        wrts.append(row)
    print("Дропаем старую таблицу writers")
    cur.execute("DROP TABLE writers")
    print("Создаем новую таблицу с автоинкрементом")
    cur.execute("""
        CREATE TABLE writers(
        id integer primary key autoincrement,
        writer_id text(27),
        name text
        )""")
    print("Пушим данные в новую таблицу writers")
    insert_sql = "INSERT INTO writers (writer_id, name) values (?, ?)"
    insert_multiple_records(insert_sql, wrts)


def create_movie_writers_t():
    print("Создаем таблицу movie_writers")
    cur.execute("""
        CREATE TABLE movie_writers(
        id text primary key,
        movie_id text,
        writer_id integer
        )""")
    print("Парсим сценаристов из таблицы movies")
    mov_writ = get_movie_writers()
    print("Пушим сценаристов в новую таблицу movie_writers")
    insert_sql = "INSERT INTO movie_writers (id, movie_id, writer_id) values (?, ?, ?)"
    insert_multiple_records(insert_sql, mov_writ)


def create_movie_genres_t():
    print("Создаем таблицу movie_genres")
    cur.execute("""
        CREATE TABLE movie_genres(
        movie_id text primary key,
        Action text,
        Adventure text,
        Animation text,
        Biography text,
        Comedy text,
        Crime text,
        Documentary text,
        Drama text,
        Family text,
        Fantasy text,
        GameShow text,
        History text,
        Horror text,
        Music text,
        Musical text,
        Mystery text,
        News text,
        RealityTV text,
        Romance text,
        SciFi text,
        Short text,
        Sport text,
        TalkShow text,
        Thriller text,
        War text,
        Western text
        )""")
    print("Парсим жанры из таблицы movies")
    movie_genres = get_movie_genre()
    print("Пушим жанры в новую таблицу movie_genres")
    insert_sql = """
        INSERT INTO movie_genres (movie_id,
        Action,
        Adventure,
        Animation,
        Biography,
        Comedy,
        Crime,
        Documentary,
        Drama,
        Family,
        Fantasy,
        GameShow,
        History,
        Horror,
        Music,
        Musical,
        Mystery,
        News,
        RealityTV,
        Romance,
        SciFi,
        Short,
        Sport,
        TalkShow,
        Thriller,
        War,
        Western) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    insert_multiple_records(insert_sql, movie_genres)


def recreate_rating_agency_t():
    print("Дропаем таблицу rating_agency")
    cur.execute("DROP TABLE rating_agency")
    print("Создаем таблицу rating_agency с использованием primary key")
    cur.execute("""
        CREATE TABLE rating_agency(
        id text primary key,
        name text
        )""")


def drop_columns():
    print("Дропаем лишние столбцы в таблицах через пересоздание таблиц (т.к. SQLite)")
    li = []
    for row in cur.execute("SELECT * FROM writers"):
        li.append((row[2],))
    cur.execute("DROP TABLE writers")
    cur.execute("""
        CREATE TABLE writers(
        id integer primary key autoincrement,
        name text
        )""")
    insert_sql = "INSERT INTO writers (name) values (?)"
    insert_multiple_records(insert_sql, li)
    li = []
    for row in cur.execute("SELECT * FROM movies"):
        try:
            imdb = float(row[7])
        except ValueError:
            imdb = None
        li.append((row[0], row[4], row[5], row[6], imdb))
    cur.execute("DROP TABLE movies")
    cur.execute("""
        CREATE TABLE movies (
        id text primary key,
        title text,
        plot text,
        ratings text,
        imdb_rating float
        )""")
    insert_sql = "INSERT INTO movies (id, title, plot, ratings, imdb_rating) values (?, ?, ?, ?, ?)"
    insert_multiple_records(insert_sql, li)
    print("Готово")


if __name__ == '__main__':

    try:
        con = sqlite3.connect('db.sqlite')
        cur = con.cursor()

        remove_na()
        recreate_movie_actors_t()
        create_directors_table()
        create_movie_directors_t()
        recreate_writers_t()
        create_movie_writers_t()
        create_movie_genres_t()
        recreate_rating_agency_t()
        drop_columns()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite DB", error)
    finally:
        if con:
            con.close()
            print("Соединение с SQLite DB закрыто")
