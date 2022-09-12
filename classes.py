from PyQt5.Qt import *


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle('hello')
        self.resize(500,500)
        self.move(400,200)
    def setup_ui(self):
        label = QLabel(self)
        label.setText('SSS')


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
