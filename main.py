import sys
from io import BytesIO

import requests
from PIL import Image

from Functions import takeParametersForTheMapScale_GEO, findSomethingAround, takeParametersForTheMapScale_SEARCH

# Этот класс поможет нам сделать картинку из потока байт

# Пусть наше приложение предполагает запуск:
# python main.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    print('нет запроса')
    exit(0)
    pass

# получаем параметры для заданного объекта.
map_params = takeParametersForTheMapScale_GEO(response)
response_find_something = findSomethingAround(map_params['ll'], 'аптека')
print(response_find_something)
map_params = takeParametersForTheMapScale_SEARCH(response_find_something[0], response_find_something[1], 10)

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).save('image.png')
