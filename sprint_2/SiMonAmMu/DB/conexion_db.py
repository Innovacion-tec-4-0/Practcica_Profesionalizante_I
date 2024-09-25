#conexion_db.py
import mysql.connector

class Conexion:
    def __init__(self):
        self.conectar = None
        try:
            self.conectar = mysql.connector.connect(                        
                host="localhost",
                user="root",
                password="root",
                database="simonammu"
            )
            print("Conexión exitosa")
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")

    def __enter__(self):
        if self.conectar is None:
            raise Exception("No se pudo establecer la conexión a la base de datos.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conectar:
            self.conectar.close()
            print("Conexión a la base de datos cerrada.")
            
    def ver(self):
        if self.conectar is None:
            print("No hay conexión a la base de datos.")
            return

        cursor = self.conectar.cursor()
        sql = "SELECT * FROM sensores"
        cursor.execute(sql)
        datos = cursor.fetchall()
        
        if len(datos) < 1:
            print("No se encontraron resultados")
        else:
            for i in datos:
                print(i)

    def insertarDatos(self, a):
        if self.conectar is None:
            print("No hay conexión a la base de datos.")
            return

        cursor = self.conectar.cursor()
        sql = "INSERT INTO sensores (id, sensor, nombre, descripcion, fecha) VALUES (%s, %s, %s, %s, %s)"
        data = (a.getid(),
                a.getsensor(),
                a.getnombre(),
                a.getdescripcion(),
                a.getfecha())
        cursor.execute(sql, data)
        self.conectar.commit()
        print("Registrado")

    def cerrar_conexion(self):
        if self.conectar:
            self.conectar.close()
            print("Conexión a la base de datos cerrada.")
