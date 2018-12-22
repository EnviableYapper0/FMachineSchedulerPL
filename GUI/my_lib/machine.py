import uuid
from . import my_time as mt

class Machine(object):
    def __init__(self, name, duration, energy_consumption):
        self.id = uuid.uuid4().node
        self.name = name
        self.duration = float(duration)
        self.energy_consumption = float(energy_consumption)

    def get_duration_str(self):
        return str(self.duration) + " Hrs."

    def get_energy_consumption_str(self):
        return str(self.energy_consumption) + " KW/h"

    def get_name(self):
        return self.name

    def get_energy_consumption(self):
        return self.energy_consumption

    def get_duration(self):
        return self.duration

    def get_duration_minutes(self):
        return mt.float_to_minute(self.duration)

    def to_fact(self):
        attributes = [self.id, self.get_duration_minutes(), self.energy_consumption]
        return "machine(" + ",".join(str(att) for att in attributes) + ")"

    def __str__(self):
        return self.to_fact()
