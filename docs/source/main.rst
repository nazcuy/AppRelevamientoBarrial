Módulo "main.py"
================

.. automodule:: main
   :members:
   :undoc-members:
   :show-inheritance:

Inicialización de la base de datos
----------------------------------

.. code-block:: python

   from modelo import Conexion_de_BD

   # Inicializa la conexión a la base de datos y crea la tabla si no existe.
   conexion = Conexion_de_BD()
   conexion.conectar()
   conexion.crear_tabla()

Configuración de la interfaz gráfica
-------------------------------------

.. code-block:: python

   import tkinter as tk
   from vista import Aplicacion

   # Crea la ventana principal de la aplicación.
   root = tk.Tk()

   # Instancia la aplicación y le pasa la ventana principal.
   app = Aplicacion(root)

   # Inicia el bucle principal de la interfaz gráfica.
   root.mainloop()
