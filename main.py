import sys
from PyQt5.QtWidgets import QApplication
from GraphicBlock import GameLifeMainWindow


def start():
    app = QApplication(sys.argv)
    window = GameLifeMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    start()
