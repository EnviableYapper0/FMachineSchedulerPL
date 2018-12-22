from . import machine as m
from . import machine_calculator as mc
from . import my_time as mt


class Factory:

    def __init__(self, open_time=0.00, close_time=24.00):
        self.open_time = open_time
        self.close_time = close_time
        self.machine_id_map = {}
        self.machines = []

        self.no_peak_1 = [0.00, 8.59]
        self.peak_1 = [9.00, 13.29]
        self.crit_peak = [13.30, 15.29]
        self.peak_2 = [15.30, 21.59]
        self.no_peak_2 = [22.00, 23.59]

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

    def get_no_peak_minutes(self):
        part_1 = 0
        part_2 = 0

        # case in no_peak_1
        if (self.open_time <= self.no_peak_1[1] and self.close_time <= self.no_peak_1[1]):
            part_1 = mt.distance_between_time_in_minute(self.close_time, self.open_time)
            part_2 = 0
        # case in no_peak_2
        elif (self.open_time >= self.no_peak_2[0] and self.close_time >= self.no_peak_2[0]):
            part_1 = 0
            part_2 = mt.distance_between_time_in_minute(self.close_time, self.open_time)
        # case overlap no_peak_1 and no_peak_2
        elif (self.open_time <= self.no_peak_1[1] and self.close_time >= self.no_peak_2[0]):
            part_1 = mt.distance_between_time_in_minute(self.no_peak_1[1],self.open_time) + 1
            part_2 = mt.distance_between_time_in_minute(self.close_time,self.no_peak_2[0]) + 1
        # case overlap no_peak_1 and before no_peak_2
        elif (self.open_time <= self.no_peak_1[1] and self.close_time <= self.no_peak_2[0]):
            part_1 = mt.distance_between_time_in_minute(self.no_peak_1[1],self.open_time)
            part_2 = 0
        # case before no_peak_2 and in no_peak_2
        elif (self.open_time <= self.no_peak_2[0] and self.close_time >= self.no_peak_2[1]):
            part_1 = 0
            part_2 = mt.distance_between_time_in_minute(self.no_peak_2[0],self.close_time)

        print("No Peak: ", part_1 + part_2)

        return part_1 + part_2

    def get_peak_minutes(self):
        part_1 = 0
        part_2 = 0

        # case before peak_1 and in peak_1
        if (self.open_time <= self.peak_1[0] and self.close_time >= self.peak_1[0] and self.close_time <= self.peak_1[1]):
            print("# case before peak_1 and in peak_1")
            part_1 = mt.distance_between_time_in_minute(self.peak_1[0],self.close_time)
            part_2 = 0
        # case in peak_1 only
        if (self.open_time >= self.peak_1[0] and self.close_time <= self.peak_1[1]):
            print("# case in peak_1 only")
            part_1 = mt.distance_between_time_in_minute(self.close_time, self.open_time)
            part_2 = 0
        # case in peak_2 only
        elif (self.open_time >= self.peak_2[0] and self.close_time <= self.peak_2[1]):
            print("# case in peak_2 only")
            part_1 = 0
            part_2 = mt.distance_between_time_in_minute(self.close_time, self.open_time)
        # case before peak_1 and in peak_2
        elif (self.open_time <= self.peak_1[0] and self.close_time >= self.peak_2[0] and self.close_time <= self.peak_2[1]):
            print("# case before peak_1 and in peak_2")
            part_1 = mt.distance_between_time_in_minute(self.peak_1[1], self.peak_1[0]) + 1
            part_2 = mt.distance_between_time_in_minute(self.peak_2[0], self.close_time)
        # case before peak_1 and before peak_2
        elif (self.open_time <= self.peak_1[0] and self.close_time >= self.peak_1[1] and self.close_time <= self.peak_2[0]):
            print("# case before peak_1 and before peak_2")
            part_1 = mt.distance_between_time_in_minute(self.peak_1[1], self.peak_1[0]) + 1
            part_2 = 0
        # case before peak_1 and after peak_2
        elif (self.open_time <= self.peak_1[0] and self.close_time >= self.peak_2[1]):
            print("# case before peak_1 and after peak_2")
            part_1 = mt.distance_between_time_in_minute(self.peak_1[1], self.peak_1[0]) + 1
            part_2 = mt.distance_between_time_in_minute(self.peak_2[1], self.peak_2[0]) + 1
        # case after peak_1 and in peak_2
        elif (self.open_time >= self.peak_1[1] and self.close_time >= self.peak_2[0] and self.close_time <= self.peak_2[1]):
            print("# case after peak_1 and in peak_2")
            part_1 = 0
            part_2 = mt.distance_between_time_in_minute(self.peak_2[1], self.close_time)
        # case after peak_1 and after peak_2
        elif(self.open_time >= self.peak_1[1] and self.close_time >= self.peak_2[1]):
            print("# case after peak_1 and after peak_2")
            part_1 = 0
            part_2 = mt.distance_between_time_in_minute(self.peak_2[1],self.peak_2[0]) + 1
        # case before peak_2 and in peak_2
        elif(self.open_time <= self.peak_2[0] and self.close_time >= self.peak_2[0] and self.close_time <= self.peak_2[1]):
            print("# case before peak_2 and in peak_2")
            part_1 = 0
            part_2 = mt.distance_between_time_in_minute(self.close_time,self.peak_2[0])

        print("Peak: ", part_1 + part_2)

        return part_1 + part_2

    def get_crit_peak_minutes(self):
        return self.crit_peak[1] - self.crit_peak[0]

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

        peak_min = self.get_peak_minutes()
        no_peak_min = self.get_no_peak_minutes()

        print(peak_min,no_peak_min)
        
        m_calc = mc.MachineCalculator()
        no_peak,peak,crit_peak = m_calc.get_sorted_machines_by_peak(sorted_machine, peak_min, no_peak_min)
       
        return (no_peak, peak, crit_peak)
