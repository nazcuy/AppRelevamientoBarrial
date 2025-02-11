Módulo "observador.py"
======================

.. automodule:: observador
   :members:
   :undoc-members:
   :private-members:
   :special-members: __init__
   :show-inheritance:
   :exclude-members: __weakref__

Definición de la clase Observador
---------------------------------

.. code-block:: python

   class Observador:
       """
       Observador.

       Este módulo define la clase Observador, implementa el patrón Observador
       permitiendo que objetos se agreguen como observadores y reciban notificaciones de eventos.
       """

       def __init__(self):
           """
           Inicializa una nueva instancia de la clase Observador.
           Crea una lista vacía para almacenar los observadores registrados.
           """
           self.observadores = []

       def agregar_observador(self, observador):
           # Agrega un observador a la lista.
           self.observadores.append(observador)

       def eliminar_observador(self, observador):
           # Elimina un observador de la lista.
           self.observadores.remove(observador)

       def notificar_observadores(self, evento, *args, **kwargs):
           # Notifica a todos los observadores sobre un evento.
           for observador in self.observadores:
               observador.actualizar(evento, *args, **kwargs)

