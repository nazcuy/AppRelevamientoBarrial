Módulo "vista.py"
=================

.. automodule:: vista
   :members:
   :undoc-members:
   :show-inheritance:

Descripción general
-------------------
Este módulo define la interfaz gráfica de la aplicación utilizando Tkinter. 
Contiene la clase `Aplicacion`, que administra la interacción con el usuario, 
actualiza la vista (incluyendo un gráfico) y se comunica con el controlador.

Código fuente
-------------
A continuación, se presenta el código fuente del módulo `vista.py`:

.. literalinclude:: ../../vista.py
   :language: python
   :linenos:
   :caption: Código fuente de vista.py

Detalle de las clases y funciones
---------------------------------

Clase `Aplicacion`
~~~~~~~~~~~~~~~~~~~
La clase `Aplicacion` es la encargada de gestionar la interfaz gráfica, 
así como la interacción con los componentes de la misma.

- **Método `__init__`:** Inicializa la interfaz gráfica y los componentes principales de la aplicación.
- **Método `actualizar`:** Actualiza la vista según el evento que se haya notificado (alta, baja, modificación).
- **Método `alta`:** Gestiona la operación de alta de un nuevo registro en la base de datos.
- **Método `borrar`:** Gestiona la operación de baja de un registro seleccionado.
- **Método `modificar`:** Gestiona el proceso de modificación de un registro seleccionado.
- **Método `consulta`:** Recupera los registros de la base de datos y actualiza la vista.
- **Método `actualizar_grafico`:** Actualiza el gráfico de barras que muestra los niveles educativos de los registros.
- **Método `actualizar_vista`:** Actualiza el Treeview para reflejar los registros actuales de la base de datos.

Decorador `validar_campos`
~~~~~~~~~~~~~~~~~~~~~~~~~~
El decorador `validar_campos` asegura que los campos de entrada no estén vacíos antes de realizar cualquier operación (alta, baja, modificación). Si alguno de los campos está vacío, muestra un mensaje de error.

Explicación del gráfico
------------------------
El gráfico generado por el método `actualizar_grafico` representa los niveles educativos de los registros. Utiliza la biblioteca `matplotlib` para crear un gráfico de barras que es incrustado en la interfaz gráfica usando Tkinter.

El gráfico se actualiza cada vez que se realiza una operación en la base de datos (alta, baja, modificación o consulta).

