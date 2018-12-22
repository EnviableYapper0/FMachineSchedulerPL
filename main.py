from GUI.my_lib import Factory
from GUI.my_lib import Machine

m1 = Machine(1,40,300)
m2 = Machine(2,50,200)
m3 = Machine(3,80,400)
print(m1)

fac = Factory()
fac.add_machine(m1)
fac.add_machine(m2)
fac.add_machine(m3)


print(fac.get_sorted_machines_by_kwh())
