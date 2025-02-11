Módulo "controlador.py"
========================

Este módulo define la clase `Controlador`, que actúa de puente entre la vista y el modelo.
Se encarga de ejecutar operaciones (alta, baja, modificación, consulta) y enviar logs a un servidor remoto.

Código fuente
-------------

A continuación, se presenta el código completo del controlador:

.. code-block:: python
   :linenos:

   """
   Controlador.
   
   Este módulo define la clase Controlador, que actúa de puente entre la vista y el modelo.
   Se encarga de ejecutar operaciones (alta, baja, modificación, consulta) y enviar logs a un servidor remoto.
   """
   from peewee import *
   from observador import Observador
   import modelo
   import socket

   class Controlador(Observador):
       # Hereda de la clase Observador para notificar a la vista sobre los cambios.
       def __init__(self, vista):
           # Inicializa la instancia del controlador.
           super().__init__()
           self.vista = vista
           self.abmc = modelo.Abmc()
           self.log_host = 'localhost'  # Profe le saco la IP y el puerto para enviarlo.
           self.log_puerto = 12345  # Profe le saco la IP y el puerto para enviarlo.
           
       def enviar_log(self, mensaje):
           # Envía un mensaje de log al servidor remoto.
           try:
               with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                   s.connect((self.log_host, self.log_puerto))  # Conecta al servidor de logs.
                   s.sendall(mensaje.encode('utf-8'))  # Envía el mensaje codificado
           except ConnectionRefusedError:
               print("Error: No se pudo conectar al servidor de logs.")
           except Exception as e:
               print(f"Error al enviar log: {e}")
          
       def realizar_alta(self, nombre, direccion, educacion):
           # Inserta un registro
           if self.abmc.alta_registro(nombre, direccion, educacion):
               log_msg = f"Alta realizada: {nombre}, {direccion}, {educacion}"
               self.enviar_log(log_msg)
               print("Alta de vivienda", "¡La casa fue cargada con éxito!")
               self.notificar_observadores("alta", nombre, direccion, educacion)
           else:
               print("Error", "No se pudo guardar la vivienda.")
           self.vista.actualizar_vista()

       def realizar_baja(self, vivienda_id):
           # Elimina un registro
           self.abmc.borrar_registro(vivienda_id)
           log_msg = f"Baja realizada: ID {vivienda_id}"
           self.enviar_log(log_msg)
           self.notificar_observadores("baja", vivienda_id)

       def realizar_modificacion(self, vivienda_id, nombre, direccion, educacion):
           # Modifica un registro
           try:
               self.abmc.modificar_registro(vivienda_id, nombre, direccion, educacion)
               log_msg = f"Modificación realizada: ID {vivienda_id}, {nombre}, {direccion}, {educacion}"
               self.enviar_log(log_msg)
               self.notificar_observadores("modificacion", vivienda_id, nombre, direccion, educacion)
               print(f"Controlador: Registro con ID {vivienda_id} modificado correctamente.")
           except Exception as e:
               print(f"Controlador: Error al modificar el registro: {e}")
               raise

       def realizar_consulta(self):
           # Realiza una consulta de registros a la base de datos.
           return self.abmc.consultar_registro()
