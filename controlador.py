from tkinter import Tk
import vista
from tkinter import ttk
import observador


class Controlador:
    """clase que controla toda la app, desde aqui puede ser lanzada"""

    def __init__(self, ventana):
        self.objeto_vista = vista.Control(ventana)
        self.el_observador = observador.ConcreteObserverA(self.objeto_vista.objeto)


if __name__ == "__main__":
    root_tk = Tk()
    control = Controlador(root_tk)
    root_tk.mainloop()
