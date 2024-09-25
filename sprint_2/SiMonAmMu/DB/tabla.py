from datetime import *

class Sensores():
    id = 0
    sensor = 0
    nombre = ""
    descripcion = ""
    fecha = datetime.today()

    def __init__(self,id,sensor,nombre,descripcion,fecha=None):
        self.id = id
        self.sensor = sensor
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha = fecha if fecha else datetime.today()
    def getid(self):
        return self.id
    def getsensor(self):
        return self.sensor
    def getnombre(self):
        return self.nombre
    def getdescripcion(self):
        return self.descripcion
    def getfecha(self):
        return self.fecha
    def setid(self,id):
        self.id = id
    def setsensor(self,sensor):
        self.sensor = sensor
    def setnombre(self,nombre):
        self.nombre = nombre
    def setdescripcion(self,descripcion):
        self.descripcion = descripcion
    def setfecha(self,fecha):
        self.fecha = fecha
