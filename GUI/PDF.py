
import sys
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
import os
import sys
import fpdf
import webbrowser
from fpdf import FPDF
from datetime import datetime


class PDF():
    def __init__(self):
        self.pdf=FPDF()

    def convert_to_data(self, time_table):
        data = []

        for schedule in time_table:
            name = schedule[0]
            duration = str(schedule[1]) + " minutes"
            kwh = str(schedule[2]) + " kW"
            start_time = schedule[3]
            end_time = schedule[4]
            if schedule[1] != 0:
                data.append([name,duration,kwh,start_time,end_time])

        print("Data:")
        print(data)

        return data



    def createPDF(self, time_table_list, factory):
        self.date_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 10)

        data = self.convert_to_data(time_table_list)
        col_width = self.pdf.w / 7
        row_height = 9
        tableHeader=['Machine Name', 'Duration', 'Energy', 'Start Time','End Time']
        self.pdf.set_x(15)

        self.pdf.set_text_color(r=0, g=0, b=0)
        self.pdf.set_fill_color(r=255, g=191, b=0)
        for i in range (0,5):
            if i==0:
                self.pdf.cell(col_width+30, row_height,txt=tableHeader[i], border=1,align='C',fill=1)
            else :
                self.pdf.cell(col_width , row_height, txt=tableHeader[i], border=1,align='C',fill=1)
        self.pdf.ln(row_height)

        self.pdf.set_x(15)
        self.pdf.set_text_color(r=0, g=0, b=0)
        self.pdf.set_font('Arial', 'B', 8)
        for row in data:
            count=0
            for item in row:
                if(count==0 ):
                    self.pdf.cell(col_width+30, row_height,txt=item, border=1)
                    count=1
                else:
                    self.pdf.cell(col_width, row_height,txt=item, border=1)
            self.pdf.ln(row_height)
            self.pdf.set_x(15)
        self.filename = 'schedule'+self.date_time+'.pdf'
        print(self.filename)
        self.pdf.output(self.filename,'F')



