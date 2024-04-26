import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QLabel

from MathBlock import MatrixCalculator
import config as cfg


class GameLifeMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("main_window")
        self.resize(cfg.main_window_height, cfg.main_window_width)
        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)
        self.timer = QtCore.QTimer()

        self.matrix_block = MatrixCalculator(cfg.matrix_height, cfg.matrix_width, cfg.init_matrix)

        self.label_image = QLabel(self.central_widget)
        self.label_image.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.label_image.setGeometry(QtCore.QRect(cfg.matrix_window_padding_x,
                                                  cfg.matrix_window_padding_y,
                                                  cfg.matrix_window_width,
                                                  cfg.matrix_window_height))
        self.label_image.setObjectName("label_image")
        self.label_image.setPixmap(self.view())

        self.button_next = QtWidgets.QPushButton(self.central_widget)
        self.button_next.setGeometry(QtCore.QRect(30, 40, 201, 28))
        self.button_next.setStyleSheet("font: 8pt \"Arial\";")
        self.button_next.setObjectName("button_next")
        self.button_next.setText("Следующий шаг")

        self.button_pause = QtWidgets.QPushButton(self.central_widget)
        self.button_pause.setGeometry(QtCore.QRect(30, 80, 201, 28))
        self.button_pause.setStyleSheet("font: 8pt \"Arial\";")
        self.button_pause.setObjectName("button_pause")
        self.button_pause.setText("Запуск")

        self.button_previous = QtWidgets.QPushButton(self.central_widget)
        self.button_previous.setGeometry(QtCore.QRect(30, 120, 201, 28))
        self.button_previous.setStyleSheet("font: 8pt \"Arial\";")
        self.button_previous.setObjectName("button_previous")
        self.button_previous.setText("Предыдущий шаг")

        self.label_speed = QtWidgets.QLabel(self.central_widget)
        self.label_speed.setGeometry(QtCore.QRect(40, 250, 81, 20))
        self.label_speed.setStyleSheet("font: 9pt \"Arial\";")
        self.label_speed.setObjectName("label_speed")
        self.label_speed.setText("Скорость:")

        self.slider_speed = QtWidgets.QSlider(self.central_widget)
        self.slider_speed.setGeometry(QtCore.QRect(30, 280, 201, 22))
        self.slider_speed.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider_speed.setObjectName("slider_speed")

        self.label_brash = QtWidgets.QLabel(self.central_widget)
        self.label_brash.setGeometry(QtCore.QRect(40, 180, 101, 20))
        self.label_brash.setStyleSheet("font: 9pt \"Arial\";")
        self.label_brash.setObjectName("label_brash")
        self.label_brash.setText("Размер кисти:")

        self.slider_brash = QtWidgets.QSlider(self.central_widget)
        self.slider_brash.setGeometry(QtCore.QRect(30, 210, 201, 22))
        self.slider_brash.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider_brash.setObjectName("slider_brash")

    def view(self, prev: bool = False) -> QPixmap:
        if not prev:
            matrix = self.matrix_block.do_single_update_interface()
        else:
            matrix = self.matrix_block.do_single_previous_interface()
        image_data = np.uint8(matrix) * 255
        image = QImage(image_data.data, image_data.shape[1], image_data.shape[0], QImage.Format_Indexed8)
        pixmap = QPixmap.fromImage(image)
        return pixmap

