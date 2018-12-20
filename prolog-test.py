from pyswip import Prolog

class MachineCalculator:

    def __init__(self, prolog_file_name):
        self.p = Prolog()
        self.p.consult(prolog_file_name)

    def add_machine(self,name,kwh,duration):
        machine = [name,kwh,duration]
        machine_fact = "machine(" + \
                ",".join(str(s) for s in machine) + ")"
        self.p.assertz(machine_fact)

    def get_sorted_machines_by_kw(self):
        query_str = "sort_by_kw(...)"
        a = self.p.query(query_str)
        print(list(a))

    def get_sorted_machines_by_peak(self):
        query_str = "sort_by_peak(...)"
        a = self.p.query(query_str)
        print(list(a))
