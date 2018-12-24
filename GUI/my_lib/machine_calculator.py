from pyswip import Prolog
from . import machine
from . import factory
from . import my_time as mt
from collections import defaultdict
import uuid

PEAK_START = 540
CRITICAL_PEAK_START = 810
CRITICAL_PEAK_END = 930
PEAK_END = 1320

minute_cost_table = ([1] * PEAK_START) + ([2] * (CRITICAL_PEAK_START - PEAK_START)) + ([3] * (CRITICAL_PEAK_END - CRITICAL_PEAK_START)) + ([2] * (PEAK_END - CRITICAL_PEAK_END)) + ([1] * (1440 - PEAK_END))
class MachineCalculator:

    def __init__(self, prolog_file_name="my_lib/main.pl"):
        self.p = Prolog()
        self.p.consult(prolog_file_name)

        self.uuid_map = defaultdict(list)

    def convert_machine_to_dict(self,machine_functor):
        m_list = machine_functor.replace("machine(","").replace(")","").replace(" ","").split(",")
        m_dict = {"id": int(m_list[0]), "duration": float(m_list[1]), "energy_consumption": float(m_list[2])}

        return m_dict

    def readable_results(self, results):
        all = []
        for r in results:
            machine_dict  = self.convert_machine_to_dict(str(r))
            all.append(machine_dict)
        return all

    def readable_results_list(self, results):
        all = []
        for r in results:
            all.append(str(r))
        return all

    def readable_time_table_list(self, unread_time_table):
        all = []
        for r in unread_time_table:
            m_data_list = str(r).replace("sorted_machine(","").replace(")","").replace(" ","").split(",")
            all.append(m_data_list)
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
        results = list(a)[0][result_var]
        readable_results = self.readable_results(results)

        return readable_results

    def get_sorted_machines_by_peak(self, machines, peak_length, no_peak_length):
        machines_str = self.machines_to_List(machines)
        print("Machines:")
        print(machines_str)
        no_peak_var = "NP"
        peak_var = "P"
        crit_peak_var = "CP"

        # classify_machine(List, NonPeakLength, PeakLength, NonPeakList, PeakList, CritialPeakList)
        query_str = "classify_machine(" + machines_str + "," + str(no_peak_length) + "," + str(peak_length)\
                    + "," + no_peak_var + "," + peak_var + "," + crit_peak_var + ")"
        print(query_str)
        a = self.p.query(query_str)

        results = list(a)[0]

        no_peak = results[no_peak_var]
        peak = results[peak_var]
        crit_peak = results[crit_peak_var]

        readable_no_peak = self.readable_results_list(no_peak)
        readable_peak = self.readable_results_list(peak)
        readable_crit_peak = self.readable_results_list(crit_peak)

        return readable_no_peak,readable_peak,readable_crit_peak

    def get_time_table(self, no_peak_list, peak_list, crit_peak_list, open_time):

        time_table_var = "L"
        open_time_minutes = str(mt.float_to_minute(open_time))
        no_peak_str = str(no_peak_list).replace("'","")
        peak_str = str(peak_list).replace("'", "")
        crit_peak_str = str(crit_peak_list).replace("'", "")

        # final_arrangement(L, A, B, C, CurrentTime)
        query_str = "final_arrangement(" + time_table_var + "," + no_peak_str + "," + peak_str + "," + crit_peak_str + "," + open_time_minutes + ")"
        print(query_str)

        a = self.p.query(query_str)

        results = list(a)[0][time_table_var]

        readable_time_table = self.readable_time_table_list(results)

        print("Time table:")
        print(readable_time_table)

        return readable_time_table

    def calculate_cost(self, start_time, end_time, kW):
        total = 0
        for i in range(start_time, end_time):
            total += minute_cost_table[i]
        return total * kW

    def generate_nodes(self, machines, open_time, close_time):

        start_node = machine.Machine("root_node",0,0)

        for m in machines:
            new_m_list = machines[:]
            new_m_list.remove(m)

            cost_H = self.calculate_cost(open_time, open_time + m.get_duration_minutes(),
                                         m.get_energy_consumption())
            id_H = uuid.uuid4().node
            fact_H = "path( start , "+ str(id_H)+ ","+ str(cost_H)+ ")"
            print(fact_H)
            self.p.assertz(fact_H)
            self.generate_nodes_recur(m, id_H, "H", new_m_list, open_time, close_time)

            cost_T = self.calculate_cost(close_time - m.get_duration_minutes(), close_time,
                                         m.get_energy_consumption())
            id_T = uuid.uuid4().node
            fact_T = "path( start , "+ str(id_T)+ ","+ str(cost_T)+ ")"
            print(fact_T)
            self.p.assertz(fact_T)
            self.generate_nodes_recur(m, id_T, "T", new_m_list, open_time, close_time)

            print(self.uuid_map)

    def generate_nodes_recur(self, parent, parent_uuid, position, frontier, open_time, close_time):
        if len(frontier) == 0:
            print("path(", parent_uuid, ", end ,", 0, ")")
            return
        for machine in frontier:
            new_frontier = frontier[:]
            new_frontier.remove(machine)

            cost_H = self.calculate_cost(open_time, open_time + machine.get_duration_minutes(), machine.get_energy_consumption())
            id_H = uuid.uuid4().node
            fact_H = "path(" + str(parent_uuid) + "," + str(id_H) + "," + str(cost_H) + ")"
            print(fact_H)
            self.p.assertz(fact_H)
            self.uuid_map[id_H].append(("H",machine))
            self.generate_nodes_recur(machine, id_H, "H", new_frontier[:], open_time, close_time)

            cost_T = self.calculate_cost(close_time - machine.get_duration_minutes(), close_time, machine.get_energy_consumption())
            id_T = uuid.uuid4().node
            fact_T = "path("+ str(parent_uuid)+ ","+ str(id_T)+ ","+ str(cost_T)+ ")"
            print(fact_T)
            self.p.assertz(fact_T)
            self.uuid_map[id_T].append(("T", machine))
            self.generate_nodes_recur(machine, id_T, "T", new_frontier[:], open_time, close_time)