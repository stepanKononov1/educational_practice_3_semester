import random

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
        self.setFixedSize(QtCore.QSize(cfg.main_window_height, cfg.main_window_width))
        self.setStyleSheet("background-color: #e0e0e0; font: \"Times New Roman\";")
        self.setWindowTitle('игра "Жизнь"')
        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

        self.matrix_label = MatrixLabel(self.central_widget)
        self.matrix_label.setAlignment(Qt.AlignTop)
        self.matrix_label.setGeometry(QtCore.QRect(cfg.matrix_window_padding_x,
                                                   cfg.matrix_window_padding_y,
                                                   cfg.matrix_window_height,
                                                   cfg.matrix_window_width))

        self.button_next = QtWidgets.QPushButton(self.central_widget)
        self.button_next.setGeometry(QtCore.QRect(30, 40, 201, 28))
        self.button_next.setStyleSheet("font: 8pt \"Arial\"; background-color: white;")
        self.button_next.setObjectName("button_next")
        self.button_next.setText("Следующий шаг")
        self.button_next.clicked.connect(self.button_next_foo)

        self.button_pause = QtWidgets.QPushButton(self.central_widget)
        self.button_pause.setGeometry(QtCore.QRect(30, 80, 201, 28))
        self.button_pause.setStyleSheet("font: 8pt \"Arial\"; background-color: white;")
        self.button_pause.setObjectName("button_pause")
        self.button_pause.setText("Запуск")
        self.button_pause.clicked.connect(self.button_pause_foo)

        self.button_previous = QtWidgets.QPushButton(self.central_widget)
        self.button_previous.setGeometry(QtCore.QRect(30, 120, 201, 28))
        self.button_previous.setStyleSheet("font: 8pt \"Arial\"; background-color: white;")
        self.button_previous.setObjectName("button_previous")
        self.button_previous.setText("Предыдущий шаг")
        self.button_previous.clicked.connect(self.button_previous_foo)

        self.button_clear_screen = QtWidgets.QPushButton(self.central_widget)
        self.button_clear_screen.setGeometry(QtCore.QRect(30, 330, 201, 28))
        self.button_clear_screen.setStyleSheet("font: 8pt \"Arial\"; background-color: white;")
        self.button_clear_screen.setObjectName("button_clear_screen")
        self.button_clear_screen.setText("Очистить экран")
        self.button_clear_screen.clicked.connect(self.button_clear_screen_foo)

        self.label_white_space = QLabel(self.central_widget)
        self.label_white_space.setGeometry(QtCore.QRect(20, 170, 221, 140))
        self.label_white_space.setStyleSheet("background-color: white;")

        self.label_brash = QLabel(self.central_widget)
        self.label_brash.setGeometry(QtCore.QRect(30, 180, 101, 20))
        self.label_brash.setStyleSheet("font: 9pt \"Arial\"; background-color: white;")
        self.label_brash.setObjectName("label_brash")
        self.label_brash.setText("Размер кисти:")

        self.slider_brash = QtWidgets.QSlider(self.central_widget)
        self.slider_brash.setGeometry(QtCore.QRect(30, 210, 201, 20))
        self.slider_brash.setStyleSheet("background-color: white;")
        self.slider_brash.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider_brash.setObjectName("slider_brash")
        self.slider_brash.setMinimum(cfg.min_size_brash)
        self.slider_brash.setMaximum(cfg.max_size_brash)
        self.slider_brash.valueChanged.connect(self.on_brash_radius_event)

        self.label_speed = QLabel(self.central_widget)
        self.label_speed.setGeometry(QtCore.QRect(30, 250, 81, 20))
        self.label_speed.setStyleSheet("font: 9pt \"Arial\"; background-color: white;")
        self.label_speed.setObjectName("label_speed")
        self.label_speed.setText("Скорость:")

        self.slider_speed = QtWidgets.QSlider(self.central_widget)
        self.slider_speed.setGeometry(QtCore.QRect(30, 280, 201, 20))
        self.slider_speed.setStyleSheet("background-color: white;")
        self.slider_speed.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider_speed.setObjectName("slider_speed")
        self.slider_speed.setMinimum(cfg.min_speed)
        self.slider_speed.setMaximum(cfg.max_speed)
        self.slider_speed.valueChanged.connect(self.on_change_speed_event)

    def button_next_foo(self):
        self.matrix_label.single_update()

    def button_previous_foo(self):
        self.matrix_label.single_update(prev=True)
        self.matrix_label.timer.stop()
        self.button_pause.setText('Запуск')

    def on_change_speed_event(self):
        time = abs(self.slider_speed.value() - cfg.max_speed)
        if time < cfg.min_speed:
            time = cfg.min_speed
        self.matrix_label.timer.setInterval(time)
    
    def button_clear_screen_foo(self):
        self.matrix_label.timer.stop()
        self.button_pause.setText('Запуск')
        self.matrix_label.matrix_block.set_matrix(np.zeros((cfg.matrix_height, cfg.matrix_width), dtype=np.bool_))
        self.matrix_label.matrix_update(
            self.matrix_label.matrix_block.get_matrix_without_border(
                self.matrix_label.matrix_block.get_matrix()
            )
        )

    def on_brash_radius_event(self):
        brash_radius = self.slider_brash.value()
        self.matrix_label.brash_radius = brash_radius // cfg.brush_step

    def button_pause_foo(self):
        if self.matrix_label.timer.isActive():
            self.button_pause.setText('Запуск')
            self.matrix_label.timer.stop()
        else:
            self.button_pause.setText('Пауза')
            self.matrix_label.timer.start(abs(self.slider_speed.value() - cfg.max_speed))


class MatrixLabel(QLabel):
    def __init__(self, parent: Qt.Widget):
        super().__init__(parent=parent)
        self.matrix_block = MatrixCalculator()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.single_update)
        self.brash_radius = cfg.min_size_brash
        self.matrix_update(self.matrix_block.get_matrix_without_border(
            self.matrix_block.get_matrix())
        )

    def matrix_update(self, matrix: np.array):
        image_data = np.uint8(matrix) * 255
        image = QImage(image_data.data, image_data.shape[1], image_data.shape[0], image_data.strides[0],
                       QImage.Format_Indexed8)
        self.setPixmap(QPixmap.fromImage(image).scaled(cfg.matrix_window_height,
                                                       cfg.matrix_window_width,
                                                       Qt.KeepAspectRatio,
                                                       Qt.FastTransformation))

    def single_update(self, prev: bool = False):
        if not prev:
            matrix = self.matrix_block.do_single_update_interface()
        else:
            matrix = self.matrix_block.do_single_previous_interface()
        self.matrix_update(matrix)

    def change_matrix_mouse_event(self, x: int, y: int):
        if x < 0 or y < 0:
            return
        matrix = self.matrix_block.get_matrix()
        matrix_x, matrix_y = matrix.shape
        y = y // cfg.cell_size + 1
        x = x // cfg.cell_size + 1
        if self.brash_radius == 0:
            try:
                matrix[y][x] = not matrix[y][x]
            except IndexError:
                pass
        else:
            for i in range(y - self.brash_radius, y + self.brash_radius):
                for j in range(x - self.brash_radius, x + self.brash_radius):
                    if i > matrix_x - 2 or j > matrix_y - 2 or i < 1 or j < 1:
                        continue
                    try:
                        matrix[i][j] = bool(random.getrandbits(1))
                    except IndexError:
                        pass
        self.matrix_block.set_matrix(matrix)
        self.matrix_update(self.matrix_block.get_matrix_without_border(matrix))

    def mousePressEvent(self, event):
        self.change_matrix_mouse_event(event.pos().x(), event.pos().y())

    def mouseMoveEvent(self, event):
        self.change_matrix_mouse_event(event.pos().x(), event.pos().y())
