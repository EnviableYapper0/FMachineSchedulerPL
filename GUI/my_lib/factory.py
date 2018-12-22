from . import machine as m
from . import machine_calculator as mc


class Factory:

    def __init__(self, open_time=0, close_time=0):
        self.open_time = open_time
        self.close_time = close_time
        self.machine_id_map = {}
        self.machines = []

    def set_time(self,open_time,close_time):
        self.open_time = open_time
        self.close_time = close_time

    def add_machine(self, machine):
        self.machines.append(machine.id)
        self.machine_id_map[machine.id] = machine

    def remove_machine(self, id):
        pass

    def get_machine_by_id(self, id):
        return self.machine_id_map[id]

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
        
        m_calc = mc.MachineCalculator()
        no_peak,peak,crit_peak = m_calc.get_sorted_machines_by_peak(sorted_machine)
       
        return (no_peak, peak, crit_peak)
