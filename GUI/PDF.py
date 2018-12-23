
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

    def convert_to_data(self, no_peak, peak, crit_peak, factory):
        data = []

        open_time = factory.open_time
        close_time = factory.close_time

        peak_time_list = [[0.00, 9.00],[9.00, 13.30],[13.30, 15.30],[15.30, 22.00],[22.00, 24.00]]
        found_open = False
        found_close = False

        for i in range(0,len(peak_time_list)):
            start_time = peak_time_list[i][0]
            end_time = peak_time_list[i][1]
            if open_time >= start_time and open_time <= end_time:
                peak_time_list[i][0] = open_time
                found_open = True
            if close_time >= start_time and close_time <= end_time:
                peak_time_list[i][1] = close_time
                found_close = True
                continue

            if not found_open:
                peak_time_list[i][0] = -1
                peak_time_list[i][1] = -1

            if found_close:
                peak_time_list[i][0] = -1
                peak_time_list[i][1] = -1

        print(peak_time_list)

        curr_time = open_time

        no_peak_1_duration = 0
        peak_1_duration = 0
        crit_peak_duration = 0
        peak_2_duration = 0
        no_peak_2_duration = 0

        # if peak_time_list[0][0] != -1:
        #     no_peak_1_duration = distance_between_time_in_minute(peak_time_list[0][1],peak_time_list[0][0])
        # if peak_time_list[1][0] != -1:
        #     peak_1_duration = distance_between_time_in_minute(peak_time_list[1][1], peak_time_list[1][0])
        # if peak_time_list[2][0] != -1:
        #     crit_peak_duration = distance_between_time_in_minute(peak_time_list[2][1], peak_time_list[2][0])
        # if peak_time_list[3][0] != -1:
        #     peak_2_duration = distance_between_time_in_minute(peak_time_list[3][1], peak_time_list[3][0])
        # if peak_time_list[4][0] != -1:
        #     no_peak_2_duration = distance_between_time_in_minute(peak_time_list[4][1], peak_time_list[4][0])

        while no_peak_1_duration > 0:
            pass
        while peak_1_duration > 0:
            pass
        while crit_peak_duration > 0:
            pass
        while peak_2_duration > 0:
            pass
        while no_peak_2_duration > 0:
            pass


    def createPDF(self, time_table_list, factory):
        self.date_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 10)

        # self.convert_to_data(no_peak,peak,crit_peak,factory)
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
        self.filename = 'schedule'+self.date_time+'.pdf'
        print(self.filename)
        self.pdf.output(self.filename,'F')



