"""
Motor de validaciones: recibe lo que escribio el usuario y el diccionario
de reglas, y devuelve la lista de errores.

No importa Tkinter ni SQLite, asi que se puede probar sin abrir ventanas.
"""


def _solo_letras(valor):
    """True si el valor tiene solo letras y espacios (acepta acentos y ñ)."""
    return valor.replace(" ", "").isalpha()


def validar_campo(campo, valor, regla):
    """
    Revisa UN campo contra SU regla (el diccionario de reglas de ese campo).
    Devuelve None si el valor esta bien, o el texto del error si esta mal.
    """
    # 1) vacio: solo importa si es obligatorio; si no, no se revisa nada mas
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
    Revisa TODOS los campos: datos = {campo: valor escrito},
    validaciones = {campo: reglas}.

    Devuelve una lista de pares (campo, error); vacia = todo esta bien.
    Un campo que no figura en el diccionario se toma como obligatorio.
    """
    errores = []
    for campo, valor in datos.items():
        regla = validaciones.get(campo, {"obligatorio": True})
        error = validar_campo(campo, valor, regla)
        if error:
            errores.append((campo, error))
    return errores
