import mysql.connector

class Conexion:
    def __init__(self):
        self.conectar = mysql.connector.connect(                        
                host="localhost",
                user="root",
                password = "pancho1677",
                database="iot")

        if self.conectar.is_connected:
            print("conexion exitosa")
    def ver(self):
        cursor = self.conectar.cursor()
        sql = "select * from sensores"
        cursor.execute(sql)
        datos = cursor.fetchall()
        
        if len(datos) < 1:
                        print("no se encontraron resultados")
        else:
            for i in datos:
                print(i)
        self.conectar.close()
    
    def insertarDatos(self,a):
        
            cursor = self.conectar.cursor()
            sql = "insert into sensores values(%s,%s,%s,%s,%s)"
            data = (a.getid(),
                    a.getsensor(),
                    a.getnombre(),
                    a.getdescripcion(),
                    a.getfecha())
            cursor.execute(sql,data)
            self.conectar.commit()
            
            print("registrado")

