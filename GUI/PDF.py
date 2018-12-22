
import sys
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
import os
import sys
import fpdf
import webbrowser
from fpdf import FPDF
class PDF():
    def __init__(self):
        self.pdf = FPDF()

    def createPDF(self):
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 10)


        data = [
                ['Machine1', '10 hr', '333', '111','444'],
                ['Machine2', '3 hr', '444', '11','3434'],
                ['Machine3', '5 hr', '4555', '2222','4r4']
                ]
        col_width = self.pdf.w / 7
        row_height = 9
        tableHeader=['Machine Name', 'Duration', 'Current', 'Start Time','End Time']
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

        self.pdf.output('file1.pdf','F')



