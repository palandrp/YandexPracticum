# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.movie import Movie  # noqa: E501
from swagger_server.models.short_movie import ShortMovie  # noqa: E501
from swagger_server.models.validation_error import ValidationError  # noqa: E501
from swagger_server.test import BaseTestCase


class TestMoviesController(BaseTestCase):
    """MoviesController integration test stubs"""

    def test_get_movie_by_id(self):
        """Test case for get_movie_by_id

        Получить фильм
        """
        response = self.client.open(
            '/api/movies/{movieID}'.format(movie_id='movie_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_movies(self):
        """Test case for list_movies

        Список фильмов
        """
        query_string = [('limit', 50),
                        ('page', 1),
                        ('sort', 'id'),
                        ('sort_order', 'asc'),
                        ('search', 'search_example')]
        response = self.client.open(
            '/api/movies',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
