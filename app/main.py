"""
Main.

Este módulo es el punto de entrada de la aplicación. Se encarga de:
  - Inicializar la conexión a la base de datos.
  - Crear las tablas necesarias.
  - Configurar y mostrar la interfaz gráfica.
"""
import tkinter as tk
from vista import Aplicacion
from modelo import Conexion_de_BD

# Punto de entrada principal del programa.
if __name__ == "__main__":
    """
    Inicializa la conexión a la base de datos y crea la tabla si no existe.
    """
    conexion = Conexion_de_BD()
    conexion.conectar()
    conexion.crear_tabla()

    # Crea la ventana principal de la aplicación.
    root = tk.Tk()

    # Instanciamos el objeto "app" de la clase Aplicacion, que se encuentra en vista.py,
    # y le pasamos como argumento la ventana principal "root".
    app = Aplicacion(root)

    # Inicia el bucle principal de la interfaz gráfica.
    # Este bucle espera las interacciones del usuario y mantiene la aplicación en ejecución.
    root.mainloop()