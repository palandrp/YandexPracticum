CREATE TABLE actors(
id integer primary key autoincrement,
name text
);

CREATE TABLE writers(
id text(27) primary key,
name text
);

CREATE TABLE movie_actors(
movie_id text,
actor_id text
);

CREATE TABLE movies (
id text primary key,
genre text,
director text,
writer text,
title text,
plot text,
ratings text,
imdb_rating text, writers text);

CREATE TABLE rating_agency(
id text(27),
name text
);
