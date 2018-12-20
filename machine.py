class Machine:

    def __init__(self,name,kwh,duration):
        self.name = name
        self.kwh = kwh
        self.duration = duration

    def get_name(self):
        return self.name

    def get_kwh(self):
        return self.kwh

    def get_duration(self):
        return self.duration

    def __str__(self):
        attributes = [self.name,self.kwh,self.duration]
        return "machine(" + ",".join(attributes) + ")"

