import sys
from PyQt5 import QtCore, QtGui, uic, QtWebEngineWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *

form_class = uic.loadUiType("mainwindow.ui")[0]


class GUI(QMainWindow, form_class):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.initUI()
        self.button_addMachine.clicked.connect(self.addMachine)


    def initUI(self):
        self.current_pic = QPixmap('venv/image/current.png')
        self.duration_pic = QPixmap('venv/image/duration.png')
       # self.arl_icon.addPixmap(QtGui.QPixmap('ui_asset/arl.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.iconCurrent.setPixmap(self.current_pic)
        self.iconDuration.setPixmap(self.duration_pic)
        self.show()

    def addMachine(self):
        self.machineName = self.text_machineName.toPlainText()
        self.durationTime = self.inputDuration.value()
        self.currentKWh = self.inputCurrent.value()
        if(self.machineName.isalnum() and self.durationTime != 0 and self.currentKWh != 0):
            groupWidget = QListWidget()
            #self.listWidget_machine.setText()
           # QListWidgetItem((self.machineName+ "   " + str(self.duration)+ " Hr.   " +str(self.current)+" KW/h"), self.listWidget_machine)
            self.hlayout = QHBoxLayout()
            self.machine = QLabel()
            self.machine.setText(self.machineName)
            self.duration = QLabel()
            self.duration.setText(str(self.durationTime))
            self.current = QLabel()
            self.current.setText(str(self.currentKWh))
            self.hlayout.addWidget(self.machine)
            self.hlayout.addWidget(self.duration)
            self.hlayout.addWidget(self.current)
            self.hlayout.addStretch()
            self.hlayout.setSizeConstraint(QLayout.SetFixedSize)
            self.widget= QWidget()
            self.widget.setLayout(self.hlayout)
            itemN = QListWidgetItem()
            itemN.setSizeHint(self.widget.sizeHint())

            self.listWidget_machine.addItem(itemN)
            self.listWidget_machine.setItemWidget(itemN, self.widget)







def launch():
    app = QApplication(sys.argv)
    w = GUI()
    w.setWindowTitle('Factory Machine Scheduler')

    app.setAttribute(QtCore.Qt.AA_DisableHighDpiScaling)

    print("Launch GUI")
    w.show()
    app.exec_()


launch()