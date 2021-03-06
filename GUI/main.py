import sys
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
from QuestionWindow import QuestionWindow
# from machine import Machine
from my_lib.machine import Machine
from my_lib.factory import Factory
from PDF import PDF
from Storage import Storage

form_class = uic.loadUiType("mainwindow.ui")[0]
form_class2 =uic.loadUiType("coverPage.ui")[0]

class GUI(QMainWindow, form_class):

    def __init__(self):

        QMainWindow.__init__(self)
        self.setFixedSize(860,600)
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
        self.button_Execute.clicked.connect(self.calculateValue)
        self.button_trash.setEnabled(False)
        self.button_Execute.setEnabled(False)
        self.label_caution.setVisible(False)
        self.listWidget_machine.horizontalScrollBar().setEnabled(False)

        self.factory = Factory()

        self.sWindow=QuestionWindow()
        self.pdf=PDF()

        self.storage=Storage()
        self.display_initial_Machine()


    def initUI(self):
        self.label_openTime.setText("Factory Open Time :")
        self.label_openTime.setStyleSheet('font: 15pt ".SF NS Text"; color: "black"')

        self.label_closeTime.setText("Factory Close Time :")
        self.label_closeTime.setStyleSheet('font: 15pt ".SF NS Text";color: "black"')

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

        self.inputDuration.setRange(0,23.59)
        self.time_closeTime.setRange(0,23.59)
        self.time_openTime.setRange(0, 23.59)

        self.current_pic = QPixmap('image/current.png')
        self.duration_pic = QPixmap('image/duration.png')
        self.iconCurrent.setPixmap(self.current_pic)
        self.iconDuration.setPixmap(self.duration_pic)

        self.button_addMachine.setStyleSheet('border:0px')
        addbutton_GUI= QtGui.QPixmap('image/machineButton.png')
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
        self.show()

    def addMachine(self):
        machineName = self.text_machineName.toPlainText()
        durationTime = self.inputDuration.value()
        currentKWh = self.inputCurrent.toPlainText()
        self.checkDuplicate= 0

        if machineName != "" and \
                not machineName.isspace() and \
                durationTime != 0 and durationTime <=24.00 and \
                currentKWh.isnumeric() and currentKWh != "0" :
            for machine in self.factory.get_machine_list():
                if machine.name == machineName:
                    self.label_caution.setText("﻿*This machine already exists")
                    self.label_caution.setVisible(True)
                    self.checkDuplicate=1
                    return
            if(self.checkDuplicate==0):
                self.factory.add_machine(Machine(machineName, durationTime, currentKWh))
                self.label_caution.setVisible(False)
                self.storage.saveTime(self.time_openTime.value(),self.time_closeTime.value())
                self.storage.save(self.factory.get_machine_list())
                self.displayMachine()
                self.enableExecute()

        else :
            self.label_caution.setText("﻿* Please check your input again")
            self.label_caution.setVisible(True)

    def displayMachine(self):
        self.listWidget_machine.clear()
        if(len(self.factory.machines) == 0) :
            self.disableExecute()
        else:
            self.enableExecute()
        for machine_id in self.factory.machines:
            eachMachine = self.factory.get_machine_by_id(machine_id)
            self.hlayout = QHBoxLayout()
            self.machine_image= QLabel()
            self.image=QPixmap("image/machine.png");
            self.machine_image.setPixmap(self.image);
            self.machine = QLabel()
            self.machine.setFixedWidth(190)
            self.machine.setText(eachMachine.name)
            self.duration = QLabel()
            self.duration.setFixedWidth(85)
            self.duration.setText(eachMachine.get_duration_str())
            self.current = QLabel()
            self.current.setFixedWidth(145)
            self.current.setText(eachMachine.get_energy_consumption_str())

            self.hlayout.addWidget(self.machine_image)
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
    def display_factory_time(self):
        self.timeFile = self.storage.readTime()
        count_t = 1
        for each_time in self.timeFile:
            self.getTime = ''.join(each_time.split())
            if (count_t == 1):
                if len(each_time) != 0:
                    self.time_openTime.setValue(float(self.getTime))
                else:
                    pass
                count_t += 1
            else:
                self.time_closeTime.setValue(float(self.getTime))

    def display_initial_Machine(self):
        self.display_factory_time()

        self.all_file=self.storage.read()
        self.listWidget_machine.clear()
        self.factory.get_machine_list().clear()
        round=1
        if(len(self.all_file)!=0):
            self.enableExecute()
        for each_file in self.all_file:
            if(round==1):
                self.temp_machine = ''.join(each_file.split())
            elif (round == 2):
                self.temp_duration = ''.join(each_file.split())
            elif (round == 3):
                self.temp_current = ''.join(each_file.split())
                self.factory.add_machine(Machine(self.temp_machine,self.temp_duration,self.temp_current))
                round=0
            round+=1
        self.displayMachine()



    def set_factory_time(self):
        self.factory.set_time(float(self.time_openTime.value()), float(self.time_closeTime.value()))

    def calculateValue(self):
        self.text_machineName.setPlainText("")
        self.inputDuration.setValue(0.0)
        self.inputCurrent.setPlainText("")
        self.set_factory_time()
        time_table_list = self.factory.get_time_table_list()
        self.factory.generate_nodes()

        self.sendPDF(time_table_list)

    def sendPDF(self, time_table_list):
        self.close_time = float(self.time_closeTime.value())
        self.open_time = float(self.time_openTime.value())

        print("open",self.open_time, "close", self.close_time)

        if ( self.factory.get_operation_time() <= self.factory.get_total_machine_work_time()):
            QMessageBox.warning(self, "Caution", "Factory operation time must be more then total of machine work time")
        elif (self.open_time >= self.close_time):
            QMessageBox.warning(self, "Caution", "Factory close time must be more than the open time")
        elif(self.time_closeTime.value()!=0 and self.time_openTime.value()!=0 and  self.open_time < self.close_time):
            self.storage.saveTime(self.time_openTime.value(), self.time_closeTime.value())
            self.factory.set_time(self.open_time, self.close_time)
            # self.pdf.createPDF(time_table_list, self.factory)
            QMessageBox.information(self,"Result","PDF File has been saved in your folder")
        else :
            QMessageBox.warning(self, "Caution", "Please input the open and close time of factory")


    def showQuery(self):
        self.sWindow.createSecondWindow()

    def enableExecute(self):
        self.button_Execute.setEnabled(True)

    def disableExecute(self):
        self.button_Execute.setEnabled(False)

    def enableTrash(self):
        self.button_trash.setEnabled(True)

    def deleteMachine(self):
        index = self.listWidget_machine.currentRow()
        self.factory.remove_machine(index)
        self.storage.save(self.factory.get_machine_list())
        self.storage.saveTime(self.time_openTime.value(), self.time_closeTime.value())
        self.displayMachine()
        self.button_trash.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = GUI()
    w.setWindowTitle('Factory Machine Scheduler')
    w.setFixedSize(860,600)


    app.setAttribute(QtCore.Qt.AA_DisableHighDpiScaling)

    w.show()
    app.exec_()
