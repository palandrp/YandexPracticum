import connexion
import six

from swagger_server.models.movie import Movie  # noqa: E501
from swagger_server.models.short_movie import ShortMovie  # noqa: E501
from swagger_server.models.validation_error import ValidationError  # noqa: E501
from swagger_server import util


def get_movie_by_id(movie_id):  # noqa: E501
    """Получить фильм

    Получить фильм # noqa: E501

    :param movie_id: 
    :type movie_id: str

    :rtype: Movie
    """
    return 'do some magic!'


def list_movies(limit=None, page=None, sort=None, sort_order=None, search=None):  # noqa: E501
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
    return 'do some magic!'
