"""
Vista

Este módulo define la interfaz gráfica de la aplicación utilizando Tkinter.
Contiene la clase Aplicacion, que administra la interacción con el usuario,
actualiza la vista (incluyendo un gráfico) y se comunica con el controlador.
"""
import tkinter as tk
from tkinter import ttk, messagebox, Label, Frame, Entry, StringVar, Button, N, S, E, W
from controlador import Controlador
from modelo import Vivienda
from peewee import *
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def validar_campos(func):
    """
    Decorador para validar que los campos de entrada no estén vacíos.
    """
    def envoltorio(self, *args, **kwargs):
        nombre = self.a_val.get().strip()
        direccion = self.b_val.get().strip()
        educacion = self.c_val.get().strip()
        
        if not nombre or not direccion or not educacion:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        return func(self, *args, **kwargs)
    return envoltorio

class Aplicacion:
    """
    Clase principal de la interfaz gráfica.

    Configura y administra la ventana principal, maneja eventos (alta, baja, modificación, consulta)
    y actualiza tanto el Treeview como el gráfico mostrado.
    """
    def __init__(self, root):
        #Inicializa la interfaz gráfica y sus componentes.
        self.controlador = Controlador(self)
        self.controlador.agregar_observador(self)
        self.id_modificar = None
        #Configuración de la ventana principal.
        root.title("ORGANIZACIÓN DE LA COMUNIDAD - Gestor de gobierno popular")
        root.rowconfigure(1, weight=1)  
        root.rowconfigure(2, weight=1)
        root.columnconfigure(1, weight=3)
        
        #Etiqueta de título.
        titulo = Label(root, text="RELEVAMIENTO BARRIAL", bg="#253876", fg="#fdc444", font=("Open Sans ExtraBold", 16))
        titulo.grid(row=0, column=0, columnspan=2, sticky=E+W)

        #Marco izquierdo para los campos de entrada y botones.
        marco_izquierdo = Frame(root, padx=5, pady=5, bg="#f5efe1")
        marco_izquierdo.grid(row=1, column=0, sticky=N+S+E+W)
        marco_izquierdo.columnconfigure((0, 1), weight=1)

        #Marco para gráfico
        self.marco_grafico = Frame(root, bg="white", padx=5, pady=5)
        self.marco_grafico.grid(row=1, column=1, sticky=N+S+E+W)
        self.marco_grafico.rowconfigure(0, weight=1)
        self.marco_grafico.columnconfigure(0, weight=1)

        #Marco para datos (Treeview, ocupa la mitad inferior)
        marco_datos = Frame(root, bg="lightgrey", padx=5, pady=5)
        marco_datos.grid(row=2, column=1, sticky=N+S+E+W)
        marco_datos.rowconfigure(0, weight=1)
        marco_datos.columnconfigure(0, weight=1)
        
        #Etiquetas para los campos de entrada.
        nombre = Label(marco_izquierdo, text="Nombre y Apellido: ", bg="#f5efe1", fg="#000000", font=("Open Sans", 10, "italic"))
        nombre.grid(row=0, column=0, sticky=W)
        direcc=Label(marco_izquierdo, text="Dirección Relevada: ", bg="#f5efe1", fg="#000000", font=("Open Sans", 10, "italic"))
        direcc.grid(row=1, column=0, sticky=W)
        educ=Label(marco_izquierdo, text="Educación Alcanzada: ", bg="#f5efe1", fg="#000000", font=("Open Sans", 10, "italic"))
        educ.grid(row=2, column=0, sticky=W)

        #Variables para entradas
        self.a_val, self.b_val, self.c_val = StringVar(), StringVar(), StringVar()

        #Campos de entrada.
        Entry(marco_izquierdo, textvariable=self.a_val).grid(row=0, column=1, sticky=W+E)
        Entry(marco_izquierdo, textvariable=self.b_val).grid(row=1, column=1, sticky=W+E)
        Entry(marco_izquierdo, textvariable=self.c_val).grid(row=2, column=1, sticky=W+E)

        #Botones
        Button(marco_izquierdo, text="Alta", command=lambda: self.alta(),
               bg="#336699", fg="white", font=("Open Sans ExtraBold", 9)).grid(row=3, column=0, pady=10)
        Button(marco_izquierdo, text="Baja", command=lambda: self.borrar(),
               bg="#336699", fg="white", font=("Open Sans ExtraBold", 9)).grid(row=3, column=1, pady=10)
        Button(marco_izquierdo, text="Modificar", command=lambda: self.modificar(),
               bg="#336699", fg="white", font=("Open Sans ExtraBold", 9)).grid(row=4, column=0, pady=10)
        Button(marco_izquierdo, text="Consultar lista", command=lambda: self.consulta(),
               bg="#336699", fg="white", font=("Open Sans ExtraBold", 9)).grid(row=4, column=1, pady=10)

        #Configuración del Treeview para mostrar los registros.
        self.tree = ttk.Treeview(marco_datos, columns=("id", "col1", "col2", "col3"), show="headings")
        self.tree.heading("id", text="Id")
        self.tree.heading("col1", text="Nombre y apellido")
        self.tree.heading("col2", text="Dirección relevada")
        self.tree.heading("col3", text="Educación alcanzada")
        self.tree.grid(row=0, column=0, sticky=N+S+E+W)
        self.actualizar_vista()

    def actualizar(self, evento, *args, **kwargs):
        #Actualiza la vista en función del evento notificado.
        if evento == "alta":
            print("Notificación: Se realizó un alta.")
        elif evento == "baja":
            print("Notificación: Se realizó una baja.")
        elif evento == "modificacion":
            print("Notificación: Se realizó una modificación.")
        self.actualizar_vista()
        self.actualizar_grafico()

    @validar_campos
    def alta(self):
        """
        Gestiona la operación de alta.

        Si se tiene un ID para modificar (self.id_modificar), se realiza una actualización;
        de lo contrario, se inserta un nuevo registro.
        """
        nombre = self.a_val.get()
        direccion = self.b_val.get()
        educacion = self.c_val.get()
        #Validación: El nombre debe contener solo letras y espacios.
        if not re.match("^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre):
            messagebox.showerror("Error", "El nombre solo puede contener letras y espacios.")
            return
        if self.id_modificar is not None:
            try:
                self.controlador.realizar_modificacion(self.id_modificar, nombre, direccion, educacion)
                messagebox.showinfo("Modificación exitosa", "El registro ha sido actualizado.")
                self.id_modificar = None
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo modificar el registro: {e}")
        else:
            try:
                self.controlador.realizar_alta(nombre, direccion, educacion)
                messagebox.showinfo("Alta de vivienda", "¡La vivienda fue cargada con éxito!")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar la vivienda: {e}")

        self.actualizar_vista()
        self.actualizar_grafico()

    @validar_campos
    def borrar(self):
        """
        Gestiona la operación de baja.

        Elimina el registro seleccionado tanto de la base de datos como del Treeview.
        """
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            vivienda_id = item["values"][0]
            print(f"Valor de vivienda_id: {vivienda_id} (tipo: {type(vivienda_id)})")
            self.controlador.realizar_baja(vivienda_id)
            messagebox.showinfo("Borrar vivienda", "¡La vivienda fue borrada con éxito!")
            self.actualizar_vista()
            self.actualizar_grafico()


    @validar_campos
    def modificar(self):
        """
        Gestiona el proceso de modificación.

        Carga los datos del registro seleccionado en los campos de entrada para que el usuario
        pueda editar y luego actualizar el registro.
        """
        seleccion_item = self.tree.selection()
        if seleccion_item:
            item = self.tree.item(seleccion_item)
            self.id_modificar = item['values'][0]
            nombre = item['values'][1]
            direccion = item['values'][2]
            educacion = item['values'][3]
            #Cargamos los datos en los campos de entrada para editar
            self.a_val.set(nombre)
            self.b_val.set(direccion)
            self.c_val.set(educacion)
            print(f"Modificar: ID={self.id_modificar}, Nombre={nombre}, Dirección={direccion}, Educación={educacion}")
        else:
            messagebox.showerror("Error", "Seleccione un registro para modificar.")


    def consulta(self):
        """
        Gestiona la consulta de registros.

        Recupera los datos de la base de datos y actualiza tanto el Treeview como el gráfico.
        """
        self.controlador.realizar_consulta()
        self.actualizar_vista()
        self.actualizar_grafico()


    def actualizar_grafico(self):
        """
        Actualiza el gráfico mostrado en la interfaz.

        Crea un gráfico de barras que representa los niveles educativos de los registros.
        """
        #Limpia cualquier contenido previo en el marco
        for widget in self.marco_grafico.winfo_children():
            widget.destroy()
        educacion_contadores = {'A': 0, 'PI': 0,'PC': 0,  'SI': 0, 'SC': 0, 'TI': 0, 'TC': 0, 'UI': 0, 'UC': 0}
        viviendas = Vivienda.select()
        for vivienda in viviendas:
            educacion = vivienda.educacion
            if educacion in educacion_contadores:
                educacion_contadores[educacion] += 1

        #Prepara los datos para el gráfico
        categorias = list(educacion_contadores.keys())
        conteos = list(educacion_contadores.values())

        #Se crea el gráfico de barras
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(categorias, conteos, color='skyblue')

        #Añado el título y las etiquetas
        ax.set_title('TRAYECTORIA EDUCATIVA RELEVADA', fontsize=14)
        ax.set_xlabel('Nivel de Educación', fontsize=12)
        ax.set_ylabel('Cantidad de Personas Relevadas', fontsize=12)

        #Se convierte el gráfico a formato que Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.marco_grafico)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky=N+S+E+W)

    def actualizar_vista(self):
        """
        Actualiza el Treeview con los registros actuales de la base de datos.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)
        viviendas = Vivienda.select().order_by(Vivienda.id)
        if viviendas:
            for vivienda in viviendas:
                self.tree.insert("", tk.END, text=vivienda.id, values=(vivienda.id, vivienda.nombre, vivienda.direccion, vivienda.educacion))
        else:
            print("No se encontraron registros para mostrar.")
