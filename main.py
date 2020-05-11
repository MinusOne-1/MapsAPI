import os
import sys
from io import BytesIO
from random import choice as ch

import requests
from PIL import Image
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication


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
    # и забиваем на них

    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta1]),
        "l": ch(["map", 'sat'])  # ,
        # 'pt': ",".join([toponym_longitude, toponym_lattitude]) + ',pm2rdl'
    }
    if map_params["l"] == 'map':
        delta = '0.002'
        delta1 = '0.002'
        map_params["spn"] = ",".join([delta, delta1])
    return map_params


class CitysGuess(QMainWindow):
    def __init__(self):
        super().__init__()
        self.indx = 0
        self.cities = ['Москва', 'Санкт-Петебург', 'Будапешт', 'Талин', 'Краснодар',
                       'Екатеренбург', 'Оренбург', 'Прага', 'Рига', 'Лондон']
        uic.loadUi('citys_guess_ui.ui', self)
        self.pushButton.clicked.connect(self.next_prev_b)
        self.pushButton_2.clicked.connect(self.next_prev_b)

        self.getCitysImage()
        self.setImageToPixmap()

    def next_prev_b(self):
        if self.sender() == self.pushButton:
            self.indx += 1
            if self.indx >= len(self.cities):
                self.indx = 0
        else:
            self.indx -= 1
            if self.indx < 0:
                self.indx = len(self.cities) - 1
        self.setImageToPixmap()

    def setImageToPixmap(self):
        is_all_secc = self.getImage()
        self.pixmap = QPixmap(is_all_secc)
        self.image.setPixmap(self.pixmap)

    def getCitysImage(self):
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        for i in self.cities:
            geocoder_params = {
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                "geocode": i,
                "format": "json"}
            response = requests.get(geocoder_api_server, params=geocoder_params)
            if not response:
                print('нет запроса', i)
                continue

            # получаем параметры для заданного объекта.
            map_params = takeParametersForTheMapScale_GEO(response)
            map_api_server = "http://static-maps.yandex.ru/1.x/"
            response = requests.get(map_api_server, params=map_params)
            if not response:
                print('no zapros', i)
                continue
            if map_params['l'] == 'map':
                Image.open(BytesIO(
                    response.content)).save('image_' + i + '.png')
            else:
                Image.open(BytesIO(
                    response.content)).save('image_' + i + '.jpg')

    def getImage(self):
        file = 'image_' + self.cities[self.indx] + '.png'
        if os.path.exists(file):
            return file
        else:
            file = 'image_' + self.cities[self.indx] + '.jpg'
            if os.path.exists(file):
                return file
            return 'image.png'

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        for i in self.cities:
            try:
                os.remove('image_' + i + '.png')
            except:
                pass
            try:
                os.remove('image_' + i + '.jpg')
            except:
                continue


class WarningWindow(QMainWindow):
    def __init__(self, main, text):
        super().__init__(main)
        self.setGeometry(50, 50, 500, 500)
        self.warning = QLabel(self)
        self.warning.setText(text)
        self.warning.resize(self.warning.sizeHint())
        self.warning.move(250 - self.warning.width() // 2, 250 - self.warning.height() // 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CitysGuess()
    ex.show()
    sys.exit(app.exec())
