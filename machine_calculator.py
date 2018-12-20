from pyswip import Prolog
from machine import Machine
from factory import Factory

class MachineCalculator:

    def __init__(self, prolog_file_name="main.pl"):
        self.p = Prolog()
        self.p.consult(prolog_file_name)

    def __machines_to_List(self,machines):
        return "[" + ",".join(machines.to_fact()) + "]"

    def assert_machine(self,machine):
        self.p.assertz(machine.to_fact())

    def get_sorted_machines_by_kw(self,machines):
        machines_list = 
        
        query_str = "sort_by_kw(...)"
        a = self.p.query(query_str)
        print(list(a))

    def get_sorted_machines_by_peak(self,machines):
        query_str = "sort_by_peak(...)"
        a = self.p.query(query_str)
        print(list(a))
