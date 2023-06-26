import sys
from PyQt6 import QtCore
from PyQt6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, QWidget, QPushButton, QLineEdit, QFileDialog, QMessageBox)
 
from mymd5 import *

class App(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()
        self.initEvent()
        self.filepath = None

    def initUI(self):
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.plainbox = QLineEdit()
        self.filebtn = QPushButton("选择文件")
        self.hlayout1 = QHBoxLayout()
        self.hlayout1.addWidget(self.filebtn, 1)
        self.hlayout1.addWidget(self.plainbox, 3)
        
        self.label2 = QLabel("MD5值")
        self.label2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.cipherbox = QLineEdit()
        self.cipherbox.setReadOnly(True)
        self.hlayout2 = QHBoxLayout()
        self.hlayout2.addWidget(self.label2, 1)
        self.hlayout2.addWidget(self.cipherbox, 3)
        
        
        self.label3 = QLabel("对比值")
        self.label3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.cmpbox = QLineEdit()
        self.hlayout3 = QHBoxLayout()
        self.hlayout3.addWidget(self.label3, 1)
        self.hlayout3.addWidget(self.cmpbox, 3)
        
        self.start_btn = QPushButton("计算MD5值")
        self.diffbtn = QPushButton("对比")

        self.body = QVBoxLayout(self.centralWidget)
        self.body.addLayout(self.hlayout1)
        self.body.addLayout(self.hlayout2)
        self.body.addLayout(self.hlayout3)
        self.body.addWidget(self.start_btn)
        self.body.addWidget(self.diffbtn)

        self.centralWidget.setLayout(self.body)
        self.setGeometry(300, 300, 360, 120)
        self.setWindowTitle('MD5加密 by Otirik')
        self.center()
        self.show()

    def initEvent(self):
        self.start_btn.clicked.connect(self.calculate)
        self.filebtn.clicked.connect(self.openfile)
        self.diffbtn.clicked.connect(self.compare)


    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(self.screen().availableGeometry().center())
        self.move(qr.topLeft())
        
    def calculate(self):
        if self.filepath is None:
            QMessageBox.warning(self, "警告", "请选择一个文件！",QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
        print(self.filepath)
        self.cipherbox.setText("正在计算,请稍等...")
        cipher = get_file_md5(self.filepath)
        self.cipherbox.setText(cipher)
        
    def openfile(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "选择文件", r"C://", "Any Files(*)")
        self.plainbox.setText(filepath)
        self.filepath = filepath
    
    def compare(self):
        print(self.cipherbox.text() , self.cmpbox.text())
        if self.cipherbox.text() == self.cmpbox.text():
            QMessageBox.information(self, "成功", "恭喜你的文件没有被篡改",QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.warning(self, "警告", "MD5值不正确,可能是你输入的md5值错误或者你的文件被篡改",QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)

def main():

    app = QApplication(sys.argv)
    myapp = App()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()