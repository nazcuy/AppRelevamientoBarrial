.. app relevamiento barrial documentation master file, created by
   sphinx-quickstart on Fri Feb  7 00:34:41 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Aplicación Relevamiento Barrial
======================================
.. tip::

	La aplicación es un **gestor de relevamiento barrial** que permite **registrar, consultar, modificar y eliminar** información de viviendas o registros comunitarios 
	a través de una interfaz gráfica intuitiva.

	Utiliza **Tkinter** para la interfaz de usuario, donde se ingresan datos como nombre, dirección y nivel educativo, 
	y almacena esta información en una base de datos **SQLite.**

	Los registros se muestran en un *Treeview* y se complementan con un *gráfico interactivo* que visualiza la distribución de los niveles educativos, 
	facilitando el análisis de la información. 

	Además, la aplicación implementa un sistema de notificaciones basado en el **patrón observador** 
	y **envía logs de las operaciones (altas, bajas y modificaciones) a un servidor remoto**, 
	lo que permite un seguimiento detallado de las actividades realizadas.


.. toctree::
   :maxdepth: 2
   :caption: Contenido:
   
   modules
   

