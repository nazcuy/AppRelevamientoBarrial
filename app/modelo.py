"""
Modelo.

Este módulo define la conexión a la base de datos y las operaciones de Alta, Baja, Modificación y Consulta utilizando Peewee.
"""
from peewee import *
#Se define la conexión a una base de datos SQLite.
basededatos = SqliteDatabase ("censo.db")


class Conexion_de_BD():
    """
    Clase para gestionar la conexión a la base de datos.
    Proporciona métodos para conectar, desconectar y crear las tablas necesarias.
    """
    def __init__(self, nombreBD="censo.db"):
        #Inicializa la conexión con el nombre de la base de datos.
        self.nombreBD = nombreBD
        self.basededatos = SqliteDatabase (self.nombreBD)

    def conectar(self):
        #Conecta a la base de datos.
        try:
            self.basededatos.connect()
            print(f"La conexión a {self.nombreBD} fue sumamente exitosa!")
        except OperationalError as e:
            print(f"Tenés un error al conectar la base de datos:{self.nombreBD}: {e}")
        finally:
            print(f"El intento de conectarse a la base de datos {self.nombreBD} ha finalizado.")

    def desconectar(self):
        #Desconecta la base de datos.
        if self.basededatos.is_closed():
            print("Conexión cerrada correctamente.")
        else:
            print("No se pudo hacer la desconexión, la base de datos está abierta.")

    def crear_tabla(self):
        #Crea la tabla para el modelo Vivienda si no existe.
        self.basededatos.create_tables([Vivienda])
        
class Vivienda(Model):
    """
    Modelo Vivienda que representa un registro en la base de datos.
    """
    nombre = CharField()
    direccion = CharField()
    educacion = CharField()

    class Meta():
        database = basededatos

class Abmc:
    """
    Clase que tiene las operaciones básicas de la base de datos:
      - Alta
      - Baja
      - Modificación
      - Consulta
    """
    def alta_registro(self, nombre, direccion, educacion):
        #Inserta un nuevo registro en la tabla Vivienda.
        try:
            nueva_vivienda = Vivienda.create(nombre=nombre, direccion=direccion, educacion=educacion)
            return True
        except Exception as e:
            print(f"Error al guardar en la base de datos: {e}")
            return False
            
    def borrar_registro(self, vivienda_id):
        #Elimina un registro de la tabla Vivienda basado en el ID.    
        try:
            # Intenta obtener la vivienda por el ID
            vivienda = Vivienda.get_by_id(vivienda_id)
            vivienda.delete_instance()  #Elimina la vivienda
        except Vivienda.DoesNotExist:
            # Si no se encuentra el ID en la base de datos
            print(f"Modelo: No se encontró una vivienda con ID {vivienda_id}")
        
    def modificar_registro(self, vivienda_id, nombre, direccion, educacion):
        #Modifica un registro existente en la tabla Vivienda.
        vivienda = Vivienda.get_by_id(vivienda_id)
        vivienda.nombre = nombre
        vivienda.direccion = direccion
        vivienda.educacion = educacion
        vivienda.save()
        print(f"Registro con ID {vivienda_id} actualizado en la base de datos.")
    
    def consultar_registro(self):
        #Consulta y muestra todos los registros de la tabla Vivienda.
        registros = list(Vivienda.select())
        if registros:
            print("Registros en la base de datos:")
            for registro in registros:
                print(f"ID: {registro.id}, Nombre: {registro.nombre}, Dirección: {registro.direccion}, Educación: {registro.educacion}")
        else:
            print("No hay registros en la base de datos.")
        return registros