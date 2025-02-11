"""
Observador.

Este módulo define la clase Observador, implementa el patrón Observador
permitiendo que objetos se agreguen como observadores y reciban notificaciones de eventos.
"""

class Observador:
    def __init__(self):
        """
        Inicializa una nueva instancia de la clase Observador.
        Crea una lista vacía para almacenar los observadores registrados.
        """
        self.observadores = []

    def agregar_observador(self, observador):
        #Agrega un observador a la lista.
        self.observadores.append(observador)

    def eliminar_observador(self, observador):
        #Elimina un observador de la lista.
        self.observadores.remove(observador)

    def notificar_observadores(self, evento, *args, **kwargs):
        #Notifica a todos los observadores sobre un evento.
        for observador in self.observadores:
            observador.actualizar(evento, *args, **kwargs)