from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel
from PyQt5.QtCore import QPropertyAnimation, QPoint
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from Crypto.Util.Padding import pad, unpad
import sys, os

from Crypto.Cipher import AES


def set_default_design(field):
    field.setStyleSheet("background-color: #222222; border-radius: 10px; border-width: 0; padding: 10px; color: white;")
    

def encode(message: str, key):
    data = bytes(message, "utf-8")
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    return ciphertext.hex()


def decode(message: str, key):
    ciphertext = bytes.fromhex(message)
    
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_data.decode()


def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    else:
        return os.path.join(os.path.abspath("."), relative)
    

def set_error_animation_keys():
    pos = output_field.pos()
    x, y = pos.x(), pos.y()

    error_animation.setDuration(150)
    error_animation.setLoopCount(2)
    error_animation.setKeyValueAt(0, QPoint(x, y))
    error_animation.setKeyValueAt(0.09, QPoint(x + 2, y))
    error_animation.setKeyValueAt(0.18, QPoint(x + 4, y))
    error_animation.setKeyValueAt(0.27, QPoint(x + 2, y))
    error_animation.setKeyValueAt(0.36, QPoint(x + 0, y))
    error_animation.setKeyValueAt(0.45, QPoint(x - 2, y))
    error_animation.setKeyValueAt(0.54, QPoint(x - 4, y))
    error_animation.setKeyValueAt(0.63, QPoint(x - 6, y))
    error_animation.setKeyValueAt(0.72, QPoint(x - 8, y))
    error_animation.setKeyValueAt(0.81, QPoint(x - 6, y))
    error_animation.setKeyValueAt(0.90, QPoint(x - 4, y))
    error_animation.setKeyValueAt(0.99, QPoint(x - 2, y))
    error_animation.setEndValue(QPoint(x, y))


def set_success_animation_keys():
    pos = output_field.pos()
    x, y = pos.x(), pos.y()

    success_animation.setDuration(100)
    success_animation.setKeyValueAt(0, QPoint(x, y))
    success_animation.setKeyValueAt(0.09, QPoint(x, y - 5))
    success_animation.setEndValue(QPoint(x, y))


def error(text):
    output_field.setText(text)
    output_field.setStyleSheet("background-color: #ff0000; border-radius: 10px; border-width: 0; padding: 10px 10px; color: white;")
    
    set_error_animation_keys()
    error_animation.start()
    

with open(resource_path("key.txt"), "rb") as f:
    key = f.read()

font = QFont("Consolas", 15)
app = QApplication([])
widget = QWidget()
widget.resize(600, 400)
widget.setWindowTitle("Шифровальщик AES")
widget.setStyleSheet("background-color: #111111;")
widget.setWindowIcon(QIcon(resource_path("logo.png")))

l1 = QVBoxLayout()
l2 = QHBoxLayout()

title = QLabel(text="Шифровальщик AES")
title.setStyleSheet("color: white;")
title.setFont(QFont("Consolas", pointSize=30, italic=True))


encode_btn = QPushButton(text="Кодировать")
encode_btn.setStyleSheet("color: white; background-color: #0064FF; border-radius: 10px; border-width: 0; height: 30px; margin-right: 5px;")
encode_btn.setFont(font)
decode_btn = QPushButton(text="Декодировать")
decode_btn.setStyleSheet("color: white; background-color: #0064FF; border-radius: 10px; border-width: 0; height: 30px;")
decode_btn.setFont(font)
input_field = QTextEdit()
input_field.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
input_field.setFont(font)
input_field.setText("Введите ваше секретное сообщение сюда...")
input_field.setStyleSheet("background-color: #222222; border-radius: 10px; border-width: 0; padding: 10px; color: white;")
output_field = QTextEdit()
output_field.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
output_field.setFont(font)
output_field.setText(encode("Введите ваше секретное сообщение сюда...", key))
set_default_design(input_field)
set_default_design(output_field)
output_field.setReadOnly(1)



l2.addWidget(encode_btn)
l2.addWidget(decode_btn)

l1.addWidget(title)
l1.addWidget(input_field)
l1.addWidget(output_field)
l1.addItem(l2)
widget.setLayout(l1)

success_animation = QPropertyAnimation(output_field, b"pos")
error_animation = QPropertyAnimation(output_field, b"pos")


def encode_callback():
    
    text = input_field.toPlainText()
    encoded = encode(text, key)
    set_default_design(output_field)
    output_field.setText(encoded)
    set_success_animation_keys()
    success_animation.start()

encode_btn.clicked.connect(encode_callback)


def decode_callback():
    text = input_field.toPlainText()

    try:
        decoded = decode(text, key)
        set_default_design(output_field)
        output_field.setText(decoded)
        set_success_animation_keys()
        success_animation.start()
    except ValueError:
        error("Ошибка: сообщение не является зашифрованным текстом")

decode_btn.clicked.connect(decode_callback)


widget.show()
sys.exit(app.exec_())