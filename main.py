# главный рабочий класс проекта
# при изменениях в реквестах очень прошу писать комментари к коммиту

import os
import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic
from PIL import Image


class MyMap(QWidget):
    def __init__(self):
        super().__init__()
        self.x, self.y, self.masht = '37.530887', '55.703118', '0.002'
        uic.loadUi('1.ui', self)
        self.pushButton.clicked.connect(self.setImageToPixmap)
        # 37.530887, 55.703118
        self.map_request = ['http://static-maps.yandex.ru/1.x/?ll=', self.x, ',', self.y,
                            '&spn=', self.masht, ',', self.masht, '&l=map']
        self.setImageToPixmap()
    def getImage(self):
        self.x = self.edit_x.toPlainText()
        self.y = self.edit_y.toPlainText()
        self.masht = self.mashtab.toPlainText()
        if self.layer.currentIndex() == 0:
            self.vid = 'map'
        if self.layer.currentIndex() == 1:
            self.vid = 'sat'
        if self.layer.currentIndex() == 2:
            self.vid = 'skl'
        self.map_request = ''.join(['http://static-maps.yandex.ru/1.x/?ll=', self.x, ',',
                                    self.y, '&spn=', self.masht, ',', self.masht, '&l=', self.vid])
        response = requests.get(self.map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(self.map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            return "Ошибка выполнения запроса:" + '\n' + "Http статус:", response.status_code, "(", response.reason, ")"
        # Запишем полученное изображение в файл.
        if self.layer.currentIndex() == 2 or self.layer.currentIndex() == 0:
            self.map_file = "map.png"
        if self.layer.currentIndex() == 1:
            self.map_file = "map.jpeg"
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
    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyMap()
    ex.show()
    sys.exit(app.exec())
