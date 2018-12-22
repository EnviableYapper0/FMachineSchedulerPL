import sys
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *




class QuestionWindow():
    def __init__(self):
        self.questionWindow = QMainWindow()

    def createSecondWindow(self):
        self.questionWindow.setWindowTitle("Electricity Charge Table")
        self.questionWindow.setFixedSize(600, 400)
        self.voltageLabel = QLabel(self.questionWindow)
        self.voltageLabel.setGeometry(98, 6, 600, 150)
        self.voltagePicture = QPixmap('image/table.png')
        self.voltageLabel.setPixmap(self.voltagePicture)

        self.graph_label = QLabel(self.questionWindow)
        self.graph_label.setGeometry(98, 145, 600, 170)
        self.graphPicture = QPixmap('image/graph.png')
        self.graph_label.setPixmap(self.graphPicture)

        self.button_close = QPushButton(self.questionWindow)
        self.button_close.setGeometry(250,300,100,100)

        close = QtGui.QPixmap('image/close1.png')
        self.button_close.setStyleSheet('border:0px')
        self.button_close.setIcon(QIcon(close))
        self.button_close.setIconSize(QtCore.QSize(100, 100))
        self.button_close.clicked.connect(self.closeSecondWindow)

        self.questionWindow.show()

    def closeSecondWindow(self):
        self.questionWindow.close()