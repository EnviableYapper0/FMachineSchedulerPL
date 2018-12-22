class Machine(object):
    def __init__(self, name, duration, energy_consumption):
        self.name = name
        self.duration = duration
        self.energy_consumption = energy_consumption

    def get_duration_str(self):
        return str(self.duration) + " Hrs."

    def get_energy_consumption_str(self):
        return str(self.energy_consumption) + " KW/h"

    def get_name(self):
        return self.name

    def get_kwh(self):
        return self.energy_consumption

    def get_duration(self):
        return self.duration

    def to_fact(self):
        attributes = [self.name, self.energy_consumption, self.duration]
        return "machine(" + ",".join(str(att) for att in attributes) + ")"

    def __str__(self):
        return self.to_fact()
