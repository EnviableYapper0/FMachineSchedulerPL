
class Machine(object):
    def __init__(self, name, duration, energy_consumption):
        self.name = name
        self.duration = duration
        self.energy_consumption = energy_consumption
    def get_duration_str(self):
        return str(self.duration) + " Hrs."

    def get_duration(self):
        return str(self.duration)

    def get_energy_consumption_str(self):
        return str(self.energy_consumption) + " KW/h"

    def get_energy(self):
        print("duration"+str(self.duration))
        return str(self.duration)

