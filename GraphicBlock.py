from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene
import MathBlock
from config import matrix, matrix_width, matrix_height


class GameLifeMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Игра')
        self.resize(1200, 800)

        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName('central_widget')
        self.setCentralWidget(self.central_widget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 26))
        self.menubar.setObjectName('menubar')

        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName('menu')
        self.setMenuBar(self.menubar)
        self.menu.setTitle('Файл')

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName('statusbar')
        self.setStatusBar(self.statusbar)

        self.save = QtWidgets.QAction(self)
        self.save.setObjectName('save')
        self.save.setText('Сохранить')
        self.load = QtWidgets.QAction(self)
        self.load.setObjectName('load')
        self.load.setText('Загрузить')

        self.menu.addAction(self.save)
        self.menu.addAction(self.load)
        self.menubar.addAction(self.menu.menuAction())


class GameLifeGraphicScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.__cursor = QtCore.pyqtSignal(int, int)
        self.__math_block = MathBlock.MathCalc(matrix_height,
                                               matrix_width,
                                               matrix)

    def mousePressEvent(self, e):
        p = QCursor.pos()
        self.__cursor.emit(p.x(), p.y())
        e.accept()

