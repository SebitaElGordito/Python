"""modelo.py"""

import re
import sqlite3
from tkinter import messagebox
import datetime
from peewee import *
import socket
from observador import Sujeto


class Abmc(Sujeto):

    """Clase "Abmc" a partir de la cual se crea la conexión con la base de datos, y se gestiona la lógica de la aplicación."""

    def __init__(
        self,
    ):
        pass

    def crear_base(
        self,
    ):
        con = sqlite3.connect("babuinos.db")
        return con

    def crear_tabla(self):
        """Función que crea la tabla, arrojándonos que "la tabla ya fue creada" si esta ya existe."""
        con = self.crear_base()
        cursor = con.cursor()
        sql = """CREATE TABLE IF NOT EXISTS proye (id PRIMARY KEY AUTOINCREMENT, nombre VARCHAR(20) NOT NULL, apellido VARCHAR(20) NOT NULL, fecha VARCHAR(10) NOT NULL, hora VARCHAR(5) NOT NULL, parto VARCHAR(1) NOT NULL, sexo VARCHAR(1) NOT NULL, peso VARCHAR(5) NOT NULL, talla VARCHAR(4) NOT NULL)"""
        cursor.execute(sql)
        con.commit()

    def version(self):
        info = "App Hospital Maternal Babuinos Felices.\nVersion 1.0.0"
        messagebox.showinfo(title="Información", message=info)

    def socket(self, mensaje):
        """
        Método para la conexión con el servidor
        """

        try:
            HOST, PORT = "localhost", 9000

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(0.0001)
            mensaje = mensaje

            sock.sendto(mensaje.encode("UTF-32"), (HOST, PORT))
            received = sock.recvfrom(1024)
            datos = received[0].strip()

            print(datos.decode("UTF-32"))

        except:
            print("El servidor no se encuentra en linea")

    def decoradore(f):
        """Decorador para realizar un registro en la consola sobre de la función
        llamada"""

        def envoltura(*args):
            if f.__name__ == "alta":
                print("Se ha agregado un registro")
            elif f.__name__ == "baja":
                print("Se ha eliminado un registro")
            elif f.__name__ == "actualizar":
                print("Se ha actualizado un registro")
            f(*args)

        return envoltura

    @decoradore
    def alta(self, nombre, apellido, fecha, hora, parto, sexo, peso, talla, tree):
        """Función para dar de alta nuevos registros y guardarlos en la base de datos"""
        cadena = parto.get()
        patron = re.compile("N|C", re.I)
        """Regex que simplifica el ingreso de datos en "tipo de parto", aceptando solo N para parto natural, o C para Cesarea, permitiendo ingresarlos tanto en minúscula o mayúscula."""
        if patron.match(cadena):
            con = self.crear_base()
            cursor = con.cursor()
            data = (
                nombre.get(),
                apellido.get(),
                fecha.get(),
                hora.get(),
                parto.get(),
                sexo.get(),
                peso.get(),
                talla.get(),
            )
            sql = "INSERT INTO proye(nombre, apellido, fecha, hora, parto, sexo, peso, talla) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(sql, data)
            con.commit()
            self.limpiarcampos(nombre, apellido, fecha, hora, parto, sexo, peso, talla)
            self.consultar(tree)
            self.socket(
                f"Se ha agregado al babuino de Nombre: {nombre.get()}  Apellido: {apellido.get()} con fecha de nacimiento:  {fecha.get()}  hora de nacimiento: {hora.get()} tipo de parto:  {parto.get()} sexo:  {sexo.get()} con un peso en gramos de: {peso.get()} y una talla en centímetros de: {talla.get()}"
            )
            self.notificar(
                nombre.get(),
                apellido.get(),
                fecha.get(),
                hora.get(),
                parto.get(),
                sexo.get(),
                peso.get(),
                talla.get(),
            )

            if sql:
                messagebox.showinfo(
                    "Guardado en la base de datos",
                    "El babuino " + nombre.get() + " ha sido agregado exitosamente",
                )
        else:
            messagebox.showerror(
                "ERROR FATAL",
                "Error al ingresar los datos... por favor ingrese el parto Natural como 'N' o 'n' y Cesarea como 'C' o 'c'",
            )

    def limpiarcampos(
        self,
        nombre,
        apellido,
        fecha,
        hora,
        parto,
        sexo,
        peso,
        talla,
    ):
        """Función que se encarga de limpiar los campos de entrada, borrando los datos allí ingresados, una vez que se presiona algunos de los botones del Crud, y se realiza una acción."""
        nombre.set("")
        apellido.set("")
        fecha.set(datetime.date.today().strftime("%d/%m/%Y"))
        hora.set(datetime.date.today().strftime("%H:%M"))
        parto.set("")
        sexo.set("")
        peso.set("")
        talla.set("")

    @decoradore
    def baja(self, tree):
        """Función que sirve para eliminar los datos del registro seleccionado en pantalla. Necesita confirmación para ejecutar la acción."""
        valor = tree.selection()
        item = tree.item(valor)
        id = item["text"]
        val = messagebox.askquestion(
            "El campo será eliminado de forma permanente...",
            "¿Realmente desea eliminar el campo seleccionado?",
        )
        if val == "yes":
            con = self.crear_base()
            cursor = con.cursor()
            data = (id,)
            sql = "DELETE FROM proye WHERE ID= ?;"
            cursor.execute(sql, data)
            con.commit()
            tree.delete(valor)

            messagebox.showinfo(
                "Campo Eliminado", "El babuino ha sido eliminado de forma permanente"
            )

        else:
            pass

    def consultar(self, tree):
        """Función que permite mostrar en la pantalla de la app, toda la información existente hasta el momento en la base de datos."""
        records = tree.get_children()
        for elemento in records:
            tree.delete(elemento)

        sql = "SELECT * FROM proye ORDER BY ID ASC"
        con = self.crear_base()
        cursor = con.cursor()
        datos = cursor.execute(sql)

        resultado = datos.fetchall()
        for fila in resultado:
            tree.insert(
                "",
                0,
                text=fila[0],
                values=(
                    fila[1],
                    fila[2],
                    fila[3],
                    fila[4],
                    fila[5],
                    fila[6],
                    fila[7],
                    fila[8],
                ),
            )

    def seleccion(self, nombre, apellido, fecha, hora, parto, sexo, peso, talla, tree):
        """Función para seleccionar uno de los registros. Ésta función es necesaria para la función "borrar", permitiendole eliminar el registro seleccionado previamente, y para la función "actualizar", permitiéndole modificar los datos de ese registro seleccionado."""
        valor = tree.focus()
        item = tree.item(valor)
        nombre.set(tree.item(item, "values")[0])
        apellido.set(tree.item(item, "values")[1])
        fecha.set(tree.item(item, "values")[2])
        hora.set(tree.item(item, "values")[3])
        parto.set(tree.item(item, "values")[4])
        sexo.set(tree.item(item, "values")[5])
        peso.set(tree.item(item, "values")[6])
        talla.set(tree.item(item, "values")[7])

    @decoradore
    def actualizar(self, nombre, apellido, fecha, hora, parto, sexo, peso, talla, tree):
        """Función con la que se modifican los datos de un registro previamente seleccionado en la pantalla de la aplicación."""
        valor = tree.selection()
        item = tree.item(valor)
        id = item["text"]
        val = tree.item(
            valor,
            values=(
                nombre.get(),
                apellido.get(),
                fecha.get(),
                hora.get(),
                parto.get(),
                sexo.get(),
                peso.get(),
                talla.get(),
            ),
        )
        con = self.crear_base()
        cursor = con.cursor()
        data = (
            nombre.get(),
            apellido.get(),
            fecha.get(),
            hora.get(),
            parto.get(),
            sexo.get(),
            peso.get(),
            talla.get(),
            id,
        )
        sql = "UPDATE proye SET nombre=?, apellido=?, fecha=?, hora=?, parto=?, sexo=?, peso=?, talla=? WHERE id=?;"
        cursor.execute(sql, data)
        con.commit()
        self.consultar(tree)
        if data:
            messagebox.showinfo(
                "Actualización de datos...",
                "Los datos del babuino han sido actualizados exitosamente",
            )

    def salir(self, root_tk):
        """Función que permite cerrar la aplicación cuando el usuario presiona el botón "Salir". Necesita confirmación."""
        valor = messagebox.askquestion(
            "Saliendo de la aplicación...", "¿Realmente desea salir?"
        )
        if valor == "yes":
            root_tk.destroy()

        else:
            pass
