import __init__
from my_lib import Machine
from my_lib import Factory
from my_lib import MachineCalculator

m1 = Machine(1,40,300)
m2 = Machine(2,50,200)
m3 = Machine(3,80,400)
print(m1)

fac = Factory()
fac.add_machine(m1)
fac.add_machine(m2)
fac.add_machine(m3)


