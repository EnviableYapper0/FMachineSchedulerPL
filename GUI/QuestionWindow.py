import sys
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *




class QuestionWindow():
    def __init__(self):
        self.questionWindow = QMainWindow()

    def createSecondWindow(self):
        self.questionWindow.setWindowTitle("Electricity Charge Table")
        self.questionWindow.setFixedSize(600, 200)
        self.voltageLabel = QLabel(self.questionWindow)
        self.voltageLabel.setGeometry(47, 10, 600, 150)
        self.voltagePicture = QPixmap('image/table.png')
        self.voltageLabel.setPixmap(self.voltagePicture)

        self.button_close = QPushButton(self.questionWindow)
        self.button_close.setGeometry(250,120,100,100)

        close = QtGui.QPixmap('image/close1.png')
        self.button_close.setStyleSheet('border:0px')
        self.button_close.setIcon(QIcon(close))
        self.button_close.setIconSize(QtCore.QSize(100, 100))
        self.button_close.clicked.connect(self.closeSecondWindow)

        self.questionWindow.show()

    def closeSecondWindow(self):
        self.questionWindow.close()