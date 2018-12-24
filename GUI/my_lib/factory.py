from . import machine as m
from . import machine_calculator as mc
from . import my_time as mt


class Factory:

    def __init__(self, open_time=0.00, close_time=24.00):
        self.open_time = open_time
        self.close_time = close_time
        self.machine_id_map = {}
        self.machines = []

    def get_operation_time(self):
        print("Operation time")
        print(mt.distance_between_time_in_minute(self.close_time,self.open_time))
        return mt.distance_between_time_in_minute(self.close_time,self.open_time)

    def get_total_machine_work_time(self):
        print("Total machine time")
        sum = 0
        for id in self.machines:
            machine = self.machine_id_map[id]
            sum += machine.get_duration_minutes()
        print(sum)
        return sum

    def set_time(self,open_time,close_time):
        self.open_time = open_time
        self.close_time = close_time

    def add_machine(self, machine):
        self.machines.append(machine.id)
        self.machine_id_map[machine.id] = machine

    def remove_machine(self, index):
        id = self.machines[index]
        del self.machines[index]
        del self.machine_id_map[id]

    def get_machine_by_id(self, id):
        return self.machine_id_map[id]

    def get_peak_minutes(self):
        peak_time_list = [[0.00, 9.00], [9.00, 13.30], [13.30, 15.30], [15.30, 22.00], [22.00, 24.00]]
        found_open = False
        found_close = False

        for i in range(0, len(peak_time_list)):
            start_time = peak_time_list[i][0]
            end_time = peak_time_list[i][1]
            if self.open_time >= start_time and self.open_time <= end_time:
                peak_time_list[i][0] = self.open_time
                found_open = True
            if self.close_time >= start_time and self.close_time <= end_time:
                peak_time_list[i][1] = self.close_time
                found_close = True
                continue

            if not found_open:
                peak_time_list[i][0] = -1
                peak_time_list[i][1] = -1

            if found_close:
                peak_time_list[i][0] = -1
                peak_time_list[i][1] = -1

        print(peak_time_list)

        no_peak_time_1 = 0
        no_peak_time_2 = 0
        if peak_time_list[0][0] != -1:
            no_peak_time_1 = mt.distance_between_time_in_minute(peak_time_list[0][1],peak_time_list[0][0])
        if peak_time_list[4][0] != -1:
            no_peak_time_2 = mt.distance_between_time_in_minute(peak_time_list[4][1],peak_time_list[4][0])
        total_no_peak_time = no_peak_time_1 + no_peak_time_2

        peak_time_1 = 0
        peak_time_2 = 0
        if peak_time_list[1][0] != -1:
            peak_time_1 = mt.distance_between_time_in_minute(peak_time_list[1][1],peak_time_list[1][0])
        if peak_time_list[3][0] != -1:
            peak_time_2 = mt.distance_between_time_in_minute(peak_time_list[3][1],peak_time_list[3][0])
        total_peak_time = peak_time_1 + peak_time_2


        return total_no_peak_time, total_peak_time

    def get_machine_list(self):
        machine_list = [self.get_machine_by_id(id) for id in self.machines]
        return machine_list

    def get_sorted_machines_by_kwh(self):
        m_calc = mc.MachineCalculator()
        sorted_machines =  m_calc.get_sorted_machines_by_kwh(self.get_machine_list())
        return sorted_machines

    def get_sorted_machines_by_peak(self):
        # Get sorted machines first then split it
        sorted_machine_dicts = self.get_sorted_machines_by_kwh()
        sorted_machine = []
        for m_dict in sorted_machine_dicts:
            machine = self.machine_id_map[m_dict["id"]]
            sorted_machine.append(machine)

        no_peak_min, peak_min = self.get_peak_minutes()

        print(peak_min,no_peak_min)
        
        m_calc = mc.MachineCalculator()
        no_peak,peak,crit_peak = m_calc.get_sorted_machines_by_peak(sorted_machine, peak_min, no_peak_min)
       
        return (no_peak, peak, crit_peak)

    def get_time_table_list(self):
        no_peak, peak, crit_peak = self.get_sorted_machines_by_peak()

        m_calc = mc.MachineCalculator()
        time_table_list = m_calc.get_time_table(no_peak,peak,crit_peak,self.open_time)

        for machine_data in time_table_list:
            # name
            machine_data[0] = self.machine_id_map[int(machine_data[0])].name
            # duration
            machine_data[1] = int(machine_data[1])
            # kw
            machine_data[2] = float(machine_data[2])
            # start
            machine_data[3] = mt.float_to_datetime(mt.minutes_to_float(int(machine_data[3])))
            # end
            machine_data[4] = mt.float_to_datetime(mt.minutes_to_float(int(machine_data[4])))

        print(time_table_list)

        return time_table_list

    def generate_nodes(self):
        m_calc = mc.MachineCalculator("my_lib/ai.pl")
        results = m_calc.generate_nodes(self.get_machine_list(), mt.float_to_minute(self.open_time), mt.float_to_minute(self.close_time))