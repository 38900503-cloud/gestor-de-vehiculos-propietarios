# -*- coding: utf-8 -*-
"""
Pruebas del motor de validaciones, sin abrir ninguna ventana.

Se corre desde esta misma carpeta:
    python probar-validaciones.py
    python probar-validaciones.py --resumen

No abre ventanas ni toca la base de datos: solo importa entidades.py y
validaciones.py, y compara lo que devuelven contra lo esperado.
"""
import sys   # solo para leer los parametros de la linea de comandos

from entidades import (campos_vehiculo, campos_propietario,
                       validaciones_vehiculo, validaciones_propietario)
from validaciones import validar_campo, validar_datos

ok = 0
fallo = 0
RESUMEN = "--resumen" in sys.argv   # imprime solo el total de cada seccion
secciones = []                      # [nombre, cantidad de pruebas, fallidas]

def seccion(nombre):
    secciones.append([nombre, 0, 0])
    if not RESUMEN:
        print("")
        print("--- " + nombre + " ---")

def probar(descripcion, obtenido, esperado):
    global ok, fallo
    secciones[-1][1] += 1
    if obtenido == esperado:
        ok += 1
        if not RESUMEN:
            print("  OK   | " + descripcion)
    else:
        fallo += 1
        secciones[-1][2] += 1
        print("  FALLA| " + descripcion)
        print("        esperado: " + repr(esperado))
        print("        obtenido: " + repr(obtenido))

def hay_error(datos, reglas, campo):
    """True si ese campo aparece en la lista de errores."""
    return campo in [c for c, _ in validar_datos(datos, reglas)]

def vehiculo(patente="AA123BB", marca="Toyota", modelo="Corolla", anio="2021"):
    return {"Patente": patente, "Marca": marca, "Modelo": modelo, "A\u00f1o": anio}

def propietario(dni="40123456", nombre="Juan", apellido="P\u00e9rez", tel="3415551234"):
    return {"DNI": dni, "Nombre": nombre, "Apellido": apellido, "Tel\u00e9fono": tel}

seccion("1. el diccionario esta bien armado")
probar("las claves de validaciones_vehiculo son los campos de vehiculo",
       list(validaciones_vehiculo), campos_vehiculo)
probar("las claves de validaciones_propietario son los campos de propietario",
       list(validaciones_propietario), campos_propietario)

seccion("2. casos validos: no dan ningun error")
probar("vehiculo correcto", validar_datos(vehiculo(), validaciones_vehiculo), [])
probar("patente vieja de 6 (ABC123)",
       validar_datos(vehiculo(patente="ABC123"), validaciones_vehiculo), [])
probar("propietario correcto",
       validar_datos(propietario(), validaciones_propietario), [])
probar("apellido con acento (Perez con tilde)",
       validar_datos(propietario(apellido="P\u00e9rez"), validaciones_propietario), [])
probar("nombre compuesto con espacio (Juan Carlos)",
       validar_datos(propietario(nombre="Juan Carlos"), validaciones_propietario), [])
probar("DNI con cero adelante (01234567) se acepta",
       validar_datos(propietario(dni="01234567"), validaciones_propietario), [])

seccion("3. obligatorio")
probar("patente vacia da error", hay_error(vehiculo(patente=""), validaciones_vehiculo, "Patente"), True)
probar("modelo vacio da error", hay_error(vehiculo(modelo=""), validaciones_vehiculo, "Modelo"), True)
probar("los 4 campos vacios dan 4 errores",
       len(validar_datos(vehiculo("", "", "", ""), validaciones_vehiculo)), 4)
probar("solo espacios cuenta como vacio (el formulario ya hace strip)",
       validar_campo("Marca", "", validaciones_vehiculo["Marca"]),
       "Marca: es obligatorio.")

seccion("4. tipo de dato")
probar("anio con letras da error", hay_error(vehiculo(anio="20x1"), validaciones_vehiculo, "A\u00f1o"), True)
probar("marca con numeros da error", hay_error(vehiculo(marca="Toyota2"), validaciones_vehiculo, "Marca"), True)
probar("patente con guion da error", hay_error(vehiculo(patente="AA-123B"), validaciones_vehiculo, "Patente"), True)
probar("patente con espacio da error", hay_error(vehiculo(patente="AA 123B"), validaciones_vehiculo, "Patente"), True)
probar("DNI con puntos da error", hay_error(propietario(dni="40.123.456"), validaciones_propietario, "DNI"), True)
probar("telefono con guion da error", hay_error(propietario(tel="341-555-1234"), validaciones_propietario, "Tel\u00e9fono"), True)
probar("nombre con numeros da error", hay_error(propietario(nombre="Juan1"), validaciones_propietario, "Nombre"), True)
probar("modelo SI acepta numeros (no tiene regla de tipo)",
       validar_datos(vehiculo(modelo="T-Cross 200"), validaciones_vehiculo), [])

seccion("5. largo")
probar("patente de 5 da error", hay_error(vehiculo(patente="AB123"), validaciones_vehiculo, "Patente"), True)
probar("patente de 8 da error", hay_error(vehiculo(patente="AA123BBC"), validaciones_vehiculo, "Patente"), True)
probar("marca de 1 letra da error", hay_error(vehiculo(marca="T"), validaciones_vehiculo, "Marca"), True)
probar("marca de 31 letras da error", hay_error(vehiculo(marca="A"*31), validaciones_vehiculo, "Marca"), True)
probar("anio de 3 digitos da error", hay_error(vehiculo(anio="202"), validaciones_vehiculo, "A\u00f1o"), True)
probar("DNI de 6 digitos da error", hay_error(propietario(dni="123456"), validaciones_propietario, "DNI"), True)
probar("DNI de 9 digitos da error", hay_error(propietario(dni="123456789"), validaciones_propietario, "DNI"), True)
probar("telefono de 7 digitos da error", hay_error(propietario(tel="1234567"), validaciones_propietario, "Tel\u00e9fono"), True)

seccion("6. rango numerico")
probar("anio 1899 da error", hay_error(vehiculo(anio="1899"), validaciones_vehiculo, "A\u00f1o"), True)
probar("anio 1900 se acepta", validar_datos(vehiculo(anio="1900"), validaciones_vehiculo), [])
probar("anio 2026 se acepta", validar_datos(vehiculo(anio="2026"), validaciones_vehiculo), [])
probar("anio 2027 da error", hay_error(vehiculo(anio="2027"), validaciones_vehiculo, "A\u00f1o"), True)

seccion("7. mensajes")
probar("la patente usa el mensaje propio del diccionario",
       validar_campo("Patente", "AA-123", validaciones_vehiculo["Patente"]),
       validaciones_vehiculo["Patente"]["mensaje"])
probar("la marca usa el mensaje automatico",
       validar_campo("Marca", "T", validaciones_vehiculo["Marca"]),
       "Marca: debe tener al menos 2 caracteres.")
probar("el anio fuera de rango avisa el maximo",
       validar_campo("A\u00f1o", "2030", validaciones_vehiculo["A\u00f1o"]),
       "A\u00f1o: no puede ser mayor que 2026.")

seccion("8. comportamiento por defecto")
probar("un campo sin reglas propias sigue siendo obligatorio",
       validar_datos({"Color": ""}, {}), [("Color", "Color: es obligatorio.")])
probar("un campo sin reglas propias con valor no da error",
       validar_datos({"Color": "rojo"}, {}), [])
probar("campo no obligatorio y vacio no se revisa",
       validar_campo("Alias", "", {"obligatorio": False, "largo_min": 5}), None)

seccion("9. se informan TODOS los errores, no solo el primero")
errores = validar_datos(vehiculo(patente="X", marca="1", modelo="", anio="abc"), validaciones_vehiculo)
probar("4 campos mal = 4 mensajes", len(errores), 4)
probar("el primer error es el de Patente (para parar el cursor ahi)", errores[0][0], "Patente")

print("")
print("=" * 64)
print("  RESUMEN DE LAS PRUEBAS DEL MOTOR DE VALIDACION")
print("=" * 64)
for nombre, cantidad, fallidas in secciones:
    estado = "OK" if fallidas == 0 else "{} FALLIDAS".format(fallidas)
    print("  {:<44} {:>3} pruebas   {}".format(nombre, cantidad, estado))
print("=" * 64)
print("  TOTAL: {} pruebas  ->  {} OK / {} FALLIDAS".format(ok + fallo, ok, fallo))
print("=" * 64)
