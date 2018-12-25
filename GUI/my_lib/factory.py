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

    def get_machine_list(self):
        machine_list = [self.get_machine_by_id(id) for id in self.machines]
        return machine_list

    def generate_nodes(self):
        m_calc = mc.MachineCalculator("my_lib/ai.pl")
        results = m_calc.generate_nodes(self.get_machine_list(), mt.float_to_minute(self.open_time), mt.float_to_minute(self.close_time))
        return results