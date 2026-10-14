# Pruebas del programa del consultorio. Se ejecuta con:  python pruebas.py
# Carga las funciones de consultorio.py sin arrancar el menu.

codigo = open("consultorio.py", encoding="utf-8").read()
codigo = codigo[:codigo.rindex("principal()")]
exec(codigo)

correctas = 0
total = 0


def probar(nombre, obtenido, esperado):
    global correctas, total
    total = total + 1
    if obtenido == esperado:
        correctas = correctas + 1
    else:
        print("FALLA", nombre, "- esperado", esperado, "- obtenido", obtenido)


# ---- funciones de calculo
probar("posicion dia 1 turno 1", posicion(1, 1), 0)
probar("posicion dia 2 turno 1", posicion(2, 1), 16)
probar("posicion dia 20 turno 16", posicion(20, 16), 319)
probar("hora turno 1", hora_del_turno(1), "8:00")
probar("hora turno 4", hora_del_turno(4), "9:30")
probar("hora turno 16", hora_del_turno(16), "15:30")
probar("dni correcto", dni_valido("45871236"), True)
probar("dni que empieza con 0", dni_valido("09874563"), True)
probar("dni de 7 digitos", dni_valido("4102587"), False)
probar("dni con letra", dni_valido("4587123A"), False)
probar("dni vacio", dni_valido(""), False)
probar("celular correcto", celular_valido("987654321"), True)
probar("celular corto", celular_valido("98765"), False)
probar("edad correcta", edad_valida("70"), True)
probar("edad fuera de rango", edad_valida("150"), False)
probar("edad con letras", edad_valida("abc"), False)
probar("tipo P", tipo_valido("P"), True)
probar("tipo X", tipo_valido("X"), False)
probar("ocultar dni", ocultar_dni("45871236"), "****1236")
probar("cobro particular", calcular_cobro("P", 34), 80.0)
probar("cobro particular de 64", calcular_cobro("P", 64), 80.0)
probar("cobro particular de 65", calcular_cobro("P", 65), 64.0)
probar("cobro control", calcular_cobro("C", 40), 40.0)
probar("cobro control de 70", calcular_cobro("C", 70), 40.0)
probar("cobro seguro", calcular_cobro("S", 70), 20.0)
probar("porcentaje", porcentaje(6, 16), 37.5)
probar("porcentaje con total cero", porcentaje(0, 0), 0.0)

# ---- agenda de ejemplo
tam = DIAS_DEL_MES * TURNOS_DEL_DIA
dnis = [""] * tam
nombres = [""] * tam
celulares = [""] * tam
tipos = [""] * tam
edades = [0] * tam
asistencias = [""] * tam
cargar_ejemplo(dnis, nombres, celulares, tipos, edades, asistencias)

probar("libres dia 1", contar_libres(dnis, 1), 10)
probar("libres dia vacio", contar_libres(dnis, 10), 16)
probar("turnos libres dia 1", turnos_libres(dnis, 1), [0, 0, 0, 0, 0, 0, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
probar("paciente conocido", nombres[buscar_paciente(dnis, "41025874")], "Maria Quispe")
probar("paciente nuevo", buscar_paciente(dnis, "11111111"), -1)
probar("buscar por nombre", buscar_en_dia(dnis, nombres, 3, "Mario"), 2)
probar("buscar por dni", buscar_en_dia(dnis, nombres, 3, "09988776"), 5)
probar("buscar a quien no esta", buscar_en_dia(dnis, nombres, 3, "Zoila"), 0)

# ---- cierre del dia 1: 6 citas, 4 atendidos, 2 faltas
probar("cierre dia 1", calcular_cierre(dnis, tipos, edades, asistencias, 1), [6, 4, 2, 184.0, 120.0, 120.0])
probar("cierre dia sin citas", calcular_cierre(dnis, tipos, edades, asistencias, 10), [0, 0, 0, 0.0, 0.0, 0.0])
probar("cierre dia sin marcar", calcular_cierre(dnis, tipos, edades, asistencias, 3), [3, 0, 0, 0.0, 0.0, 0.0])
probar("resumen del mes", resumen_mes(dnis, tipos, edades, asistencias), [3, 13, 7, 3, 308.0, 180.0, 200.0])
probar("deuda de la aseguradora", total_seguros(tipos, asistencias), 180.0)

# ---- reservar, mover y cancelar
guardar_cita(dnis, nombres, celulares, tipos, edades, asistencias, posicion(5, 2), "12345678", "Sara Lopez", "911222333", "P", 40, "-")
probar("cita guardada", nombres[posicion(5, 2)], "Sara Lopez")
probar("libres despues de reservar", contar_libres(dnis, 5), 15)
borrar_cita(dnis, nombres, celulares, tipos, edades, asistencias, posicion(5, 2))
probar("turno libre despues de cancelar", dnis[posicion(5, 2)], "")
probar("libres despues de cancelar", contar_libres(dnis, 5), 16)

print("Pruebas correctas:", correctas, "de", total)
