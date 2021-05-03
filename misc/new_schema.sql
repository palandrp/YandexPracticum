CREATE TABLE actors(
id integer primary key autoincrement,
name text
);

CREATE TABLE directors(
id integer primary key autoincrement,
name text
);

CREATE TABLE writers(
id integer primary key autoincrement,
name text
);

CREATE TABLE movie_actors(
id integer primary key autoincrement,
movie_id text,
actor_id text
);

CREATE TABLE movie_directors(
id integer primary key autoincrement,
movie_id text,
director_id text,
co_director tinyint
);

CREATE TABLE movie_writers(
id integer primary key autoincrement,
movie_id text,
writer_id text
);

CREATE TABLE movies (
id text primary key,
title text,
plot text,
ratings text,
imdb_rating text
);

CREATE TABLE movie_genres(
movie_id text primary key,
Action tinyint,
Adventure tinyint,
Animation tinyint,
Biography tinyint,
Comedy tinyint,
Crime tinyint,
Documentary tinyint,
Drama tinyint,
Family tinyint,
Fantasy tinyint,
GameShow tinyint,
History tinyint,
Horror tinyint,
Music tinyint,
Musical tinyint,
Mystery tinyint,
News tinyint,
RealityTV tinyint,
Romance tinyint,
SciFi tinyint,
Short tinyint,
Sport tinyint,
TalkShow tinyint,
Thriller tinyint,
War tinyint,
Western tinyint
);

CREATE TABLE rating_agency(
id text(27) primary key,
name text
);