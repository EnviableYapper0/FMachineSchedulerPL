import os
class Storage():
    def __init__(self):
        self.filename = "listMachine.txt"
        self.timeName = "timeName.txt"

    def saveTime(self,oopen,close):
        with open(self.timeName, "w") as self.t:
            self.t.write(str(oopen) +'\n')
            self.t.write(str(close) + '\n')

    def save(self,listMachine):
        with open(self.filename, "w") as self.f :
            for eachMachine in listMachine:
                self.f.write(eachMachine.name+"\n")
                self.f.write(eachMachine.get_duration()+"\n")
                self.f.write(eachMachine.get_energy()+"\n")

            self.f.close()
    def readTime(self):
        t=open(self.timeName,"r")
        t_read=t.readlines()
        t.close()
        return t_read
    def read(self):
        f=open(self.filename,"r")
        f_read=f.readlines()
        f.close()

        return f_read