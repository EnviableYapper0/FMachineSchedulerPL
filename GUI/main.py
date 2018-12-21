import sys
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
from machine import Machine

form_class = uic.loadUiType("mainwindow.ui")[0]


class GUI(QMainWindow, form_class):

    def __init__(self):
        QMainWindow.__init__(self)

        #p = QtGui.QPalette()
        #brush = QtGui.QBrush(QtCore.Qt.white, QtGui.QPixmap('image/background.jpg'))
        #p.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        #p.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        #p.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        #self.setPalette(p)

        self.setupUi(self)
        self.initUI()
        self.button_addMachine.clicked.connect(self.addMachine)
        self.listMachine = []


    def initUI(self):
        self.current_pic = QPixmap('image/current.png')
        self.duration_pic = QPixmap('image/duration.png')
        self.iconCurrent.setPixmap(self.current_pic)
        self.iconDuration.setPixmap(self.duration_pic)

        self.button_addMachine.setStyleSheet('border:0px')
        addbutton_GUI= QtGui.QPixmap('image/machineButton.png')
        self.button_addMachine.setIcon(QIcon( addbutton_GUI))
        self.button_addMachine.setIconSize(QtCore.QSize(120, 105))

        self.button_Execute.setStyleSheet('border:0px')
        arrow_GUI = QtGui.QPixmap('image/arrow.jpg')
        self.button_Execute.setIcon(QIcon(arrow_GUI))
        self.button_Execute.setIconSize(QtCore.QSize(125, 110))
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
            self.displayMachine()

    def displayMachine(self):
        self.listWidget_machine.clear()
        self.count=0
        for eachMachine in self.listMachine:
            self.hlayout = QHBoxLayout()
            self.machine = QLabel()
            self.machine.setFixedWidth(170)
            self.machine.setText(eachMachine.name)
            self.duration = QLabel()
            self.duration.setFixedWidth(70)
            self.duration.setText(eachMachine.get_duration_str())
            self.current = QLabel()
            self.current.setFixedWidth(130)
            self.current.setText(eachMachine.get_energy_consumption_str())
            deleteButton= QPushButton(self)
            deleteButton.setStyleSheet('border:0px')
            deleteIcon = QtGui.QPixmap('image/trash.png');
            deleteButton.setIcon(QIcon(deleteIcon))
            deleteButton.setIconSize(QtCore.QSize(25, 25))
            deleteButton.clicked.connect(self.deleteMachine)

            self.hlayout.addWidget(self.machine)
            self.hlayout.addWidget(self.duration)
            self.hlayout.addWidget(self.current)
            self.hlayout.addWidget(deleteButton)

            self.hlayout.addStretch()
            self.hlayout.setSizeConstraint(QLayout.SetFixedSize)
            self.widget = QWidget()
            self.widget.setLayout(self.hlayout)
            itemN = QListWidgetItem()
            itemN.setSizeHint(self.widget.sizeHint())

            self.listWidget_machine.addItem(itemN)
            self.listWidget_machine.setItemWidget(itemN, self.widget)
            self.count += 1

    def deleteMachine(self):
        index = self.listWidget_machine.currentRow()
        del self.listMachine[index]
        self.displayMachine()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = GUI()
    w.setWindowTitle('Factory Machine Scheduler')

    app.setAttribute(QtCore.Qt.AA_DisableHighDpiScaling)

    print("Launch GUI")
    w.show()
    app.exec_()
