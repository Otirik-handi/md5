import sys
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal, QThread
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, QWidget, QPushButton, QLineEdit)
 
from mymd5 import get_md5

class App(QMainWindow):

    exit = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.initUI()
        self.initEvent()

    def initUI(self):
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.label1 = QLabel("明文")
        self.label1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.plainbox = QLineEdit()
        self.hlayout1 = QHBoxLayout()
        self.hlayout1.addWidget(self.label1, 1)
        self.hlayout1.addWidget(self.plainbox, 3)
        
        self.label2 = QLabel("密文")
        self.label2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.cipherbox = QLineEdit()
        self.cipherbox.setReadOnly(True)
        self.hlayout2 = QHBoxLayout()
        self.hlayout2.addWidget(self.label2, 1)
        self.hlayout2.addWidget(self.cipherbox, 3)
        
        self.start_btn = QPushButton("加密")

        self.body = QVBoxLayout(self.centralWidget)
        self.body.addLayout(self.hlayout1)
        self.body.addLayout(self.hlayout2)
        self.body.addWidget(self.start_btn)

        self.centralWidget.setLayout(self.body)
        self.setGeometry(300, 300, 360, 120)
        self.setWindowTitle('MD5加密 by Otirik')
        self.center()
        self.show()

    def initEvent(self):
        self.start_btn.clicked.connect(self.calculate)


    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(self.screen().availableGeometry().center())
        self.move(qr.topLeft())
        
    def calculate(self):
        plain = self.plainbox.text()
        if len(plain) == 0:
            print("plain is empty")
        print(plain)
        cipher = get_md5(plain.encode())
        self.cipherbox.setText(cipher)


def main():

    app = QApplication(sys.argv)
    myapp = App()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()