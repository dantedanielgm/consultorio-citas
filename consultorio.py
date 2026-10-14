# Consultorio: registro de citas y cierre diario de caja.
# Trabajo final de Fundamentos de Programacion 1 (NRC 631).

from datetime import date

PRECIO_PARTICULAR = 80.0
PRECIO_CONTROL = 40.0
COPAGO_SEGURO = 20.0
DEUDA_SEGURO = 60.0
DESCUENTO_MAYOR = 0.20
EDAD_ADULTO_MAYOR = 65
TURNOS_DEL_DIA = 16
DIAS_DEL_MES = 31
DIAS_SEMANA = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "setiembre", "octubre", "noviembre", "diciembre"]


# funciones de calculo

def nombre_de_fecha(fecha):
    # 14/10/2026 se muestra como "miercoles 14 de octubre"
    return DIAS_SEMANA[fecha.weekday()] + " " + str(fecha.day) + " de " + MESES[fecha.month - 1]


def es_laborable(fecha):
    # weekday() da 0 el lunes y 6 el domingo: se atiende de lunes a viernes
    return fecha.weekday() < 5


def fecha_del_dia(dia):
    # el dia del mes actual como fecha real
    hoy = date.today()
    return date(hoy.year, hoy.month, dia)


def nombre_del_dia(dia):
    return nombre_de_fecha(fecha_del_dia(dia))


def es_dia_laborable(dia):
    return es_laborable(fecha_del_dia(dia))


def dias_del_mes_actual():
    # cuantos dias tiene este mes: resta el primero de este mes al primero del siguiente
    hoy = date.today()
    if hoy.month == 12:
        siguiente = date(hoy.year + 1, 1, 1)
    else:
        siguiente = date(hoy.year, hoy.month + 1, 1)
    return (siguiente - date(hoy.year, hoy.month, 1)).days


def posicion(dia, turno):
    # en que casillero de la agenda va el turno
    return (dia - 1) * TURNOS_DEL_DIA + (turno - 1)


def hora_del_turno(turno):
    # el turno 1 es a las 8:00 y cada turno dura 30 minutos
    minutos = 8 * 60 + (turno - 1) * 30
    hora = minutos // 60
    resto = minutos % 60
    if resto < 10:
        texto = str(hora) + ":0" + str(resto)
    else:
        texto = str(hora) + ":" + str(resto)
    return texto


def es_numero(texto):
    # revisa que todo sean numeros
    if len(texto) == 0:
        return False
    for i in range(0, len(texto), 1):
        letra = texto[i:i + 1]
        if letra < "0" or letra > "9":
            return False
    return True


def dni_valido(dni):
    return len(dni) == 8 and es_numero(dni)


def celular_valido(celular):
    return len(celular) == 9 and es_numero(celular)


def edad_valida(texto):
    return es_numero(texto) and int(texto) <= 120


def tipo_valido(tipo):
    return tipo == "P" or tipo == "S" or tipo == "C"


def ocultar_dni(dni):
    # solo se ven los ultimos 4 numeros
    return "****" + dni[4:8]


def calcular_cobro(tipo, edad):
    if tipo == "S":
        cobro = COPAGO_SEGURO
    elif tipo == "C":
        cobro = PRECIO_CONTROL
    else:
        cobro = PRECIO_PARTICULAR
        if edad >= EDAD_ADULTO_MAYOR:
            cobro = cobro - cobro * DESCUENTO_MAYOR
    return cobro


def contar_libres(dnis, dia):
    libres = 0
    for turno in range(1, TURNOS_DEL_DIA + 1, 1):
        if dnis[posicion(dia, turno)] == "":
            libres = libres + 1
    return libres


def turnos_libres(dnis, dia):
    # 0 si el turno esta ocupado
    mi_arreglo = [0] * TURNOS_DEL_DIA
    for turno in range(1, TURNOS_DEL_DIA + 1, 1):
        if dnis[posicion(dia, turno)] == "":
            mi_arreglo[turno - 1] = turno
    return mi_arreglo


def buscar_paciente(dnis, dni):
    # -1 si es paciente nuevo
    encontrado = -1
    for pos in range(0, len(dnis), 1):
        if dnis[pos] == dni:
            encontrado = pos
    return encontrado


def buscar_en_dia(dnis, nombres, dia, texto):
    # busca por DNI o por nombre, 0 si no esta
    encontrado = 0
    for turno in range(1, TURNOS_DEL_DIA + 1, 1):
        pos = posicion(dia, turno)
        if dnis[pos] != "" and encontrado == 0:
            if dnis[pos] == texto or nombres[pos][0:len(texto)] == texto:
                encontrado = turno
    return encontrado


def calcular_cierre(dnis, tipos, edades, asistencias, dia):
    # cierre de caja de un dia
    agendadas = 0
    atendidos = 0
    faltas = 0
    caja = 0.0
    seguros = 0.0
    perdido = 0.0
    for turno in range(1, TURNOS_DEL_DIA + 1, 1):
        pos = posicion(dia, turno)
        if dnis[pos] != "":
            agendadas = agendadas + 1
            cobro = calcular_cobro(tipos[pos], edades[pos])
            deuda = 0.0
            if tipos[pos] == "S":
                deuda = DEUDA_SEGURO
            if asistencias[pos] == "S":
                atendidos = atendidos + 1
                caja = caja + cobro
                seguros = seguros + deuda
            elif asistencias[pos] == "N":
                faltas = faltas + 1
                perdido = perdido + cobro + deuda
    resultado = [agendadas, atendidos, faltas, caja, seguros, perdido]
    return resultado


def porcentaje(parte, total):
    if total == 0:
        return 0.0
    return parte / total * 100


def resumen_mes(dnis, tipos, edades, asistencias):
    # suma todos los dias del mes
    resumen = [0, 0, 0, 0, 0.0, 0.0, 0.0]
    for dia in range(1, DIAS_DEL_MES + 1, 1):
        cierre = calcular_cierre(dnis, tipos, edades, asistencias, dia)
        if cierre[0] > 0:
            resumen[0] = resumen[0] + 1
            for i in range(0, len(cierre), 1):
                resumen[i + 1] = resumen[i + 1] + cierre[i]
    return resumen


def total_seguros(tipos, asistencias):
    # 60 soles por cada asegurado atendido
    total = 0.0
    for pos in range(0, len(tipos), 1):
        if tipos[pos] == "S" and asistencias[pos] == "S":
            total = total + DEUDA_SEGURO
    return total


def guardar_cita(dnis, nombres, celulares, tipos, edades, asistencias, pos, dni, nombre, celular, tipo, edad, asistencia):
    dnis[pos] = dni
    nombres[pos] = nombre
    celulares[pos] = celular
    tipos[pos] = tipo
    edades[pos] = edad
    asistencias[pos] = asistencia


def borrar_cita(dnis, nombres, celulares, tipos, edades, asistencias, pos):
    guardar_cita(dnis, nombres, celulares, tipos, edades, asistencias, pos, "", "", "", "", 0, "")


# funciones para pedir datos

def pedir_numero(mensaje, minimo, maximo):
    texto = input(mensaje)
    while not (es_numero(texto) and int(texto) >= minimo and int(texto) <= maximo):
        print("  Escriba un numero entre", minimo, "y", maximo)
        texto = input(mensaje)
    return int(texto)


def pedir_dia_de_cita(hoy):
    # solo desde hoy hasta fin de mes, y de lunes a viernes
    ultimo = dias_del_mes_actual()
    mensaje = "Dia que pide el paciente (" + str(hoy) + " a " + str(ultimo) + "): "
    dia = pedir_numero(mensaje, hoy, ultimo)
    while not es_dia_laborable(dia):
        print("  El", nombre_del_dia(dia), "el consultorio esta cerrado")
        dia = pedir_numero(mensaje, hoy, ultimo)
    return dia


def pedir_dni():
    dni = input("DNI: ")
    while not dni_valido(dni):
        print("  El DNI debe tener 8 digitos")
        dni = input("DNI: ")
    return dni


def pedir_nombre():
    nombre = input("Nombre: ")
    while nombre == "":
        print("  El nombre no puede quedar vacio")
        nombre = input("Nombre: ")
    return nombre


def pedir_celular():
    celular = input("Celular: ")
    while not celular_valido(celular):
        print("  El celular debe tener 9 digitos")
        celular = input("Celular: ")
    return celular


def pedir_tipo():
    tipo = input("Tipo (P particular, C control, S seguro): ")
    while not tipo_valido(tipo):
        print("  Escriba P, C o S")
        tipo = input("Tipo (P particular, C control, S seguro): ")
    return tipo


def pedir_letra(mensaje, primera, segunda):
    letra = input(mensaje)
    while letra != primera and letra != segunda:
        print("  Escriba", primera, "o", segunda)
        letra = input(mensaje)
    return letra


# opciones del menu

def mostrar_dia(dnis, nombres, asistencias, dia):
    print(nombre_del_dia(dia), "- libres:", contar_libres(dnis, dia), "de", TURNOS_DEL_DIA)
    for turno in range(1, TURNOS_DEL_DIA + 1, 1):
        pos = posicion(dia, turno)
        if dnis[pos] == "":
            print(" ", turno, hora_del_turno(turno), "libre")
        else:
            print(" ", turno, hora_del_turno(turno), nombres[pos], ocultar_dni(dnis[pos]), asistencias[pos])


def reservar(dnis, nombres, celulares, tipos, edades, asistencias, hoy):
    # HU01 Reservar una cita
    dia = pedir_dia_de_cita(hoy)
    while contar_libres(dnis, dia) == 0:
        print("  Ese dia esta lleno. Ofrezca otro dia.")
        dia = pedir_dia_de_cita(hoy)
    print("Turnos libres:", turnos_libres(dnis, dia))
    turno = pedir_numero("Turno elegido: ", 1, TURNOS_DEL_DIA)
    while dnis[posicion(dia, turno)] != "":
        print("  Ese turno esta ocupado")
        turno = pedir_numero("Turno elegido: ", 1, TURNOS_DEL_DIA)
    dni = pedir_dni()
    anterior = buscar_paciente(dnis, dni)
    if anterior != -1:
        nombre = nombres[anterior]
        celular = celulares[anterior]
        edad = edades[anterior]
        print("Paciente conocido:", nombre, "- celular", celular, "- edad", edad)
    else:
        nombre = pedir_nombre()
        celular = pedir_celular()
        edad = pedir_numero("Edad: ", 0, 120)
    tipo = pedir_tipo()
    pos = posicion(dia, turno)
    guardar_cita(dnis, nombres, celulares, tipos, edades, asistencias, pos, dni, nombre, celular, tipo, edad, "-")
    print("Cita reservada:", nombre_del_dia(dia), "a las", hora_del_turno(turno), "- pagara S/", calcular_cobro(tipo, edad))


def atender(dnis, nombres, tipos, edades, asistencias, hoy):
    # HU02 Atender al paciente que llega
    texto = input("Nombre o DNI del paciente: ")
    turno = buscar_en_dia(dnis, nombres, hoy, texto)
    if turno == 0:
        print("  No esta en la agenda de hoy")
    else:
        pos = posicion(hoy, turno)
        cobro = calcular_cobro(tipos[pos], edades[pos])
        print(nombres[pos], ocultar_dni(dnis[pos]), "- turno de las", hora_del_turno(turno))
        print("Debe pagar S/", cobro)
        if tipos[pos] == "S":
            print("Se anotan S/", DEUDA_SEGURO, "que debe la aseguradora")
        asistencias[pos] = "S"
        print("Asistencia marcada")


def reprogramar(dnis, nombres, celulares, tipos, edades, asistencias, hoy):
    # HU03 Reprogramar o cancelar una cita
    dia = pedir_numero("Dia de la cita (1 a " + str(dias_del_mes_actual()) + "): ", 1, dias_del_mes_actual())
    turno = pedir_numero("Turno de la cita: ", 1, TURNOS_DEL_DIA)
    pos = posicion(dia, turno)
    if dnis[pos] == "":
        print("  En ese turno no hay ninguna cita")
    else:
        accion = pedir_letra("M para mover, C para cancelar: ", "M", "C")
        if accion == "M":
            nuevo_dia = pedir_dia_de_cita(hoy)
            nuevo_turno = pedir_numero("Nuevo turno: ", 1, TURNOS_DEL_DIA)
            while dnis[posicion(nuevo_dia, nuevo_turno)] != "":
                print("  Ese turno esta ocupado. Elija otro.")
                nuevo_dia = pedir_dia_de_cita(hoy)
                nuevo_turno = pedir_numero("Nuevo turno: ", 1, TURNOS_DEL_DIA)
            destino = posicion(nuevo_dia, nuevo_turno)
            guardar_cita(dnis, nombres, celulares, tipos, edades, asistencias, destino,
                         dnis[pos], nombres[pos], celulares[pos], tipos[pos], edades[pos], "-")
            print("Cita movida al", nombre_del_dia(nuevo_dia), "a las", hora_del_turno(nuevo_turno))
        else:
            print("Cita cancelada. El turno queda libre.")
        borrar_cita(dnis, nombres, celulares, tipos, edades, asistencias, pos)


def cerrar_caja(dnis, nombres, tipos, edades, asistencias, hoy):
    # HU04 Cierre de caja del dia
    for turno in range(1, TURNOS_DEL_DIA + 1, 1):
        pos = posicion(hoy, turno)
        if dnis[pos] != "" and asistencias[pos] == "-":
            print("Sin marcar:", hora_del_turno(turno), nombres[pos])
            asistencias[pos] = pedir_letra("  Asistio? (S o N): ", "S", "N")
    cierre = calcular_cierre(dnis, tipos, edades, asistencias, hoy)
    print("CIERRE DEL", nombre_del_dia(hoy).upper())
    print("Atendidos:", cierre[1], "- Inasistencias:", cierre[2])
    print("Dinero en caja: S/", cierre[3])
    print("Por cobrar a la aseguradora: S/", cierre[4])


def indicadores(dnis, tipos, edades, asistencias, hoy):
    # HU05 Indicadores del dia y del mes
    cierre = calcular_cierre(dnis, tipos, edades, asistencias, hoy)
    print("HOY - ocupacion:", round(porcentaje(cierre[0], TURNOS_DEL_DIA), 1), "%")
    print("HOY - inasistencia:", round(porcentaje(cierre[2], cierre[1] + cierre[2]), 1), "%")
    print("HOY - ingreso perdido: S/", cierre[5])
    mes = resumen_mes(dnis, tipos, edades, asistencias)
    print("MES - dias con citas:", mes[0])
    print("MES - ocupacion:", round(porcentaje(mes[1], mes[0] * TURNOS_DEL_DIA), 1), "%")
    print("MES - inasistencia:", round(porcentaje(mes[3], mes[2] + mes[3]), 1), "%")
    print("MES - ingreso perdido: S/", mes[6])


def reporte_aseguradora(dnis, nombres, tipos, asistencias, estado):
    # HU06 Reporte mensual para la aseguradora
    print("ASEGURADOS ATENDIDOS EN EL MES")
    for dia in range(1, DIAS_DEL_MES + 1, 1):
        for turno in range(1, TURNOS_DEL_DIA + 1, 1):
            pos = posicion(dia, turno)
            if tipos[pos] == "S" and asistencias[pos] == "S":
                print(" ", nombre_del_dia(dia), hora_del_turno(turno), nombres[pos], ocultar_dni(dnis[pos]), "S/", DEUDA_SEGURO)
    print("Total que debe la aseguradora: S/", total_seguros(tipos, asistencias))
    print("Estado del reporte:", estado)
    accion = input("E para marcarlo enviado, C para marcarlo cobrado, Enter para seguir: ")
    if accion == "E":
        estado = "enviado"
    elif accion == "C":
        estado = "cobrado"
    return estado


def cargar_ejemplo(dnis, nombres, celulares, tipos, edades, asistencias, dia_sin_marcar):
    # pacientes de ejemplo
    guardar_cita(dnis, nombres, celulares, tipos, edades, asistencias, posicion(1, 1), "45871236", "Ana Torres", "987654321", "P", 34, "S")
    guardar_cita(dnis, nombres, celulares, tipos, edades, asistencias, posicion(1, 2), "09874563", "Luis Paredes", "912345678", "P", 70, "S")
    guardar_cita(dnis, nombres, celulares, tipos, edades, asistencias, posicion(1, 3), "41025874", "Maria Quispe", "934567812", "S", 45, "S")
    guardar_cita(dnis, nombres, celulares, tipos, edades, asistencias, posicion(1, 4), "70123456", "Jorge Salas", "956781234", "S", 29, "S")
    guardar_cita(dnis, nombres, celulares, tipos, edades, asistencias, posicion(1, 5), "44556677", "Rosa Medina", "945612378", "P", 51, "N")
    guardar_cita(dnis, nombres, celulares, tipos, edades, asistencias, posicion(1, 6), "10203040", "Pedro Rojas", "978123456", "C", 62, "N")
    guardar_cita(dnis, nombres, celulares, tipos, edades, asistencias, posicion(2, 1), "41025874", "Maria Quispe", "934567812", "C", 45, "S")
    guardar_cita(dnis, nombres, celulares, tipos, edades, asistencias, posicion(2, 3), "72345678", "Carla Rios", "923456781", "S", 38, "S")
    guardar_cita(dnis, nombres, celulares, tipos, edades, asistencias, posicion(2, 4), "08765432", "Elena Vargas", "967812345", "P", 66, "S")
    guardar_cita(dnis, nombres, celulares, tipos, edades, asistencias, posicion(2, 7), "46789012", "Diego Luna", "989012345", "P", 27, "N")
    guardar_cita(dnis, nombres, celulares, tipos, edades, asistencias, posicion(dia_sin_marcar, 1), "45871236", "Ana Torres", "987654321", "C", 34, "-")
    guardar_cita(dnis, nombres, celulares, tipos, edades, asistencias, posicion(dia_sin_marcar, 2), "73456789", "Mario Campos", "990123456", "S", 58, "-")
    guardar_cita(dnis, nombres, celulares, tipos, edades, asistencias, posicion(dia_sin_marcar, 5), "09988776", "Julia Ramos", "901234567", "P", 72, "-")


def probar(nombre, obtenido, esperado):
    # 1 si salio bien, 0 si fallo
    if obtenido == esperado:
        return 1
    print("  FALLA", nombre, "- esperado", esperado, "- obtenido", obtenido)
    return 0


def pruebas():
    # opcion 8: prueba las funciones con datos que ya conocemos
    ok = 0
    # funciones de calculo
    ok = ok + probar("posicion dia 1 turno 1", posicion(1, 1), 0)
    ok = ok + probar("posicion dia 2 turno 1", posicion(2, 1), 16)
    ok = ok + probar("posicion dia 31 turno 16", posicion(31, 16), 495)
    ok = ok + probar("hora turno 1", hora_del_turno(1), "8:00")
    ok = ok + probar("nombre de una fecha", nombre_de_fecha(date(2026, 10, 14)), "miercoles 14 de octubre")
    ok = ok + probar("hora turno 16", hora_del_turno(16), "15:30")
    ok = ok + probar("dni correcto", dni_valido("45871236"), True)
    ok = ok + probar("dni que empieza con 0", dni_valido("09874563"), True)
    ok = ok + probar("dni de 7 digitos", dni_valido("4102587"), False)
    ok = ok + probar("dni con letra", dni_valido("4587123A"), False)
    ok = ok + probar("dni vacio", dni_valido(""), False)
    ok = ok + probar("celular correcto", celular_valido("987654321"), True)
    ok = ok + probar("domingo cerrado", es_laborable(date(2026, 10, 18)), False)
    ok = ok + probar("edad correcta", edad_valida("70"), True)
    ok = ok + probar("edad fuera de rango", edad_valida("150"), False)
    ok = ok + probar("edad con letras", edad_valida("abc"), False)
    ok = ok + probar("tipo P", tipo_valido("P"), True)
    ok = ok + probar("viernes abierto", es_laborable(date(2026, 10, 16)), True)
    ok = ok + probar("ocultar dni", ocultar_dni("45871236"), "****1236")
    ok = ok + probar("cobro particular", calcular_cobro("P", 34), 80.0)
    ok = ok + probar("cobro particular de 64", calcular_cobro("P", 64), 80.0)
    ok = ok + probar("cobro particular de 65", calcular_cobro("P", 65), 64.0)
    ok = ok + probar("cobro control", calcular_cobro("C", 40), 40.0)
    ok = ok + probar("cobro control de 70", calcular_cobro("C", 70), 40.0)
    ok = ok + probar("cobro seguro", calcular_cobro("S", 70), 20.0)
    ok = ok + probar("porcentaje", porcentaje(6, 16), 37.5)
    ok = ok + probar("porcentaje con total cero", porcentaje(0, 0), 0.0)

    # agenda aparte, para no tocar la del dia
    tam = DIAS_DEL_MES * TURNOS_DEL_DIA
    dnis = [""] * tam
    nombres = [""] * tam
    celulares = [""] * tam
    tipos = [""] * tam
    edades = [0] * tam
    asistencias = [""] * tam
    cargar_ejemplo(dnis, nombres, celulares, tipos, edades, asistencias, 3)

    ok = ok + probar("libres dia 1", contar_libres(dnis, 1), 10)
    ok = ok + probar("libres dia vacio", contar_libres(dnis, 10), 16)
    ok = ok + probar("turnos libres dia 1", turnos_libres(dnis, 1), [0, 0, 0, 0, 0, 0, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
    ok = ok + probar("paciente conocido", nombres[buscar_paciente(dnis, "41025874")], "Maria Quispe")
    ok = ok + probar("paciente nuevo", buscar_paciente(dnis, "11111111"), -1)
    ok = ok + probar("buscar por nombre", buscar_en_dia(dnis, nombres, 3, "Mario"), 2)
    ok = ok + probar("buscar por dni", buscar_en_dia(dnis, nombres, 3, "09988776"), 5)
    ok = ok + probar("buscar a quien no esta", buscar_en_dia(dnis, nombres, 3, "Zoila"), 0)

    # cierre del dia 1
    ok = ok + probar("cierre dia 1", calcular_cierre(dnis, tipos, edades, asistencias, 1), [6, 4, 2, 184.0, 120.0, 120.0])
    ok = ok + probar("cierre dia sin citas", calcular_cierre(dnis, tipos, edades, asistencias, 10), [0, 0, 0, 0.0, 0.0, 0.0])
    ok = ok + probar("cierre dia sin marcar", calcular_cierre(dnis, tipos, edades, asistencias, 3), [3, 0, 0, 0.0, 0.0, 0.0])
    ok = ok + probar("resumen del mes", resumen_mes(dnis, tipos, edades, asistencias), [3, 13, 7, 3, 308.0, 180.0, 200.0])
    ok = ok + probar("deuda de la aseguradora", total_seguros(tipos, asistencias), 180.0)

    # reservar, mover y cancelar
    guardar_cita(dnis, nombres, celulares, tipos, edades, asistencias, posicion(5, 2), "12345678", "Sara Lopez", "911222333", "P", 40, "-")
    ok = ok + probar("cita guardada", nombres[posicion(5, 2)], "Sara Lopez")
    ok = ok + probar("libres despues de reservar", contar_libres(dnis, 5), 15)
    borrar_cita(dnis, nombres, celulares, tipos, edades, asistencias, posicion(5, 2))
    ok = ok + probar("turno libre despues de cancelar", dnis[posicion(5, 2)], "")
    ok = ok + probar("libres despues de cancelar", contar_libres(dnis, 5), 16)

    print("Pruebas correctas:", ok, "de 44")


def principal():
    total = DIAS_DEL_MES * TURNOS_DEL_DIA
    dnis = [""] * total
    nombres = [""] * total
    celulares = [""] * total
    tipos = [""] * total
    edades = [0] * total
    asistencias = [""] * total
    hoy = date.today().day
    cargar_ejemplo(dnis, nombres, celulares, tipos, edades, asistencias, hoy)
    print("Hoy es", nombre_del_dia(hoy))
    if not es_dia_laborable(hoy):
        print("Hoy el consultorio esta cerrado")
    estado_reporte = "sin enviar"
    opcion = ""
    while opcion != "7":
        print()
        mostrar_dia(dnis, nombres, asistencias, hoy)
        print("1 Reservar  2 Llego un paciente  3 Reprogramar o cancelar")
        print("4 Cierre de caja  5 Indicadores  6 Reporte de seguros  7 Salir  8 Pruebas")
        opcion = input("Opcion: ")
        if opcion == "1":
            reservar(dnis, nombres, celulares, tipos, edades, asistencias, hoy)
        elif opcion == "2":
            atender(dnis, nombres, tipos, edades, asistencias, hoy)
        elif opcion == "3":
            reprogramar(dnis, nombres, celulares, tipos, edades, asistencias, hoy)
        elif opcion == "4":
            cerrar_caja(dnis, nombres, tipos, edades, asistencias, hoy)
        elif opcion == "5":
            indicadores(dnis, tipos, edades, asistencias, hoy)
        elif opcion == "6":
            estado_reporte = reporte_aseguradora(dnis, nombres, tipos, asistencias, estado_reporte)
        elif opcion == "8":
            pruebas()
        elif opcion != "7":
            print("  Elija una opcion del 1 al 8")


principal()
