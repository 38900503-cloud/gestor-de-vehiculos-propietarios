# Gestor de Vehículos y Propietarios

Repositorio: https://github.com/38900503-cloud/gestor-de-vehiculos-propietarios

Sistema de escritorio en **Python + Tkinter** con arquitectura orientada a
objetos: una clase genérica de interfaz gráfica que administra el CRUD
(Crear, Leer, Actualizar, Eliminar) de dos entidades — **Vehículos** y
**Propietarios** — reutilizando el mismo código y variando únicamente los
parámetros de inicialización.

## Integrantes

- Santiago Luna
- Karen Maliandi

**Materia:** Programación (Tkinter) — Prof. Cepeda Leandro

## Requisitos cumplidos

| Requisito | Cómo se resuelve |
|---|---|
| Clase genérica de GUI para 2+ entidades | `FormularioCRUD` (en `formulario.py`) recibe `título`, `campos` y un `repositorio` por parámetro; se instancia igual para Vehículos y Propietarios en `main.py` |
| Generación dinámica de widgets (sin declararlos a mano) | `_crear_formulario` arma Label + Entry con un `for` sobre la lista de campos |
| Gestión del estado con diccionario | `self.entradas = {}` guarda cada Entry usando el nombre del campo como clave |
| Separación entre GUI y lógica de base de datos | `basedatos.py` (clase `RepositorioSQLite`) concentra toda la conexión/SQL; `formulario.py` no importa `sqlite3` ni sabe cómo se persisten los datos |
| Validaciones con diccionario clave-valor | `entidades.py` define `validaciones_vehiculo` y `validaciones_propietario`: la **clave** es el nombre del campo y el **valor** son sus reglas (`obligatorio`, `tipo`, `largo`, `largo_min`, `largo_max`, `minimo`, `maximo`, `mensaje`). `validaciones.py` es el único que interpreta esas reglas |
| Plan de pruebas documentado | Ver [`Plan_de_Pruebas.docx`](Plan_de_Pruebas.docx), con capturas reales de los 17 casos |
| Entrega por repositorio (no zip) | Este mismo repositorio |

## Estructura del proyecto

```
gestor-de-vehiculos-propietarios/
├── gestor propietarios-vehiculos/
│   ├── main.py          # Menú principal, arma un repositorio + formulario por entidad
│   ├── formulario.py     # Clase genérica FormularioCRUD (la interfaz gráfica)
│   ├── basedatos.py      # Clase genérica RepositorioSQLite (persistencia)
│   ├── entidades.py      # Campos y reglas de validación de cada entidad (solo datos)
│   └── validaciones.py   # Motor que interpreta las reglas y devuelve los errores
├── Plan_de_Pruebas.docx        # Plan de pruebas con capturas de pantalla e índice
└── README.md
```

## Cómo ejecutarlo

Requiere Python 3 (Tkinter y sqlite3 vienen incluidos en la instalación
estándar, no hace falta instalar nada más).

```bash
cd "gestor propietarios-vehiculos"
python main.py
```

Se abre un menú con dos botones: **Gestionar Vehículos** y **Gestionar
Propietarios**. Cada uno abre una ventana con formulario, tabla y botones
Crear / Actualizar / Eliminar / Limpiar. Los datos se guardan en un
archivo `datos.db` (SQLite) que se crea automáticamente en esa misma
carpeta la primera vez que se ejecuta.

## Funcionalidades

- CRUD completo para Vehículos (Patente, Marca, Modelo, Año) y
  Propietarios (DNI, Nombre, Apellido, Teléfono).
- Validaciones por campo al crear/actualizar, definidas en un diccionario
  clave-valor: obligatoriedad, tipo de dato (números, letras o
  alfanumérico), largo exacto, largo mínimo y máximo, rango numérico y
  mensaje propio. Se informan todos los errores juntos, uno por renglón, y
  el cursor queda parado en el primer campo que falló.
- Confirmación (Sí/No) antes de eliminar un registro, para evitar borrados
  accidentales.
- Persistencia real en SQLite: los datos no se pierden al cerrar el
  programa.
