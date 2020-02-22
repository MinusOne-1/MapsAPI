# главный рабочий класс проекта
# при изменениях в реквестах очень прошу писать комментари к коммиту


import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5 import uic
from PyQt5.QtCore import Qt


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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            try:
                self.mashtab.setPlainText(str(float(self.mashtab.toPlainText()) + 0.01))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)
        elif event.key() == Qt.Key_PageDown:
            try:
                self.mashtab.setPlainText(str(float(self.mashtab.toPlainText()) - 0.01))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)

    def getImage(self):
        self.x = self.edit_x.toPlainText().strip()
        self.y = self.edit_y.toPlainText().strip()
        self.masht = self.mashtab.toPlainText().strip()
        self.map_request = ''.join(['http://static-maps.yandex.ru/1.x/?ll=', self.x, ',',
                                    self.y, '&spn=', self.masht, ',', self.masht, '&l=map'])
        response = requests.get(self.map_request)
        if not response:
            return str('Ошибка выполнения запроса:' + '\n' + 'Http статус:' +
                       str(response.status_code) + '(' + str(response.reason) + ')')
        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        return 'успех'

    def setImageToPixmap(self):
        is_all_secc = self.getImage()
        print(is_all_secc)
        if is_all_secc == 'успех':
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
        else:
            win = WarningWindow(self, is_all_secc)
            win.show()

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
