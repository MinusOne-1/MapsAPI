import requests


def takeParametersForTheMapScale_GEO(response):
    '''получает на вход ответ сервера http://geocode-maps.yandex.ru/1.x/ - response.
            Возвращает параметры для запроса к http://static-maps.yandex.ru/1.x/

            Возвращает словарь, ключами являются: "ll" - точка центра карты, "spn" - градусные замеры карты,
            "l" - вид карты(карта/спутник/гибридный), "pt" - метки на карте.'''
    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    uCorner = list(map(float, toponym['boundedBy']['Envelope']['upperCorner'].split()))
    lCorner = list(map(float, toponym['boundedBy']['Envelope']['lowerCorner'].split()))

    # получамем размеры объекта в градусной мере
    delta = str(uCorner[0] - lCorner[0])
    delta1 = str(uCorner[1] - lCorner[1])

    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta1]),
        "l": "map",
        'pt': ",".join([toponym_longitude, toponym_lattitude]) + ',pm2rdl'
    }
    return map_params


def takeParametersForTheMapScale_SEARCH(response, address_ll, n=1):
    '''получает на вход ответ сервера https://search-maps.yandex.ru/v1/ - response
    и address_ll - точку центра карты,
    а так же доп.параметр - n - количество организаций, метки которых нужно вернуть. по умолчанию равно 1.
            Возвращает параметры для запроса к http://static-maps.yandex.ru/1.x/


            Возвращает словарь, ключами являются: "ll" - точка центра карты, "spn" - градусные замеры карты,
            "l" - вид карты(карта/спутник/гибридный), "pt" - метки на карте.'''
    # Преобразуем ответ в json-объект
    json_response = response.json()
    delta = "0.005"
    org_point_gr = []
    org_point_lb = []
    org_point_gn = []
    for i in range(n):
        try:
            # Получаем n-ную найденную организацию.
            organization = json_response["features"][i]
            # Название организации.
            org_name = organization["properties"]["CompanyMetaData"]["name"]
            # Адрес организации.
            org_address = organization["properties"]["CompanyMetaData"]["address"]

            # Получаем координаты ответа.
            point = organization["geometry"]["coordinates"]
            try:
                TwentyFourHours = organization["properties"]["CompanyMetaData"]['Hours']['Availabilities'][
                    'TwentyFourHours']
                if TwentyFourHours:
                    org_point_gn.append("{0},{1}".format(point[0], point[1]))
                else:
                    org_point_lb.append("{0},{1}".format(point[0], point[1]))
            except:
                org_point_gr.append("{0},{1}".format(point[0], point[1]))
        except:
            break

    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        # позиционируем карту центром на наш исходный адрес
        "ll": address_ll,
        "spn": ",".join([delta, delta]),
        "l": "map",
        # добавим точку, чтобы указать найденную аптеку
        "pt": '~'.join([f"{i},pm2gnl" for i in org_point_gn]) + '~' +
              '~'.join([f"{i},pm2lbl" for i in org_point_lb]) + '~' +
              '~'.join([f"{i},pm2grl" for i in org_point_gr])
    }
    return map_params


def findSomethingAround(point, something):
    '''Получает на вход: point - точку, вокруг которой вёдется поиск,
    something - то, что будем искать вокруг этой точки.

    Возвращает кортеж - (response, point) - где response - ответ сервера https://search-maps.yandex.ru/v1/
    и point - точка, вокруг которой велся поиск.'''
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

    search_params = {
        "apikey": api_key,
        "text": something,
        "lang": "ru_RU",
        "ll": point,
        "type": "biz"
    }

    response = requests.get(search_api_server, params=search_params)
    if not response:
        return 'нет запроса'
    return (response, point)
