# главный рабочий класс проекта
# при изменениях в реквестах очень прошу писать комментари к коммиту

import os
import sys

import requests
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel


class MyMap(QMainWindow):
    def __init__(self):
        super().__init__()
        self.x, self.y, self.masht = '37.530887', '55.703118', '0.002'
        self.vid = 'map'
        self.metcy_and_over = {'pt=': []}
        uic.loadUi('1.ui', self)
        self.pushButton.clicked.connect(self.setImageToPixmap)
        self.pushButton_2.clicked.connect(self.search)
        self.del_ask.clicked.connect(self.delAskMethod)
        # 37.530887, 55.703118
        self.map_request_str = ''
        self.map_request = ['http://static-maps.yandex.ru/1.x/?ll=', self.x, ',',
                            self.y, '&spn=', self.masht, ',', self.masht, '&l=', self.vid]
        self.setImageToPixmap()
        self.setSelfFocus()

    def delAskMethod(self):
        self.metcy_and_over['pt='] = []
        self.ask_info.setPlainText('')
        self.ask.setText('')
        self.setImageToPixmap()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            try:
                self.mashtab.setPlainText(str(float(self.mashtab.toPlainText()) + 0.01))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)
        if event.key() == Qt.Key_PageDown:
            try:
                self.mashtab.setPlainText(str(float(self.mashtab.toPlainText()) - 0.01))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)
        if event.key() == Qt.Key_Up:
            try:
                self.edit_y.setPlainText(str(float(self.edit_y.toPlainText()) +
                                             (1 / 2) * float(self.mashtab.toPlainText())))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)
        if event.key() == Qt.Key_Down:
            try:
                self.edit_y.setPlainText(str(float(self.edit_y.toPlainText()) -
                                             (1 / 2) * float(self.mashtab.toPlainText())))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)
        if event.key() == Qt.Key_Right:
            try:
                self.edit_x.setPlainText(str(float(self.edit_x.toPlainText()) +
                                             1 * float(self.mashtab.toPlainText())))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)
        if event.key() == Qt.Key_Left:
            try:
                self.edit_x.setPlainText(str(float(self.edit_x.toPlainText()) -
                                             1 * float(self.mashtab.toPlainText())))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)

    def search(self):
        self.metcy_and_over['pt='] = []
        response = requests.get(
            "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" + self.ask.text() + "&format=json")
        print("http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" + self.ask.text() + "&format=json")
        if response:
            # Запрос успешно выполнен, печатаем полученные данные.
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            # Полный адрес топонима:
            toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            # Координаты центра топонима:
            toponym_coodrinates = toponym["Point"]["pos"]
            # Печатаем извлечённые из ответа поля:
            print(toponym_address, "имеет координаты:", toponym_coodrinates)
            self.ask_info.setPlainText('Адрес: ' + toponym_address)
            code = False
            postal_code = 'не найден'
            try:
                postal_code = toponym["metaDataProperty"]["GeocoderMetaData"]['Address']['postal_code']
                code = True
            except:
                code = False
            if self.post_indx.isChecked():
                if code:
                    print('Почтовый индекс: ', postal_code)
                    self.ask_info.setPlainText('Адрес: ' + toponym_address +
                                               '\n Почтовый индекс: ' + postal_code)
                else:
                    print('Почтовый индекс: не найден')
                    self.ask_info.setPlainText('Адрес: ' + toponym_address +
                                               '\n Почтовый индекс: ' + postal_code)
            self.metcy_and_over['pt='].append(
                (toponym_coodrinates.split()[0] + ',', toponym_coodrinates.split()[1] + ',', 'pmdol1'))
            self.edit_x.setPlainText(toponym_coodrinates.split()[0])
            self.edit_y.setPlainText(toponym_coodrinates.split()[1])
            self.setImageToPixmap()
        else:
            # Произошла ошибка выполнения запроса. Обрабатываем http-статус.
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            return -1

    def addMetcyToMap(self):
        res = ''
        if self.metcy_and_over['pt='] != []:
            res += '&pt=' + ''.join(list(map(''.join, self.metcy_and_over['pt='])))
        return res

    def getImage(self):
        self.x = self.edit_x.toPlainText().strip()
        self.y = self.edit_y.toPlainText().strip()
        self.masht = self.mashtab.toPlainText().strip()
        if self.layer.currentIndex() == 0:
            self.vid = 'sat'
        if self.layer.currentIndex() == 1:
            self.vid = 'map'
        if self.layer.currentIndex() == 2:
            self.vid = 'skl'
        self.map_request = ['http://static-maps.yandex.ru/1.x/?ll=', self.x, ',',
                            self.y, '&spn=', self.masht, ',', self.masht, '&l=', self.vid]
        self.map_request_str = ''.join(self.map_request) + self.addMetcyToMap()
        response = requests.get(self.map_request_str)
        if not response:
            return str('Ошибка выполнения запроса:' + '\n' + 'Http статус:' +
                       str(response.status_code) + '(' + str(response.reason) + ')')
            print("Ошибка выполнения запроса:")
            print(self.map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
        # Запишем полученное изображение в файл.
        if self.layer.currentIndex() > 0:
            self.map_file = "map.png"
        else:
            self.map_file = "map.jpg"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        return 'успех'

    def setImageToPixmap(self):
        is_all_secc = self.getImage()
        if is_all_secc == 'успех':
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
        else:
            self.image.setText(is_all_secc)
            win = WarningWindow(self, is_all_secc)
            win.show()
        self.setSelfFocus()

    def setSelfFocus(self):
        self.setFocusPolicy(Qt.StrongFocus)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


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
    ex = MyMap()
    ex.show()
    sys.exit(app.exec())
