"""vista.py"""

from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import ImageTk, Image
import modelo
import datetime
from pathlib import Path
import os
import sys
import threading
import subprocess


proceso = ""


class Control:

    """Clase "control", interfaz gráfica de la aplicación"""

    def __init__(self, ventana):
        self.root = ventana
        self.root.geometry("1050x500")
        self.root.resizable(False, False)
        self.root.title("Proyecto ABMC")
        color_fondo = "#006"
        color_letra = "#FFF"
        self.root.configure(background=color_fondo)

        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.ruta = os.path.join(self.BASE_DIR, "img", "bebe3.jpg")

        self.raiz = Path(__file__).resolve().parent
        self.ruta_server = os.path.join(self.raiz, "servidor", "server.py")

        self.botonencendido = Button(
            self.root,
            text="Encender Servidor",
            bd=3,
            bg="light green",
            fg="white",
            command=lambda: self.conexion(),
        )
        self.botonencendido.place(x=25, y=430, width=100, height=30)

        self.botonapagado = Button(
            self.root,
            text="Apagar Servidor",
            bd=3,
            bg="light pink",
            fg="white",
            command=lambda: self.apagar(),
        )
        self.botonapagado.place(x=165, y=430, width=100, height=30)
        self.botonapagado.config(state=DISABLED)

        self.foto = Image.open(self.ruta)
        self.foto1 = ImageTk.PhotoImage(self.foto)
        self.fotito = tk.Label(self.root, image=self.foto1)
        self.fotito.place(x=900, y=1, relwidth=0.06, relheight=0.13)
        self.titulo = Label(
            self.root,
            text="Hospital Maternal Babuinos Felices",
            bg=color_fondo,
            fg=color_letra,
            font="arial 31",
        )
        self.titulo.place(x=180, y=20)

        self.objeto = modelo.Abmc()

        self.menubar = Menu(self.root)

        self.menu_edicion = Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label="Versión", command=self.objeto.version)
        self.root.config(menu=self.menubar)

        self.var_id = StringVar()
        self.var_nombre = StringVar()
        self.var_apellido = StringVar()
        self.var_fecha = StringVar()
        self.var_hora = StringVar()
        self.var_parto = StringVar()
        self.var_sexo = StringVar()
        self.var_peso = StringVar()
        self.var_talla = StringVar()
        self.var_fecha.set(datetime.date.today().strftime("%d/%m/%Y"))
        self.var_hora.set(datetime.date.today().strftime("%H:%M"))

        self.nombre = Label(
            self.root,
            text="Nombre del Bebé: ",
            fg=color_letra,
            bg=color_fondo,
            font="arial 12",
        )
        self.nombre.place(x=15, y=110)
        self.entry_nombre = Entry(self.root, textvariable=self.var_nombre, bd=2)
        self.entry_nombre.place(x=155, y=110)

        self.apellido = Label(
            self.root,
            text="Apellido materno: ",
            fg=color_letra,
            bg=color_fondo,
            font="arial 12",
        )
        self.apellido.place(x=15, y=150)

        self.entry_apellido = Entry(self.root, textvariable=self.var_apellido, bd=2)
        self.entry_apellido.place(x=155, y=150)

        self.fecha = Label(
            self.root,
            text="Fecha (D/M/A): ",
            fg=color_letra,
            bg=color_fondo,
            font="arial 12",
        )
        self.fecha.place(x=15, y=190)

        self.entry_fecha = Entry(self.root, textvariable=self.var_fecha, bd=2, width=15)
        self.entry_fecha.place(x=155, y=190)

        self.hora = Label(
            self.root,
            text="Hora (HH:MM): ",
            fg=color_letra,
            bg=color_fondo,
            font="arial 12",
        )
        self.hora.place(x=15, y=230)
        self.entry_hora = Entry(self.root, textvariable=self.var_hora, bd=2, width=15)
        self.entry_hora.place(x=155, y=230)

        self.parto = Label(
            self.root,
            text="Tipo de parto: ",
            fg=color_letra,
            bg=color_fondo,
            font="arial 12",
        )
        self.parto.place(x=15, y=270)
        self.entry_parto = Entry(self.root, textvariable=self.var_parto, bd=2, width=15)
        self.entry_parto.place(x=155, y=270)

        self.sexo = Label(
            self.root,
            text="Sexo (F o M): ",
            fg=color_letra,
            bg=color_fondo,
            font="arial 12",
        )
        self.sexo.place(x=15, y=310)
        self.entry_parto = Entry(self.root, textvariable=self.var_sexo, bd=2, width=15)
        self.entry_parto.place(x=155, y=310)

        self.peso = Label(
            self.root,
            text="Peso (gr.): ",
            fg=color_letra,
            bg=color_fondo,
            font="arial 12",
        )
        self.peso.place(x=15, y=350)
        self.entry_peso = Entry(self.root, textvariable=self.var_peso, bd=2, width=15)
        self.entry_peso.place(x=155, y=350)

        self.talla = Label(
            self.root,
            text="Talla (cm): ",
            fg=color_letra,
            bg=color_fondo,
            font="arial 12",
        )
        self.talla.place(x=15, y=390)
        self.entry_talla = Entry(self.root, textvariable=self.var_talla, bd=2, width=15)
        self.entry_talla.place(x=155, y=390)

        self.e1 = Entry(self.root, textvariable=self.var_id)

        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = (
            "col1",
            "col2",
            "col3",
            "col4",
            "col5",
            "col6",
            "col7",
            "col8",
        )
        self.tree.column("#0", width=20, minwidth=20, anchor="center")
        self.tree.column("col1", width=70, minwidth=150, anchor="center")
        self.tree.column("col2", width=70, minwidth=150, anchor="center")
        self.tree.column("col3", width=40, minwidth=65, anchor="center")
        self.tree.column("col4", width=40, minwidth=65, anchor="center")
        self.tree.column("col5", width=40, minwidth=65, anchor="center")
        self.tree.column("col6", width=40, minwidth=65, anchor="center")
        self.tree.column("col7", width=40, minwidth=65, anchor="center")
        self.tree.column("col8", width=40, minwidth=65, anchor="center")
        self.tree.heading("#0", text="id")
        self.tree.heading("col1", text="Nombre", anchor="center")
        self.tree.heading("col2", text="Apellido", anchor="center")
        self.tree.heading("col3", text="Fecha", anchor="center")
        self.tree.heading("col4", text="Hora", anchor="center")
        self.tree.heading("col5", text="Parto", anchor="center")
        self.tree.heading("col6", text="Sexo", anchor="center")
        self.tree.heading("col7", text="Peso", anchor="center")
        self.tree.heading("col8", text="Talla", anchor="center")
        self.tree.place(x=300, y=110, width=730, height=302)

        self.botonagregar = Button(
            self.root,
            text="Guardar",
            bd=3,
            bg="light slate blue",
            fg="white",
            command=lambda: self.objeto.alta(
                self.var_nombre,
                self.var_apellido,
                self.var_fecha,
                self.var_hora,
                self.var_parto,
                self.var_sexo,
                self.var_peso,
                self.var_talla,
                self.tree,
            ),
        )
        self.botonagregar.place(x=385, y=430, width=100, height=30)

        self.botoneliminar = Button(
            self.root,
            text="Eliminar",
            bd=3,
            bg="light slate blue",
            fg="white",
            command=lambda: self.objeto.baja(self.tree),
        )
        self.botoneliminar.place(x=505, y=430, width=100, height=30)

        self.botonconsultar = Button(
            self.root,
            text="Consultar",
            bd=3,
            bg="light slate blue",
            fg="white",
            command=lambda: self.objeto.consultar(self.tree),
        )
        self.botonconsultar.place(x=625, y=430, width=100, height=30)

        self.botonmodificar = Button(
            self.root,
            text="Modificar",
            bd=3,
            bg="light slate blue",
            fg="white",
            command=lambda: self.objeto.actualizar(
                self.var_nombre,
                self.var_apellido,
                self.var_fecha,
                self.var_hora,
                self.var_parto,
                self.var_sexo,
                self.var_peso,
                self.var_talla,
                self.tree,
            ),
        )

        self.botonmodificar.place(x=745, y=430, width=100, height=30)

        self.botonsalir = Button(
            self.root,
            text="Salir...",
            bd=3,
            bg="light pink",
            fg="white",
            command=lambda: self.objeto.salir(self.root),
        )
        self.botonsalir.place(x=865, y=430, width=100, height=30)

    def conexion(
        self,
    ):
        """
        Conexión del servidor
        """
        if proceso != "":
            proceso.kill()
            threading.Thread(target=self.encender, args=(True,), daemon=True).start()
        else:
            threading.Thread(target=self.encender, args=(True,), daemon=True).start()

    def encender(self, arg):
        """
        Método para el encendido del servidor
        """
        path = self.ruta_server
        if arg is True:
            global proceso
            proceso = subprocess.Popen([sys.executable, path])
            proceso.communicate()
            self.botonencendido.config(state=DISABLED)
            self.botonapagado.config(state=NORMAL)
            print("El servidor se ha encendido")
        else:
            print("")

    def apagar(
        self,
    ):
        """
        Método para el apagado del servidor
        """
        global proceso
        if proceso != "":
            self.botonencendido.config(state=NORMAL)
            self.botonapagado.config(state=DISABLED)
            print("El servidor se ha apagado")
            proceso.kill()
        else:
            print("")
