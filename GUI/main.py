import sys
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
from QuestionWindow import QuestionWindow
from machine import Machine
from my_lib.machine import Machine
from PDF import PDF

form_class = uic.loadUiType("mainwindow.ui")[0]
form_class2 =uic.loadUiType("coverPage.ui")[0]

class GUI(QMainWindow, form_class):

    def __init__(self):
        print("enter")
        QMainWindow.__init__(self)

        p = QtGui.QPalette()
        brush = QtGui.QBrush(QtCore.Qt.white, QtGui.QPixmap('image/background.png'))
        p.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        p.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        p.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.setPalette(p)

        self.setupUi(self)
        self.initUI()
        self.button_addMachine.clicked.connect(self.addMachine)
        self.button_trash.clicked.connect(self.deleteMachine)
        self.button_help.clicked.connect(self.showQuery)
        self.button_Execute.clicked.connect(self.sendPDF)
        self.button_backCover.clicked.connect(self.backCover)
        self.button_trash.setEnabled(False)
        self.button_Execute.setEnabled(False)
        self.label_caution.setVisible(False)
        self.listMachine = []
        self.listWidget_machine.horizontalScrollBar().setEnabled(False)

        self.sWindow=QuestionWindow()
        self.pdf=PDF()

    def initUI(self):
        self.label_openTime.setText("Factory Open Time :")
        self.label_openTime.setStyleSheet('font: 16pt ".SF NS Text"; color: "black"')

        self.label_closeTime.setText("Factory Close Time :")
        self.label_closeTime.setStyleSheet('font: 16pt ".SF NS Text";color: "black"')

        self.label_machineName.setText("Machine Name")
        self.label_machineName.setStyleSheet('font: 20 pt ".SF NS Text";color: "black"')

        self.label_durationUnit.setText("H:M")
        self.label_durationUnit.setStyleSheet('font: 20 pt ".SF NS Text";color: "black"')

        self.label_currentUnit.setText("KW/h")
        self.label_currentUnit.setStyleSheet('font: 20 pt ".SF NS Text";color: "black"')

        self.widget_7.setStyleSheet ('background-color: "white"')
        self.widget_2.setStyleSheet('background-color: "white"')

        self.label_caution.setText("﻿* Please check your input again")
        self.label_caution.setStyleSheet('color: rgb(255, 0, 10); font: 10pt ".SF NS Text";')

        self.inputDuration.setRange(0,24)
        self.time_closeTime.setRange(0,24)
        self.time_openTime.setRange(0, 24)

        self.current_pic = QPixmap('image/current.png')
        self.duration_pic = QPixmap('image/duration.png')
        self.iconCurrent.setPixmap(self.current_pic)
        self.iconDuration.setPixmap(self.duration_pic)

        self.button_addMachine.setStyleSheet('border:0px')
        addbutton_GUI= QtGui.QPixmap('image/machineButton.png')
        addbuttonPress_GUI= QtGui.QPixmap('image/machineButtonPress.png')
        self.button_addMachine.setIcon(QIcon( addbutton_GUI))
        self.button_addMachine.setIconSize(QtCore.QSize(120, 105))
        self.button_addMachine.setStyleSheet("QPushButton {background-color: transparent} QPushButton:pressed { background-color:#f36d4a}")

        self.button_Execute.setStyleSheet('border:0px')
        arrow_GUI = QtGui.QPixmap('image/arrow.png')
        self.button_Execute.setIcon(QIcon(arrow_GUI))
        self.button_Execute.setIconSize(QtCore.QSize(150, 100))
        self.button_Execute.setStyleSheet("QPushButton {background-color: transparent} QPushButton:pressed { background-color:#f36d4a}")

        trash =QtGui.QPixmap('image/trash.png')
        self.button_trash.setStyleSheet('border:0px')
        self.button_trash.setIcon(QIcon(trash))
        self.button_trash.setIconSize(QtCore.QSize(52, 52))
        self.button_trash.setStyleSheet("QPushButton {background-color: transparent} QPushButton:pressed { background-color:#f36d4a}")

        question = QtGui.QPixmap('image/question.png')
        self.button_help.setStyleSheet('border:0px')
        self.button_help.setIcon(QIcon(question))
        self.button_help.setIconSize(QtCore.QSize(20, 20))


        self.listWidget_machine.currentItemChanged.connect(self.enableTrash)
        #self.listWidget_machine.setStyleSheet("QListView:item{border:1px}")

        self.show()

    def addMachine(self):
        machineName = self.text_machineName.toPlainText()
        durationTime = self.inputDuration.value()
        currentKWh = self.inputCurrent.toPlainText()

        if machineName != "" and \
                not machineName.isspace() and \
                durationTime != 0 and durationTime <=24.00 and \
                currentKWh.isnumeric():
            self.listMachine.append(Machine(machineName, durationTime, currentKWh))
            self.label_caution.setVisible(False)
            self.displayMachine()
            self.enableExecute()
        else :
            self.label_caution.setVisible(True)

    def displayMachine(self):
        self.listWidget_machine.clear()
        if(len(self.listMachine) == 0) :
            self.button_Execute.setEnabled(False)
        for eachMachine in self.listMachine:
            self.hlayout = QHBoxLayout()
            self.machine = QLabel()
            self.machine.setFixedWidth(230)
            self.machine.setText(eachMachine.name)
            self.duration = QLabel()
            self.duration.setFixedWidth(85)
            self.duration.setText(eachMachine.get_duration_str())
            self.current = QLabel()
            self.current.setFixedWidth(145)
            self.current.setText(eachMachine.get_energy_consumption_str())

            self.hlayout.addWidget(self.machine)
            self.hlayout.addWidget(self.duration)
            self.hlayout.addWidget(self.current)

            self.hlayout.addStretch()
            self.hlayout.setSizeConstraint(QLayout.SetFixedSize)
            self.widget = QWidget()
            self.widget.setLayout(self.hlayout)
            itemN = QListWidgetItem()
            itemN.setSizeHint(self.widget.sizeHint())


            self.listWidget_machine.addItem(itemN)
            self.listWidget_machine.setItemWidget(itemN, self.widget)
            #self.listWidget_machine.setStyleSheet("QListWidget:item { border: 2px}")

    def sendPDF(self):
        self.text_machineName.setPlainText("")
        self.inputDuration.setValue(0.0)
        self.inputCurrent.setPlainText("")
        self.listWidget_machine.clear()

        if(self.time_closeTime.value()!=0 and self.time_openTime.value()!=0):
            self.pdf.createPDF()
            #!!!! save to other path
            QMessageBox.about(self,"Result","PDF File has been saved in your folder")
        else :
            QMessageBox.about(self, "Caution", "Please input the open and close time of factory")


    def showQuery(self):
        self.sWindow.createSecondWindow()

    def enableExecute(self):
        self.button_Execute.setEnabled(True)

    def enableTrash(self):
        self.button_trash.setEnabled(True)

    def deleteMachine(self):
        index = self.listWidget_machine.currentRow()
        del self.listMachine[index]
        self.displayMachine()
        self.button_trash.setEnabled(False)

    def backCover(self):
        print("enter")
        #QMainWindow.__init__(Cover())
       # self.close()

class Cover(QMainWindow,form_class2):
    def __init__(self):
        QMainWindow.__init__(self)
        p = QtGui.QPalette()
        #brush = QtGui.QBrush(QtCore.Qt.white, QtGui.QPixmap('image/coverpage.png'))
        #p.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
       # p.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
       #p.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        #self.setPalette(p)
        self.setupUi(self)

        self.initUI()

    def initUI(self):
        self.button_enterProgram.clicked.connect(self.enterMain)
        self.g = GUI()
        self.g.hide()

    def enterMain(self):

        #QMainWindow.__init__(GUI())

        self.g.show()
        print("sss")
        self.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Cover()
    w.setWindowTitle('Factory Machine Scheduler')

    app.setAttribute(QtCore.Qt.AA_DisableHighDpiScaling)

    w.show()
    app.exec_()
