# coding: utf-8

"""
    Spec

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class ShortMovie(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'str',
        'title': 'str',
        'imdb_rating': 'float'
    }

    attribute_map = {
        'id': 'id',
        'title': 'title',
        'imdb_rating': 'imdb_rating'
    }

    def __init__(self, id=None, title=None, imdb_rating=None):  # noqa: E501
        """ShortMovie - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._title = None
        self._imdb_rating = None
        self.discriminator = None
        self.id = id
        self.title = title
        if imdb_rating is not None:
            self.imdb_rating = imdb_rating

    @property
    def id(self):
        """Gets the id of this ShortMovie.  # noqa: E501


        :return: The id of this ShortMovie.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ShortMovie.


        :param id: The id of this ShortMovie.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def title(self):
        """Gets the title of this ShortMovie.  # noqa: E501


        :return: The title of this ShortMovie.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this ShortMovie.


        :param title: The title of this ShortMovie.  # noqa: E501
        :type: str
        """
        if title is None:
            raise ValueError("Invalid value for `title`, must not be `None`")  # noqa: E501

        self._title = title

    @property
    def imdb_rating(self):
        """Gets the imdb_rating of this ShortMovie.  # noqa: E501


        :return: The imdb_rating of this ShortMovie.  # noqa: E501
        :rtype: float
        """
        return self._imdb_rating

    @imdb_rating.setter
    def imdb_rating(self, imdb_rating):
        """Sets the imdb_rating of this ShortMovie.


        :param imdb_rating: The imdb_rating of this ShortMovie.  # noqa: E501
        :type: float
        """

        self._imdb_rating = imdb_rating

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(ShortMovie, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ShortMovie):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
