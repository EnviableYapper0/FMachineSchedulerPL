from fpdf import FPDF
from datetime import datetime
from my_lib.my_time import float_to_datetime
from my_lib.my_time import minutes_to_float


class PDF():

    def convert_to_data(self, time_table):
        data = []

        for schedule in time_table:
            machine = schedule[0][1]
            start_minutes = schedule[0][2]
            end_minutes = schedule[0][3]
            start_time = float_to_datetime(minutes_to_float(start_minutes))
            end_time = float_to_datetime(minutes_to_float(end_minutes))
            data.append([machine.name, machine.get_duration_str(), machine.get_energy_consumption_str(), start_time, end_time])

        return data

    def createPDF(self, time_table_list, factory):
        self.pdf=FPDF()
        self.date_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 10)

        data = self.convert_to_data(time_table_list)
        print("Data:")
        print(data)
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