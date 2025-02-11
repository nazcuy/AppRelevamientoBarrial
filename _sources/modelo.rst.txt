Módulo "modelo.py"
===================

.. automodule:: modelo
   :members:
   :undoc-members:
   :show-inheritance:

Definición y conexión a la base de datos
----------------------------------------

.. code-block:: python

   from peewee import *

   # Se define la conexión a una base de datos SQLite.
   basededatos = SqliteDatabase("censo.db")

Clase de conexión a la base de datos
------------------------------------

.. code-block:: python

   class Conexion_de_BD():
       """
       Clase para gestionar la conexión a la base de datos.
       Proporciona métodos para conectar, desconectar y crear las tablas necesarias.
       """
       def __init__(self, nombreBD="censo.db"):
           # Inicializa la conexión con el nombre de la base de datos.
           self.nombreBD = nombreBD
           self.basededatos = SqliteDatabase(self.nombreBD)

       def conectar(self):
           # Conecta a la base de datos.
           try:
               self.basededatos.connect()
               print(f"La conexión a {self.nombreBD} fue sumamente exitosa!")
           except OperationalError as e:
               print(f"Tenés un error al conectar la base de datos:{self.nombreBD}: {e}")
           finally:
               print(f"El intento de conectarse a la base de datos {self.nombreBD} ha finalizado.")

       def desconectar(self):
           # Desconecta la base de datos.
           if self.basededatos.is_closed():
               print("Conexión cerrada correctamente.")
           else:
               print("No se pudo hacer la desconexión, la base de datos está abierta.")

       def crear_tabla(self):
           # Crea la tabla para el modelo Vivienda si no existe.
           self.basededato
