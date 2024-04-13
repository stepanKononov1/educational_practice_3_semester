from PyQt5.QtWidgets import QApplication
from GraphicBlock import GameLifeMainWindow


def start():
    app = QApplication([])
    window = GameLifeMainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    start()
