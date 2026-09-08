import tkinter as tk
from tkinter import ttk
from formulario import FormularioCRUD
from basedatos import RepositorioSQLite
from entidades import campos_vehiculo, campos_propietario

class MenuPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión CRUD")
        self.geometry("350x200")

        lbl = ttk.Label(self, text="Seleccione la Entidad a Gestionar", font=("Arial", 12, "bold"))
        lbl.pack(pady=20)

        # botón para abrir la entidad Vehículos
        btn_vehiculos = ttk.Button(
            self,
            text="Gestionar Vehículos",
            command=self.abrir_vehiculos
        )
        btn_vehiculos.pack(fill="x", padx=40, pady=5)

        # Botón para abrir la entidad Propietarios
        btn_propietarios = ttk.Button(
            self,
            text="Gestionar Propietarios",
            command=self.abrir_propietarios
        )
        btn_propietarios.pack(fill="x", padx=40, pady=5)

    def abrir_vehiculos(self):
        # Reutiliza la misma clase genérica pasándole los datos de Vehículos.
        # El repositorio también es genérico: solo cambia la tabla y los campos.
        repositorio = RepositorioSQLite("vehiculos", campos_vehiculo)
        FormularioCRUD(self, "Gestión de Vehículos", campos_vehiculo, repositorio)

    def abrir_propietarios(self):
        # Reutiliza la misma clase genérica pasándole los datos de Propietarios
        repositorio = RepositorioSQLite("propietarios", campos_propietario)
        FormularioCRUD(self, "Gestión de Propietarios", campos_propietario, repositorio)

if __name__ == "__main__":
    app = MenuPrincipal()
    app.mainloop()
