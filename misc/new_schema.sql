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
id text primary key,
movie_id text,
actor_id integer
);

CREATE TABLE movie_directors(
id text primary key,
movie_id text,
director_id integer,
co_director text
);

CREATE TABLE movie_writers(
id text primary key,
movie_id text,
writer_id integer
);

CREATE TABLE movies (
id text primary key,
title text,
plot text,
ratings text,
imdb_rating float
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
id text primary key,
name text
);