import sys, os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPropertyAnimation
from Crypto.Random import get_random_bytes
from math import sin
import importlib.util


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    
    def button_callback(self):
        pos = self.button.pos()
        x, y = pos.x(), pos.y()

        for i in range(100):
            self.click_animation.setKeyValueAt(i/100, QtCore.QPoint(x, y - round(2*sin(i/100*3.1415*3))))

        self.click_animation.setEndValue(pos)

        self.click_animation.start()

        self.status.setText('Статус: Установка библиотек...') 
        os.system('pip install pyinstaller')
        os.system('pip install PyQt5') 
        os.system('pip install pycryptodome')

        with open(resource_path("key.txt"), "wb") as f:
            f.write(get_random_bytes(32))

        self.process = QtCore.QProcess()
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)

        self.process.start("py", ["-m", "PyInstaller", resource_path('main.py'), "-F", "-w", "-n=AESclient", "--noconsole", "--add-data", resource_path("key.txt;."), "--add-data", resource_path("logo.png;."), "--onefile", "--icon", resource_path("logo.ico")])
        self.process.finished.connect(self.delete_key)

    
    @staticmethod
    def delete_key():
        os.remove(resource_path("key.txt"))


    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode("cp1251")
        self.status.setText(f"Статус: {stdout}")


    def handle_stderr(self):
        data = self.process.readAllStandardError()
        stderr = bytes(data).decode("cp1251")
        self.status.setText(f"Статус: {stderr}")



    def setup_ui(self):
        self.widget = QtWidgets.QWidget()
        self.widget.setFixedSize(900, 260)
        self.setWindowIcon(QtGui.QIcon(resource_path("logo.png")))

        self.l1 = QtWidgets.QVBoxLayout()

        self.title = QtWidgets.QLabel("Билдер клиента AES", self)
        self.title.setObjectName("title")
        self.author = QtWidgets.QLabel("Для работы нужен установленный Python. Путь к Python не должен содержать кириллицы", self)
        self.author.setObjectName("author")
        self.status = QtWidgets.QTextEdit(self)
        self.status.setText("Статус: отсутствует")
        self.status.setReadOnly(1)
        self.status.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.button = QtWidgets.QPushButton("Сгенерировать ключ и упаковать", self)

        self.l1.addWidget(self.title)
        self.l1.addWidget(self.status)
        self.l1.addWidget(self.button)
        self.l1.addWidget(self.author)

        self.click_animation = QPropertyAnimation(self.button, b"pos")
        self.click_animation.setDuration(300)

        

        self.button.clicked.connect(self.button_callback)
        

        self.widget.setLayout(self.l1)
        self.setCentralWidget(self.widget)


def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    else:
        return os.path.join(os.path.abspath("."), relative)


def main():
    app = QtWidgets.QApplication([])
    QtGui.QFontDatabase.addApplicationFont(resource_path("consola.ttf"))
    window = Window()
    window.show()
    with open(resource_path("style.css"), "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()