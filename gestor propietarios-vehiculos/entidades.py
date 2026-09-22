# Solo datos: aca no se ejecuta nada, no hay ventanas ni base de datos.
#
# Por cada entidad: la lista de campos, y el diccionario de validaciones
# donde CLAVE = el nombre del campo y VALOR = las reglas que debe cumplir.
#
# Reglas que interpreta validaciones.py:
#   obligatorio, tipo ("numero" / "texto" / "alfanumerico"), largo,
#   largo_min, largo_max, minimo, maximo, y mensaje (texto propio; si no
#   se pone, el mensaje se arma solo).

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
