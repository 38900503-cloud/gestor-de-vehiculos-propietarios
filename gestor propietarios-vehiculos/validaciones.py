# =============================================================================
# ARCHIVO NUEVO DEL 22/09/2026 - MOTOR DE VALIDACIONES
#
# QUE HACE:
#   recibe lo que el usuario escribio y el diccionario de reglas de
#   entidades.py, y devuelve la lista de errores. Nada mas que eso.
#
# POR QUE ES UN ARCHIVO APARTE:
#   para que cada archivo tenga un solo trabajo. formulario.py se ocupa de la
#   pantalla, basedatos.py del SQL, entidades.py de los datos de cada entidad
#   y este del control de las reglas. Como no importa tkinter ni sqlite3, se
#   puede probar entero sin abrir una ventana ni tocar la base: eso es lo que
#   hace el script probar-validaciones.py (40 pruebas).
#
# COMO SE AGREGA UNA REGLA NUEVA:
#   se le da un nombre (por ejemplo "largo_min"), se lo agrega al diccionario
#   del campo en entidades.py y se lo revisa en validar_campo(), abajo.
# =============================================================================

"""
Motor de validaciones.

Recibe los datos que escribio el usuario y el diccionario de reglas, y
devuelve la lista de errores.

Este archivo no sabe nada de Tkinter ni de SQLite: no importa ninguno de
los dos. Por eso se puede probar sin abrir una sola ventana.
"""


def _solo_letras(valor):
    """True si el valor tiene solo letras y espacios (acepta acentos y ñ)."""
    return valor.replace(" ", "").isalpha()


def validar_campo(campo, valor, regla):
    """
    Revisa UN campo contra SU regla.

    campo: nombre del campo, se usa para armar el mensaje de error
    valor: lo que escribio el usuario (ya sin espacios al principio ni al final)
    regla: el diccionario de reglas de ESE campo

    Devuelve None si el valor esta bien, o el texto del error si esta mal.
    """
    # 1) campo vacio: solo importa si es obligatorio. Si no lo es, no se
    #    revisa nada mas (no tiene sentido pedirle largo minimo a algo vacio).
    if valor == "":
        if regla.get("obligatorio"):
            return f"{campo}: es obligatorio."
        return None

    # si la regla trae un mensaje propio, se muestra ese en lugar del automatico
    mensaje_propio = regla.get("mensaje")

    # 2) tipo de contenido
    tipo = regla.get("tipo")
    if tipo == "numero" and not valor.isdigit():
        return mensaje_propio or f"{campo}: debe contener solo números."
    if tipo == "texto" and not _solo_letras(valor):
        return mensaje_propio or f"{campo}: debe contener solo letras."
    if tipo == "alfanumerico" and not valor.isalnum():
        return mensaje_propio or f"{campo}: debe contener solo letras y números."

    # 3) largo
    largo = regla.get("largo")
    if largo is not None and len(valor) != largo:
        return mensaje_propio or f"{campo}: debe tener exactamente {largo} caracteres."

    largo_min = regla.get("largo_min")
    if largo_min is not None and len(valor) < largo_min:
        return mensaje_propio or f"{campo}: debe tener al menos {largo_min} caracteres."

    largo_max = regla.get("largo_max")
    if largo_max is not None and len(valor) > largo_max:
        return mensaje_propio or f"{campo}: no puede tener más de {largo_max} caracteres."

    # 4) rango numerico: solo se revisa si el valor es un numero
    if valor.isdigit():
        numero = int(valor)
        minimo = regla.get("minimo")
        if minimo is not None and numero < minimo:
            return mensaje_propio or f"{campo}: no puede ser menor que {minimo}."
        maximo = regla.get("maximo")
        if maximo is not None and numero > maximo:
            return mensaje_propio or f"{campo}: no puede ser mayor que {maximo}."

    return None


def validar_datos(datos, validaciones):
    """
    Revisa TODOS los campos del formulario.

    datos:        {campo: valor escrito por el usuario}
    validaciones: {campo: reglas}  <-- el diccionario clave/valor de entidades.py

    Devuelve una lista de pares (campo, error). Lista vacia = todo esta bien.

    Un campo que no figura en el diccionario de validaciones se toma como
    obligatorio: asi se mantiene el comportamiento que tenia el programa
    antes de existir este archivo, cuando la unica regla era "no vacio".
    """
    errores = []
    for campo, valor in datos.items():
        regla = validaciones.get(campo, {"obligatorio": True})
        error = validar_campo(campo, valor, regla)
        if error:
            errores.append((campo, error))
    return errores
