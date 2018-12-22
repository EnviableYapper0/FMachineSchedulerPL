from . import machine as m
from . import machine_calculator as mc


class Factory:

    def __init__(self, open_time=0, close_time=0):
        self.open_time = open_time
        self.close_time = close_time
        self.machines = []

    def add_machine(self, machine):
        self.machines.append(machine)

    def get_sorted_machines_by_kwh(self):
        m_calc = mc.MachineCalculator()
        sorted_machines =  m_calc.get_sorted_machines_by_kwh(self.machines)
        return sorted_machines

    def get_sorted_machines_by_peak(self):
        # Get sorted machines first then split it
        sorted_machines = self.get_sorted_machines_by_kwh()
        
        m_calc = mc.MachineCalculator()
        no_peak,peak,crit_peak = m_calc.get_sorted_machines_by_peak(sorted_machines)
       
        return (no_peak, peak, crit_peak)
