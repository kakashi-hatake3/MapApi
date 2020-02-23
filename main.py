import os
import sys
from Map_API import MapAPI

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit


SCREEN_SIZE = [600, 500]


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.map_api = MapAPI()  # сама карта
        self.map_api.draw()
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap('map.png')
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

        self.object_input = QLineEdit(self)
        self.object_input.move(10, 460)
        self.object_input.resize(475, 25)

        self.btn = QPushButton('Search', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(490, 460)
        self.btn.clicked.connect(self.search)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp and int(self.map_api.zoom) < 17:
            self.map_api.zoom = str(int(self.map_api.zoom) + 1)
            self.update_map()
        elif event.key() == Qt.Key_PageDown and int(self.map_api.zoom) > 2:
            self.map_api.zoom = str(int(self.map_api.zoom) - 1)
            self.update_map()
        elif event.key() == Qt.Key_A:
            self.map_api.cords[0] = str((float(self.map_api.cords[0]) - 720 / 2 ** int(self.map_api.zoom) + 180) % 360 - 180)
            self.update_map()
        elif event.key() == Qt.Key_D:
            self.map_api.cords[0] = str((float(self.map_api.cords[0]) + 720 / 2 ** int(self.map_api.zoom) + 180) % 360 - 180)
            self.update_map()
        elif event.key() == Qt.Key_W and -90 >= float(self.map_api.cords[1]) + 360 / 2 ** int(self.map_api.zoom) >= 90:
            self.map_api.cords[1] = str(float(self.map_api.cords[1]) + 360 / 2 ** int(self.map_api.zoom))
            self.update_map()
        elif event.key() == Qt.Key_S and -90 >= float(self.map_api.cords[1]) - 360 / 2 ** int(self.map_api.zoom) >= 90:
            self.map_api.cords[1] = str(float(self.map_api.cords[1]) - 360 / 2 ** int(self.map_api.zoom))
            self.update_map()
        elif event.key() == Qt.Key_End:
            self.map_api.mod += 1
            self.update_map()

    def search(self):
        find_object = self.object_input.text()
        self.map_api.find(find_object)
        self.image.setPixmap(QPixmap('map.png'))

    def update_map(self):
        self.map_api.draw()
        self.image.setPixmap(QPixmap('map.png'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
