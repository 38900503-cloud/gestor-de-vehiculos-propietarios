import sqlite3


class RepositorioSQLite:
    """
    Repositorio genérico: sabe guardar/leer/actualizar/borrar filas de UNA
    tabla en SQLite. 

    Se instancia igual que FormularioCRUD: pasándole el nombre de la tabla
    y la lista de campos. Así se reutiliza para Vehículos y Propietarios
    sin escribir SQL distinto para cada uno.
    """

    def __init__(self, nombre_tabla, campos, archivo_db="datos.db"):
        self.nombre_tabla = nombre_tabla
        self.campos = campos
        self.conexion = sqlite3.connect(archivo_db)
        self._crear_tabla()

    def _crear_tabla(self):
        columnas = ", ".join(f'"{campo}" TEXT' for campo in self.campos)
        self.conexion.execute(
            f'CREATE TABLE IF NOT EXISTS "{self.nombre_tabla}" '
            f'(id INTEGER PRIMARY KEY AUTOINCREMENT, {columnas})'
        )
        self.conexion.commit()

    def listar(self):
        """Devuelve todas las filas como (id, valor_campo1, valor_campo2, ...)."""
        columnas = ", ".join(f'"{campo}"' for campo in self.campos)
        cursor = self.conexion.execute(f'SELECT id, {columnas} FROM "{self.nombre_tabla}"')
        return cursor.fetchall()

    def crear(self, datos):
        """datos: dict {campo: valor}. Devuelve el id generado."""
        columnas = ", ".join(f'"{campo}"' for campo in self.campos)
        signos = ", ".join("?" for _ in self.campos)
        valores = [datos[campo] for campo in self.campos]
        cursor = self.conexion.execute(
            f'INSERT INTO "{self.nombre_tabla}" ({columnas}) VALUES ({signos})', valores
        )
        self.conexion.commit()
        return cursor.lastrowid

    def actualizar(self, id_registro, datos):
        set_columnas = ", ".join(f'"{campo}" = ?' for campo in self.campos)
        valores = [datos[campo] for campo in self.campos] + [id_registro]
        self.conexion.execute(
            f'UPDATE "{self.nombre_tabla}" SET {set_columnas} WHERE id = ?', valores
        )
        self.conexion.commit()

    def eliminar(self, id_registro):
        self.conexion.execute(f'DELETE FROM "{self.nombre_tabla}" WHERE id = ?', (id_registro,))
        self.conexion.commit()

    def cerrar(self):
        self.conexion.close()
