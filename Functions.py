def takeParametersForTheMapScale(response):
    '''получает на вход ответ сервера http://geocode-maps.yandex.ru/1.x/ - response.
            Возвращает параметры для запроса к http://static-maps.yandex.ru/1.x/'''
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
