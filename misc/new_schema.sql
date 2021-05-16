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
co_director text
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
);

CREATE TABLE rating_agency(
id text(27) primary key,
name text
);