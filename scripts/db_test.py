import sqlite3


sql_di = """
        SELECT a.name
        FROM movie_directors AS md
        JOIN directors AS d ON md.director_id=d.id
        JOIN movie_actors AS ma ON md.movie_id=ma.movie_id
        JOIN actors AS a ON a.id=ma.actor_id
        WHERE d.name='Jørgen Lerdam'
        """

writers = [
    'Gene Roddenberry',
    'George Lucas',
    'Samuli Torssonen',
    'Damon Lindelof',
    'Alex Kurtzman'
]

actors = [
    'Anthony Daniels',
    'Mark Hamill',
    'Patrick Stewart',
    'Harrison Ford',
    'Ben Burtt'
]


def select(sql):
    for row in cur.execute(sql):
        print(row)
    print("===============")


def sql_wr(writer):
    sql = """
        SELECT COUNT(mw.movie_id)
        FROM movie_writers AS mw
        JOIN writers AS w ON mw.writer_id=w.id
        WHERE w.name='%s'
        """ % (writer,)
    return sql


def sql_ac(actor):
    sql = """
        SELECT COUNT(ma.movie_id)
        FROM movie_actors AS ma
        JOIN actors AS a ON ma.actor_id=a.id
        WHERE a.name='%s'
        """ % (actor,)
    return sql


def compare(li, sql):
    for p in li:
        for row in cur.execute(sql(p)):
            print(p, row[0])
    print("===============")


if __name__ == '__main__':

    try:
        con = sqlite3.connect('db.sqlite')
        cur = con.cursor()

        select(sql_di)
        compare(writers, sql_wr)
        compare(actors, sql_ac)
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite DB", error)
    finally:
        if con:
            con.close()
            print("Соединение с SQLite DB закрыто")
