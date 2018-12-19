from pyswip import Prolog

p = Prolog()
p.consult('test.pl')
# p.assertz('A = []')
# a = p.query("find_xyz([machine(1,60,300),machine(2,80,600)] \
        # ,[],[],[],180,60,60)")

print(list(a))
