# =============================================================================
# CAMBIO DEL 22/09/2026 - VALIDACIONES CON DICCIONARIO CLAVE-VALOR
#
# QUE SE AGREGO en este archivo:
#   los diccionarios validaciones_vehiculo y validaciones_propietario.
#   En cada uno, la CLAVE es el nombre de un campo del formulario y el VALOR
#   es otro diccionario con las reglas que ese campo tiene que cumplir.
#
# POR QUE ACA:
#   este archivo ya definia QUE campos tiene cada entidad; las reglas de esos
#   campos describen la misma entidad, asi que van en el mismo lugar. Sigue
#   siendo un archivo de datos: no importa tkinter, no importa sqlite3 y no
#   ejecuta nada.
#
# QUIEN LAS USA:
#   main.py se las pasa a la ventana, y validaciones.py es el unico que las
#   interpreta. Para agregar una regla o un campo nuevo alcanza con tocar
#   este archivo: la pantalla no se toca.
# =============================================================================

# Este archivo define QUE tiene cada entidad. Son solo datos: aca no se ejecuta
# nada, no hay ventanas ni base de datos.
#
# Por cada entidad hay dos cosas:
#   - la lista de campos que se muestran en pantalla
#   - el diccionario de validaciones, donde
#         CLAVE = el nombre del campo (escrito igual que en la lista de campos)
#         VALOR = las reglas que ese campo tiene que cumplir
#
# Reglas disponibles (las interpreta validaciones.py):
#   obligatorio -> True si el campo no puede quedar vacio
#   tipo        -> "numero", "texto" o "alfanumerico"
#   largo       -> cantidad exacta de caracteres
#   largo_min   -> cantidad minima de caracteres
#   largo_max   -> cantidad maxima de caracteres
#   minimo      -> valor numerico minimo
#   maximo      -> valor numerico maximo
#   mensaje     -> texto propio a mostrar cuando el campo esta mal
#                  (si no se pone, validaciones.py arma el mensaje solo)

campos_vehiculo = ["Patente", "Marca", "Modelo", "Año"]
# datos de ejemplo, se usan a mano solo durante las pruebas manuales (ver PLAN_DE_PRUEBAS.md)
ejemplo_vehiculos = [["AA123BB", "Toyota", "Corolla", "2021"]]

validaciones_vehiculo = {
    # se aceptan los dos formatos argentinos: ABC123 (6) y AA123BB (7)
    "Patente": {
        "obligatorio": True,
        "tipo": "alfanumerico",
        "largo_min": 6,
        "largo_max": 7,
        "mensaje": "Patente: debe tener 6 o 7 letras y números, sin espacios ni guiones (ABC123 o AA123BB).",
    },
    "Marca": {"obligatorio": True, "tipo": "texto", "largo_min": 2, "largo_max": 30},
    # Modelo no lleva tipo porque hay modelos con letras y numeros mezclados (Corolla XEI, 208, T-Cross)
    "Modelo": {"obligatorio": True, "largo_min": 1, "largo_max": 30},
    "Año": {
        "obligatorio": True,
        "tipo": "numero",
        "largo": 4,
        "minimo": 1900,
        "maximo": 2026,
    },
}

campos_propietario = ["DNI", "Nombre", "Apellido", "Teléfono"]
ejemplo_propietarios = [["40123456", "Juan", "Pérez", "3415551234"]]

validaciones_propietario = {
    "DNI": {
        "obligatorio": True,
        "tipo": "numero",
        "largo_min": 7,
        "largo_max": 8,
        "mensaje": "DNI: debe tener 7 u 8 números, sin puntos.",
    },
    "Nombre": {"obligatorio": True, "tipo": "texto", "largo_min": 2, "largo_max": 30},
    "Apellido": {"obligatorio": True, "tipo": "texto", "largo_min": 2, "largo_max": 30},
    "Teléfono": {
        "obligatorio": True,
        "tipo": "numero",
        "largo_min": 8,
        "largo_max": 15,
        "mensaje": "Teléfono: solo números, entre 8 y 15 dígitos (sin guiones ni espacios).",
    },
}
