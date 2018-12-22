from pyswip import Prolog
from . import machine
from . import factory


class MachineCalculator:

    def __init__(self, prolog_file_name="my_lib/main.pl"):
        self.p = Prolog()
        self.p.consult(prolog_file_name)

    def convert_machine_to_dict(self,machine_functor):
        m_list = machine_functor.replace("machine(","").replace(")","").replace(" ","").split(",")
        m_dict = {"id": int(m_list[0]), "duration": float(m_list[1]), "energy_consumption": float(m_list[2])}
        print(m_dict)
        return m_dict


    def readable_results(self, results, variable):
        readable = list(results)[0][variable]
        all = []
        for r in readable:
            machine_dict  = self.convert_machine_to_dict(str(r))
            all.append(machine_dict)
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
        query_str = "machine_sort(" + machines_str + "," + result_var + ")"
        a = self.p.query(query_str)
        results = self.readable_results(a,result_var)
        return results

    def get_sorted_machines_by_peak(self, machines):
        machines_str = self.machines_to_List(machines)
        print(machines_str)
        no_peak_var = "NP"
        peak_var = "P"
        crit_peak_var = "CP"
        # print("Query string:")
        query_str = "classify_machine(" + machines_str + "," + "180,240," + no_peak_var + "," + peak_var + "," + crit_peak_var + ")"
        # print(query_str)
        # classify_machine(List, NonPeakLength, PeakLength, NonPeakList, PeakList, CritialPeakList)
        a = self.p.query(query_str)
        results = list(a)[0]
        no_peak = results[no_peak_var]
        peak = results[peak_var]
        crit_peak = results[crit_peak_var]
        print(no_peak)
        print(peak)
        print(crit_peak)
        # print("no_peak:")
        # no_peak_dict = self.readable_results(a,no_peak_var)
        # print("peak")
        # peak_dict = self.readable_results(a, peak_var)
        # print("crit_peak")
        # crit_peak_dict = self.readable_results(a, crit_peak_var)
        # print(list(a))
