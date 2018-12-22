from pyswip import Prolog
from . import machine
from . import factory


class MachineCalculator:

    def __init__(self, prolog_file_name="my_lib/main.pl"):
        self.p = Prolog()
        self.p.consult(prolog_file_name)

    def readable_results(self, results, variable):
        readable = list(results)[0][variable]
        all = []
        for r in readable:
            all.append(str(r))
        return all

    def machines_to_List(self, machines):
        # convert list of machines obj to List in Prolog
        fact_str = "[" + ",".join(m.to_fact() for m in machines) + "]"
        return fact_str

    def assert_machine(self, machine):
        # assert a machine fact
        self.p.assertz(machine.to_fact())

    def get_sorted_machines_by_kwh(self, machines):
        # get list of machines that is sorted by kwh
        machines_str = self.machines_to_List(machines)
        result_var = "X"
        print(machines_str)
        query_str = "machine_sort(" + machines_str + "," + result_var + ")"
        a = self.p.query(query_str)
        results = self.readable_results(a,result_var)
        return results

    def get_sorted_machines_by_peak(self, machines):
        query_str = "sort_by_peak(...)"
        a = self.p.query(query_str)
        print(list(a))
