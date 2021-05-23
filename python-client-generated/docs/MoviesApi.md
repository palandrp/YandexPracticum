# swagger_client.MoviesApi

All URIs are relative to *https://localhost/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_movie_by_id**](MoviesApi.md#get_movie_by_id) | **GET** /movies/{movieID} | Получить фильм
[**list_movies**](MoviesApi.md#list_movies) | **GET** /movies | Список фильмов

# **get_movie_by_id**
> Movie get_movie_by_id(movie_id)

Получить фильм

Получить фильм

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.MoviesApi()
movie_id = 'movie_id_example' # str | 

try:
    # Получить фильм
    api_response = api_instance.get_movie_by_id(movie_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MoviesApi->get_movie_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **movie_id** | **str**|  | 

### Return type

[**Movie**](Movie.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_movies**
> list[ShortMovie] list_movies(limit=limit, page=page, sort=sort, sort_order=sort_order, search=search)

Список фильмов

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.MoviesApi()
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

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| количество объектов, которое надо вывести | [optional] [default to 50]
 **page** | **int**| номер страницы | [optional] [default to 1]
 **sort** | **str**| свойство, по которому нужно отсортировать результат | [optional] [default to id]
 **sort_order** | **str**| порядок сортировки | [optional] [default to asc]
 **search** | **str**| неточный поиск по названию, описанию, актёрам, сценаристам и режиссёрам фильма Представьте, что вы вбили в поиск Яндекса \&quot;Звёздные войны\&quot; или \&quot;Джордж Лукас\&quot; или \&quot;Лукас войны\&quot;  вам выводятся соответствующие фильмы.  | [optional] 

### Return type

[**list[ShortMovie]**](ShortMovie.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

