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

NON_PEAK_COST = 2.6107 / 60
PEAK_COST = 3.2131 / 60
CRITICAL_PEAK_COST = 9.1617 / 60

minute_cost_table = ([NON_PEAK_COST] * PEAK_START) + \
                    ([PEAK_COST] * (CRITICAL_PEAK_START - PEAK_START)) + \
                    ([CRITICAL_PEAK_COST] * (CRITICAL_PEAK_END - CRITICAL_PEAK_START)) + \
                    ([PEAK_COST] * (PEAK_END - CRITICAL_PEAK_END)) + \
                    ([NON_PEAK_COST] * (1440 - PEAK_END))
class MachineCalculator:

    def __init__(self, prolog_file_name="my_lib/ai.pl"):
        self.p = Prolog()
        self.p.consult(prolog_file_name)

        self.uuid_map = defaultdict(list)

    def readable_results_list(self, results):
        all = []
        for r in results:
            all.append(str(r))
        return all

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

            head_from = open_time
            head_to = open_time + m.get_duration_minutes()
            cost_H = self.calculate_cost(head_from, head_to, m.get_energy_consumption())
            id_H = uuid.uuid4().node
            fact_H = "path( start , "+ str(id_H)+ ","+ str(cost_H)+ ")"
            print(fact_H)
            self.uuid_map[id_H].append(("H", m, head_from, head_to))
            self.p.assertz(fact_H)
            self.generate_nodes_recur(m, id_H, "H", new_m_list, head_to, close_time)

            tail_from = close_time - m.get_duration_minutes()
            tail_to = close_time
            cost_T = self.calculate_cost(tail_from, tail_to, m.get_energy_consumption())
            id_T = uuid.uuid4().node
            fact_T = "path( start , "+ str(id_T)+ ","+ str(cost_T)+ ")"
            print(fact_T)
            self.uuid_map[id_T].append(("T", m, tail_from, tail_to))
            self.p.assertz(fact_T)
            self.generate_nodes_recur(m, id_T, "T", new_m_list, open_time, tail_from)

        a = list(self.p.query("find_cheapest_path(X)"))[0]["X"]
        results = self.readable_results_list(a)
        print(results)
        results = results[-1::-1]

        path = []

        for each_uuid in results:
            if each_uuid == 'end' or each_uuid == 'start':
                continue
            else:
                node = self.uuid_map[int(each_uuid)]
                path.append(node)
                if len(node) > 0:
                    print(node[0][0],node[0][1], node[0][2], node[0][3])
                else:
                    print(node)


    def generate_nodes_recur(self, parent, parent_uuid, position, frontier, open_time, close_time):
        if len(frontier) == 0:
            print("path(", parent_uuid, ", end ,", 0, ")")
            fact_E = "path(" + str(parent_uuid) + ", end ," + str(0) + ")"
            self.p.assertz(fact_E)
            return
        for machine in frontier:
            new_frontier = frontier[:]
            new_frontier.remove(machine)

            head_from = open_time
            head_to = open_time + machine.get_duration_minutes()
            cost_H = self.calculate_cost(head_from, head_to, machine.get_energy_consumption())
            id_H = uuid.uuid4().node
            fact_H = "path(" + str(parent_uuid) + "," + str(id_H) + "," + str(cost_H) + ")"
            print(fact_H)
            self.p.assertz(fact_H)
            self.uuid_map[id_H].append(("H",machine, head_from, head_to))
            self.generate_nodes_recur(machine, id_H, "H", new_frontier[:], head_to, close_time)

            tail_from = close_time - machine.get_duration_minutes()
            tail_to = close_time
            cost_T = self.calculate_cost(tail_from, tail_to, machine.get_energy_consumption())
            id_T = uuid.uuid4().node
            fact_T = "path("+ str(parent_uuid)+ ","+ str(id_T)+ ","+ str(cost_T)+ ")"
            print(fact_T)
            self.p.assertz(fact_T)
            self.uuid_map[id_T].append(("T", machine, tail_from, tail_to))
            self.generate_nodes_recur(machine, id_T, "T", new_frontier[:], open_time, tail_from)