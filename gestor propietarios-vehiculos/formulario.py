# =============================================================================
# CAMBIO DEL 22/09/2026 - LA PANTALLA YA NO DECIDE QUE SE VALIDA
#
# QUE SE SACO:
#   el metodo _validar_campos() tenia una sola regla escrita a mano:
#
#       if any(valor == "" for valor in datos.values()):
#           messagebox.showwarning("Error de Validacion",
#                                  "Todos los campos son obligatorios.")
#
#   Se quito porque mostraba siempre el mismo cartel y no decia cual de los
#   campos estaba mal. El caso NO se perdio: ahora es la regla "obligatorio"
#   dentro del diccionario de validaciones (ver entidades.py).
#
# QUE SE AGREGO:
#   1) el parametro validaciones en __init__, con el diccionario de reglas;
#   2) _validar_campos() ahora le pide la lista de errores a validaciones.py,
#      los muestra TODOS juntos (uno por renglon) y deja el cursor parado en
#      el primer campo que fallo.
#
# LO QUE NO CAMBIO:
#   esta clase sigue sin saber que se valida ni como se guarda. Recibe los
#   campos, el repositorio y las reglas, y con eso arma cualquier entidad.
# =============================================================================

import tkinter as tk
from tkinter import ttk, messagebox
from validaciones import validar_datos

class FormularioCRUD(tk.Toplevel):
    """
    Ventana genérica de CRUD. Se reutiliza para cualquier entidad
    (Vehículos, Propietarios, etc.) pasándole distintos `campos` y un
    `repositorio` que sabe cómo guardar esos datos.

    Esta clase NO sabe nada de SQLite: solo llama a
    repositorio.crear/actualizar/eliminar/listar. Así la interfaz queda
    separada de la lógica de conexión a la base de datos.

    Tampoco decide QUÉ se valida: recibe el diccionario `validaciones`
    (clave = nombre del campo, valor = sus reglas) y se lo pasa a
    validaciones.py. Si no se le pasa ninguno, todos los campos se
    toman como obligatorios, que era el comportamiento anterior.
    """
    def __init__(self, parent, titulo, campos, repositorio, validaciones=None):
        super().__init__(parent)
        self.title(titulo)
        self.geometry("700x500")

        self.campos = campos
        self.repositorio = repositorio
        # diccionario clave/valor con las reglas de cada campo
        self.validaciones = validaciones or {}
        self.entradas = {}

        self._crear_formulario()
        self._crear_botones()
        self._crear_tabla()
        self._refrescar_tabla()

        # al cerrar la ventana, cerramos también la conexión a la BD
        self.protocol("WM_DELETE_WINDOW", self._al_cerrar)

    def _crear_formulario(self):
        frame_form = ttk.LabelFrame(self, text="Datos de la Entidad", padding=10)
        frame_form.pack(fill="x", padx=10, pady=5)

        for i, campo in enumerate(self.campos):
            lbl = ttk.Label(frame_form, text=f"{campo}:")
            lbl.grid(row=i, column=0, sticky="w", pady=2, padx=5)

            entry = ttk.Entry(frame_form)
            entry.grid(row=i, column=1, sticky="ew", pady=2, padx=5)
            self.entradas[campo] = entry

        frame_form.columnconfigure(1, weight=1)

    def _crear_botones(self):
        frame_btn = ttk.Frame(self, padding=5)
        frame_btn.pack(fill="x", padx=10)

        ttk.Button(frame_btn, text="Crear", command=self.accion_crear).pack(side="left", padx=5)
        ttk.Button(frame_btn, text="Actualizar", command=self.accion_actualizar).pack(side="left", padx=5)
        ttk.Button(frame_btn, text="Eliminar", command=self.accion_eliminar).pack(side="left", padx=5)
        ttk.Button(frame_btn, text="Limpiar", command=self.limpiar_campos).pack(side="left", padx=5)

    def _crear_tabla(self):
        frame_tabla = ttk.Frame(self, padding=10)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)

        self.tabla = ttk.Treeview(frame_tabla, columns=self.campos, show="headings")
        for campo in self.campos:
            self.tabla.heading(campo, text=campo)
            self.tabla.column(campo, anchor="w", width=120)

        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar_registro)

    def obtener_datos_formulario(self):
        return {campo: entry.get().strip() for campo, entry in self.entradas.items()}

    def limpiar_campos(self):
        for entry in self.entradas.values():
            entry.delete(0, tk.END)
        self.tabla.selection_remove(self.tabla.selection())

    def _validar_campos(self):
        """
        Revisa el formulario antes de guardar.

        SE SACÓ de acá la única regla que había escrita a mano:

            if any(valor == "" for valor in datos.values()):
                messagebox.showwarning("Error de Validación",
                                       "Todos los campos son obligatorios.")

        Se quitó porque avisaba siempre lo mismo y no decía cuál campo
        estaba mal. Ese caso no se perdió: ahora es la regla
        "obligatorio" dentro del diccionario de validaciones.
        """
        datos = self.obtener_datos_formulario()
        errores = validar_datos(datos, self.validaciones)

        if errores:
            # todos los errores juntos, uno por renglón
            texto = "\n".join(mensaje for _, mensaje in errores)
            messagebox.showwarning("Error de Validación", texto, parent=self)
            # el cursor queda parado en el primer campo que falló
            primer_campo = errores[0][0]
            self.entradas[primer_campo].focus_set()
            return None

        return datos

    def _refrescar_tabla(self):
        """Vuelve a leer todas las filas desde la base y las muestra."""
        self.tabla.delete(*self.tabla.get_children())
        for fila in self.repositorio.listar():
            id_registro, *valores = fila
            # usamos el id de la BD como iid del Treeview, así lo recuperamos al seleccionar
            self.tabla.insert("", tk.END, iid=str(id_registro), values=valores)

    def accion_crear(self):
        datos = self._validar_campos()
        if datos:
            self.repositorio.crear(datos)
            self._refrescar_tabla()
            self.limpiar_campos()

    def accion_actualizar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showerror("Error de Selección", "Debe seleccionar un registro de la tabla para actualizar.")
            return

        datos = self._validar_campos()
        if datos:
            id_registro = int(seleccion[0])
            self.repositorio.actualizar(id_registro, datos)
            self._refrescar_tabla()
            self.limpiar_campos()

    def accion_eliminar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showerror("Error de Selección", "Debe seleccionar un registro de la tabla para eliminar.")
            return

        confirmar = messagebox.askyesno("Confirmar eliminación", "¿Seguro que querés eliminar este registro?")
        if not confirmar:
            return

        id_registro = int(seleccion[0])
        self.repositorio.eliminar(id_registro)
        self._refrescar_tabla()
        self.limpiar_campos()

    def _al_seleccionar_registro(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0])
            valores = item["values"]
            for campo, valor in zip(self.campos, valores):
                self.entradas[campo].delete(0, tk.END)
                self.entradas[campo].insert(0, str(valor))

    def _al_cerrar(self):
        self.repositorio.cerrar()
        self.destroy()
# hice cambios al llamar a la clase del formulario, ya que antes era una sola ventana para la gestión de vehiculos.
# ahora se llaman dos ventanas, una para gestionar vehiculos y otra para gestionar propietarios.
#
