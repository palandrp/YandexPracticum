import connexion
import six

from swagger_server.models.movie import Movie  # noqa: E501
from swagger_server.models.short_movie import ShortMovie  # noqa: E501
from swagger_server.models.validation_error import ValidationError  # noqa: E501
from swagger_server import util

import requests

from flask import abort


def get_movie_by_id(movie_id):  # noqa: E501
    """Получить фильм

    Получить фильм # noqa: E501

    :param movie_id: 
    :type movie_id: str

    :rtype: Movie
    """
    result = requests.get(
        'http://elasticsearch:9200/movies/_search',
        json={
            "_source": {
                "exclude": [
                    "writers_names",
                    "actors_names"
                ]
            },
            "query": {
                "match": {
                    "id": {
                        "query": movie_id,
                        "fuzziness": 0
                    }
                }
            },
            "size": 1
        }).json()

    try:
        source = result['hits']['hits'][0]['_source']
    except IndexError:
        abort(404)

    return source


def list_movies(limit=50, page=1, sort='id', sort_order='asc', search=None):  # noqa: E501
    """Список фильмов

     # noqa: E501

    :param limit: количество объектов, которое надо вывести
    :type limit: int
    :param page: номер страницы
    :type page: int
    :param sort: свойство, по которому нужно отсортировать результат
    :type sort: str
    :param sort_order: порядок сортировки
    :type sort_order: str
    :param search: неточный поиск по названию, описанию, актёрам, сценаристам и режиссёрам фильма Представьте, что вы вбили в поиск Яндекса \&quot;Звёздные войны\&quot; или \&quot;Джордж Лукас\&quot; или \&quot;Лукас войны\&quot;  вам выводятся соответствующие фильмы. 
    :type search: str

    :rtype: List[ShortMovie]
    """

    if limit <= 0 or limit >= 50 or page <= 0 or page >= 100:
        abort(422)

    result = requests.get(
        'http://elasticsearch:9200/movies/_search',
        json={
            "query": {
                "multi_match": {
                    "query": search,
                    "fuzziness": 0,
                    "fields": [
                        "title^4",
                        "description",
                        "genre",
                        "actors_names",
                        "writers_names",
                        "director"
                    ]
                }
            }
        }).json()

    start = limit * page - limit
    stop = limit * page

    source = []
    for i in range(start, stop):
        try:
            source.append(result['hits']['hits'][i]['_source'])
        except IndexError:
            break


    if sort_order == 'asc':
        reverse = False
    else:
        reverse = True

    source.sort(key=lambda x: (x[sort]), reverse=reverse)

    return source
