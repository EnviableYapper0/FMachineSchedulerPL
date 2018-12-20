from . import machine
from . import machine_calculator


class Factory:

    def __init__(self, open_time=0, close_time=0):
        self.open_time = open_time
        self.close_time = close_time
        self.machines = []

    def add_machine(self, machine):
        self.machines.append(machine)

    def get_sorted_machines_by_kw(self):
        m_calc = MachineCalculator()
        sorted_machines =  m_calc.get_sorted_machines_by_kw(self.machines)
        return sorted_machines

    def get_sorted_machines_by_peak(self):
        # Get sorted machines first then split it
        sorted_machines = self.get_sorted_machines_by_kw()
        
        m_calc = MachineCalculator()
        no_peak,peak,crit_peak = m_calc.get_sorted_machines_by_peak(sorted_machines)
       
        return (no_peak, peak, crit_peak)
