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

class ValidationErrorDetail(object):
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
        'loc': 'list[str]',
        'msg': 'str',
        'type': 'str'
    }

    attribute_map = {
        'loc': 'loc',
        'msg': 'msg',
        'type': 'type'
    }

    def __init__(self, loc=None, msg=None, type=None):  # noqa: E501
        """ValidationErrorDetail - a model defined in Swagger"""  # noqa: E501
        self._loc = None
        self._msg = None
        self._type = None
        self.discriminator = None
        if loc is not None:
            self.loc = loc
        if msg is not None:
            self.msg = msg
        if type is not None:
            self.type = type

    @property
    def loc(self):
        """Gets the loc of this ValidationErrorDetail.  # noqa: E501


        :return: The loc of this ValidationErrorDetail.  # noqa: E501
        :rtype: list[str]
        """
        return self._loc

    @loc.setter
    def loc(self, loc):
        """Sets the loc of this ValidationErrorDetail.


        :param loc: The loc of this ValidationErrorDetail.  # noqa: E501
        :type: list[str]
        """

        self._loc = loc

    @property
    def msg(self):
        """Gets the msg of this ValidationErrorDetail.  # noqa: E501


        :return: The msg of this ValidationErrorDetail.  # noqa: E501
        :rtype: str
        """
        return self._msg

    @msg.setter
    def msg(self, msg):
        """Sets the msg of this ValidationErrorDetail.


        :param msg: The msg of this ValidationErrorDetail.  # noqa: E501
        :type: str
        """

        self._msg = msg

    @property
    def type(self):
        """Gets the type of this ValidationErrorDetail.  # noqa: E501


        :return: The type of this ValidationErrorDetail.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ValidationErrorDetail.


        :param type: The type of this ValidationErrorDetail.  # noqa: E501
        :type: str
        """

        self._type = type

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
        if issubclass(ValidationErrorDetail, dict):
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
        if not isinstance(other, ValidationErrorDetail):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
