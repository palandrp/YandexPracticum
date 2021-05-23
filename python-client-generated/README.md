# swagger-client
No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

This Python package is automatically generated by the [Swagger Codegen](https://github.com/swagger-api/swagger-codegen) project:

- API version: 1.0.0
- Package version: 1.0.0
- Build package: io.swagger.codegen.v3.generators.python.PythonClientCodegen

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import swagger_client 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import swagger_client
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.MoviesApi(swagger_client.ApiClient(configuration))
movie_id = 'movie_id_example' # str | 

try:
    # Получить фильм
    api_response = api_instance.get_movie_by_id(movie_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MoviesApi->get_movie_by_id: %s\n" % e)

# create an instance of the API class
api_instance = swagger_client.MoviesApi(swagger_client.ApiClient(configuration))
limit = 50 # int | количество объектов, которое надо вывести (optional) (default to 50)
page = 1 # int | номер страницы (optional) (default to 1)
sort = 'id' # str | свойство, по которому нужно отсортировать результат (optional) (default to id)
sort_order = 'asc' # str | порядок сортировки (optional) (default to asc)
search = 'search_example' # str | неточный поиск по названию, описанию, актёрам, сценаристам и режиссёрам фильма Представьте, что вы вбили в поиск Яндекса \"Звёздные войны\" или \"Джордж Лукас\" или \"Лукас войны\"  вам выводятся соответствующие фильмы.  (optional)

try:
    # Список фильмов
    api_response = api_instance.list_movies(limit=limit, page=page, sort=sort, sort_order=sort_order, search=search)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MoviesApi->list_movies: %s\n" % e)
```

## Documentation for API Endpoints

All URIs are relative to *https://localhost/api*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*MoviesApi* | [**get_movie_by_id**](docs/MoviesApi.md#get_movie_by_id) | **GET** /movies/{movieID} | Получить фильм
*MoviesApi* | [**list_movies**](docs/MoviesApi.md#list_movies) | **GET** /movies | Список фильмов

## Documentation For Models

 - [Actor](docs/Actor.md)
 - [Movie](docs/Movie.md)
 - [ShortMovie](docs/ShortMovie.md)
 - [ValidationError](docs/ValidationError.md)
 - [ValidationErrorDetail](docs/ValidationErrorDetail.md)
 - [Writer](docs/Writer.md)

## Documentation For Authorization

 All endpoints do not require authorization.


## Author

