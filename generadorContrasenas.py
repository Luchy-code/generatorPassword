import random as rd
import string
import tkinter as tk
from tkinter import messagebox


# Modelo
class Model:
    def __init__(self, largo=0):
        self.largo = largo
        self.candidato = ""
        self.lista = list(string.ascii_letters + string.digits + string.punctuation)
        self.robustez = ""

    def calcular_robustez(self):
        """Determina la robustez de la contraseña según su longitud."""
        if self.largo <= 5:
            self.robustez = "Débil"
        elif 5 < self.largo <= 8:
            self.robustez = "Intermedia"
        else:
            self.robustez = "Fuerte"
        return self.robustez

    def generar(self):
        """Genera una contraseña aleatoria."""
        self.candidato = ''.join(rd.choices(self.lista, k=self.largo))
        return self.candidato


# Vista
class Interfaz:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Generador de Contraseñas")
        self.window.geometry("400x250")

        # Etiqueta
        self.label = tk.Label(self.window, text="Introduzca el largo:", fg="black", font=("Arial", 12, "bold"))
        self.label.place(relx=0.0, rely=0.05)

        # Campo de entrada
        self.entry = tk.Entry(self.window)
        self.entry.place(relx=0.4, rely=0.06)

        # Botones
        self.boton1 = tk.Button(self.window, text="Crear", bg="light green")
        self.boton1.place(relx=0.3, rely=0.2)

        self.boton2 = tk.Button(self.window, text="Otra vez", bg="light blue")
        self.boton2.place(relx=0.5, rely=0.2)

        # Label para mostrar contraseña
        self.labelPass = None
        # Label para mostrar robustez
        self.labelRobustez = None

    def mostrar_resultado(self, candidato, robustez):
        """Muestra la contraseña generada y su robustez."""
        if self.labelPass:
            self.labelPass.destroy()
        if self.labelRobustez:
            self.labelRobustez.destroy()

        self.labelPass = tk.Label(self.window, text=f"Contraseña: {candidato}", fg="black", font=("Arial", 12, "bold"))
        self.labelPass.place(relx=0.0, rely=0.5)

         # Determinar color según robustez
        color = "red" if robustez == "Débil" else "orange" if robustez == "Intermedia" else "green"

        self.labelRobustez = tk.Label(self.window, text=f"Robustez: {robustez}", fg=color, font=("Arial", 12, "bold"))
        self.labelRobustez.place(relx=0.0, rely=0.6)

    def limpiar(self):
        """Limpia el campo de entrada y elimina las etiquetas de resultados."""
        self.entry.delete(0, tk.END)
        if self.labelPass:
            self.labelPass.destroy()
        if self.labelRobustez:
            self.labelRobustez.destroy()

    def iniciar(self):
        """Inicia el loop principal de la ventana."""
        self.window.mainloop()

    def get_largo(self):
        """Obtiene el valor del largo ingresado."""
        return self.entry.get()
    def vincular_tecla_enter(self, callback):
        """Vincula la tecla Enter al método proporcionado."""
        self.window.bind("<Return>", lambda event: callback())


# Controlador
class Controller:
    def __init__(self, vista, modelo):
        self.vista = vista
        self.modelo = modelo

        # Vincular botones a métodos del controlador
        self.vista.boton1.config(command=self.validar_entrada)
        # Vincular la tecla Enter al botón "Crear"
        self.vista.vincular_tecla_enter(self.validar_entrada)
        self.vista.boton2.config(command=self.reiniciar)

    def validar_entrada(self):
        """Valida la entrada y actualiza la vista con la contraseña generada."""
        entrada = self.vista.get_largo()
        if not entrada.isdigit() or int(entrada) <= 0:
            messagebox.showerror("Error", "Por favor, introduzca un número mayor a 0")
            return
        elif int(entrada) > 15:
            messagebox.showerror("Error", "Por favor, introduzca un número más chico")
            return

        # Configurar el modelo con el nuevo largo
        self.modelo.largo = int(entrada)
        candidato = self.modelo.generar()
        robustez = self.modelo.calcular_robustez()
        self.vista.mostrar_resultado(candidato, robustez)

    def reiniciar(self):
        """Reinicia la entrada y la vista."""
        self.vista.limpiar()


# Crear instancias de MVC
modelo = Model()
vista = Interfaz()
controlador = Controller(vista, modelo)

# Iniciar la aplicación
vista.iniciar()
