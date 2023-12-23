# -*- coding: utf-8 -*-
import random
import time

class Empleado:
    def __init__(self, tipo):
        self.tipo = tipo #Tipo de empleado (full-time o part-time)
        self.horario = [] #Horario del empleado vacío
        self.horarioMinutos = [] #Horario del empleado en minutos en variables enteras vacío
        self.minutosTotalesTrabajados = 0 #Minutos totales trabajados por el empleado
        self.actividades = [] #Lista de actividades del empleado donde "0" es que es un break

    def insertarSlot(self, slot):
        self.horario.append(slot) #Insertar como string un slot con una actividad, break o almuerzo al horario del empleado

    def insertarSlotInt(self, slot):
        self.horarioMinutos.append(slot) #Insertar como entero un slot con una actividad, sin contar breaks o almuerzos

    def asignarMinutosTotales(self, minutos):
        self.minutosTotalesTrabajados = minutos #Asignar los minutos totales trabajados por el empleado

    def getMinutos(self):
        return self.minutosTotalesTrabajados #Devolver los minutos totales trabajados por el empleado

    def getHorario(self):
        return self.horario #Devolver el horario del empleado en forma de strings
    
    def getHorarioMinutos(self):
        return self.horarioMinutos #Devolver el horario del empleado en forma de enteros

    def getActividades(self):
        return self.actividades

    def crearListaActividades(self): # Se crea una lista de actividades del empleado, donde "0" es que es un break
        for i in range(len(self.horarioMinutos)):
            aux = self.horarioMinutos[i] // 15

            if self.tipo == "full-time" and i == 0:
                for j in range(aux):
                    self.actividades.append("A1")
                continue

            elif self.tipo == "full-time" and i == 1:
                self.actividades.append("0")
                for j in range(aux):
                    self.actividades.append("A2")

            elif self.tipo == "full-time" and i == 2:
                for a in range(4):
                    self.actividades.append("1")
                for j in range(aux):
                    self.actividades.append("A3")

            elif self.tipo == "full-time" and i == 3:
                self.actividades.append("0")
                for j in range(aux):
                    self.actividades.append("A4")

            else:
                for j in range(aux):
                    self.actividades.append("A" + str(i + 1))

    def cambiarActividad(self, actividad, slot):
        self.actividades[slot] = actividad

# Función para intercambiar actividades entre dos empleados
def swap(slots, empleadoUno, empleadoDos):
    if slots >= len(empleadoUno.getActividades()):
        slots = len(empleadoUno.getActividades()) - 1

    elif slots >= len(empleadoDos.getActividades()):
        slots = len(empleadoDos.getActividades()) - 1

    for i in range(slots):
        actividadAux1 = empleadoUno.getActividades()[i]
        actividadAux2 = empleadoDos.getActividades()[i]

        empleadoUno.cambiarActividad(actividadAux2, i)
        empleadoDos.cambiarActividad(actividadAux1, i)        

def generarSchedule(empleado):
    horaInicio = random.randint(8, 9)

    #La hora de inicio es entre las 8 y las 9
    if horaInicio == 8:
        minutosInicio = random.randint(0, 3) * 15
    else:
        minutosInicio = 0

    #Se establece el mínimo y máximo de horas en minutos a trabajar para trabajadores full-time y part-time
    if empleado.tipo == "full-time":
        minimo = 360 #6 horas
        # maximo = 480 #8 horas

    elif empleado.tipo == "part-time":
        minimo = 180 #3 horas
        # maximo = 360 #6 horas

    horaActual = horaInicio
    minutosActual = minutosInicio

    #Contador para controlar las horas trabajadas en minutos
    minutosTrabajados = 0

    x = 1 #Inicializar el contador de actividad

    # Ciclo para generar el horario
    while minutosTrabajados < minimo:
        # Trabajar en una actividad al menos una hora
        actividad = "Actividad {}".format(x)
        duracionActividad = random.randint(4, 10) * 15  # Duración entre 1 y 2.5 horas por slots de 15 minutos

        #Si el empleado es full-time y ya ha trabajado 5 horas y 45 minutos, se hace el cambio para evitar la posibilidad de que sobrepase las 8 horas
        if minutosTrabajados == 345:
            duracionActividad = random.randint(4, 9) * 15

        #Ya que la duración mínima de una actividad es de 1 hora, se debe verificar que la hora siguiente sea la correcta
        horaSiguiente = horaActual + 1
        minutosSiguiente = 0

        #En el caso de que el contador de minutos actual más la duración de la actividad sea mayor o igual a 180 minutos (3 horas), se debe aumentar la hora siguiente en 3
        if (minutosActual + duracionActividad) >= 180:
            horaSiguiente = horaActual + 3

        #En el caso de que el contador de minutos actual más la duración de la actividad sea mayor o igual a 120 minutos (2 horas) y menor a 180 minutos (3 horas), se debe aumentar la hora siguiente en 2
        elif (minutosActual + duracionActividad) < 180 and (minutosActual + duracionActividad) >= 120:
            horaSiguiente = horaActual + 2
            # minutosSiguiente = (minutosActual + duracionActividad) % 60

        empleado.insertarSlot("{:02}:{:02} - {:02}:{:02}: {}".format(
            horaActual, minutosActual,
            horaSiguiente, (minutosActual + duracionActividad % 60) % 60,
            actividad)
        )

        empleado.insertarSlotInt(duracionActividad)

        horaActual = horaSiguiente
        minutosActual = (minutosActual + duracionActividad % 60) % 60

        minutosTrabajados += duracionActividad

        #Si el empleado es part-time y ya se le ha asignado un break, no se le asigna otro ni almuerzo
        if (x > 1 and empleado.tipo == "part-time"):
            x += 1
            continue

        #Siendo que el empleado es full-time por pasar el if anterior, si está post cuarta actividad, no se le asigna otro break ni almuerzo
        if x > 3:
            x += 1
            continue

        #Siendo que el empleado es full-time por pasar el if anterior, si ya superó el horario mínimo, se evita darle un break innecesario
        if minutosTrabajados >= minimo:
            break

        #Si es que el empleado es full-time y está en la hora posterior a la segunda actividad, se le debe asignar un almuerzo de 1 hora
        if empleado.tipo == "full-time" and x == 2:
            horaSiguiente = horaActual + 1
            minutosSiguiente = minutosActual

            empleado.insertarSlot("{:02}:{:02} - {:02}:{:02}: {}".format(
                horaActual, minutosActual,
                horaSiguiente, minutosSiguiente,
                "Almuerzo")
            )

            horaActual = horaSiguiente
            minutosActual = minutosSiguiente

        #De otra forma, simplemente se agrega un break de 15 minutos
        else:
            nBreak = x
            horaSiguiente = horaActual
            minutosSiguiente = minutosActual + 15

            if minutosActual + 15 >= 60:
                horaSiguiente = horaActual + 1
                minutosSiguiente = (minutosActual + 15) % 60

            if x == 3:
                nBreak = 2

            breakAux = "Break {}".format(nBreak)

            empleado.insertarSlot("{:02}:{:02} - {:02}:{:02}: {}".format(
                horaActual, minutosActual,
                horaSiguiente, minutosSiguiente,
                breakAux)
            )

            horaActual = horaSiguiente
            minutosActual = minutosSiguiente

        x += 1

    empleado.asignarMinutosTotales(minutosTrabajados)
                                           
# Función para contar cuantas veces se repite un elemento en una lista
def contarElementos(lista, elemento):
    contador = 0
    for i in lista:
        if i == elemento:
            contador += 1
    
    return contador

def existeElemento(lista, elemento):
    for i in lista:
        if i == elemento:
            return True
    
    return False

def menorValor(lista):
    menor = lista[0]
    for i in lista:
        if i < menor:
            menor = i

    return menor

# Función objetivo para minimizar el total de incumplimientos de duración de las actividades
def FuncionObjetivo(listaEmpleados, horasMinimas, horasMaximas):
    slotsMinimos = (horasMinimas * 60) // 15
    slotsMaximos = (horasMaximas * 60) // 15
    sumaRestriccion = 0
    sumaTotal = 0

    #Se hace un ciclo para revisar lo que duró cada actividad del empleado, para revisar si trabajó menos o más de lo indicado
    for a in range(len(listaEmpleados)): # Se recorre la lista viendo cada empleado
        listaRestricciones = [] # Se crea una lista para guardar las restricciones de cada empleado
        listaRestricciones.append(contarElementos(listaEmpleados[a].getActividades(), 'A1'))
        listaRestricciones.append(contarElementos(listaEmpleados[a].getActividades(), 'A2'))
        listaRestricciones.append(contarElementos(listaEmpleados[a].getActividades(), 'A3'))

        if existeElemento(listaEmpleados[a].getActividades(), 'A4'):
            listaRestricciones.append(contarElementos(listaEmpleados[a].getActividades(), 'A4'))
            
        if existeElemento(listaEmpleados[a].getActividades(), 'A5'):
            listaRestricciones.append(contarElementos(listaEmpleados[a].getActividades(), 'A5'))

        for b in range(len(listaRestricciones)):
            if listaRestricciones[b] < slotsMinimos:
                sumaRestriccion = (slotsMinimos - listaRestricciones[b])
                # print("La suma de la restriccion en minimo es: " + str(sumaRestriccion))

            elif listaRestricciones[b] > slotsMaximos:
                sumaRestriccion = (listaRestricciones[b] - slotsMaximos)
                # print("La suma de la restriccion en maximo es: " + str(sumaRestriccion))

            else:
                sumaRestriccion = 0
                # print("La suma de la restriccion es: " + str(sumaRestriccion))

            sumaTotal += sumaRestriccion

    # print("La suma total de restricciones es: " + str(sumaTotal))
    return sumaTotal

tiempoInicial = time.time() #Tiempo inicial de ejecución

random.seed(1)

# Generar horarios para 50 empleados "full-time"
# Empleados = [Empleado("full-time") for i in range(50)]

# Generar horarios para 200 empleados full-time
# Empleados = [Empleado("full-time") for i in range(200)]

# Generar horarios para 500 empleados full-time
Empleados = [Empleado("full-time") for i in range(500)]

for i, empleado in enumerate(Empleados, 1):
    # print("Horario del Empleado {} ({})".format(i, empleado.tipo))
    # print("\n")
    generarSchedule(empleado)
    empleado.crearListaActividades()
    # print(empleado.getActividades())

    # Imprimir el horario en intervalos de 15 minutos (slots)
    # for j, actividad in enumerate(empleado.getHorario()):
    #     print("Slot {}: {}".format(j + 1, actividad))

    # print("Horas y minutos de trabajo (formato hh:mm): {:02}:{:02}".format(empleado.getMinutos() // 60, empleado.getMinutos() % 60))
    # print("\n")

def HillClimbing(Empleados, nVecinos):
    valorInicial = FuncionObjetivo(Empleados, 1.5, 2)
    valorMejor = valorInicial
    fin = True

    print("Valor inicial: " + str(valorInicial))

    while fin:
        soluciones = []
        for x in range(nVecinos):
            empleado1 = random.choice(Empleados)
            empleado2 = random.choice(Empleados)

            # Evitar que se seleccione el mismo empleado
            while empleado2 == empleado1:
                empleado2 = random.choice(Empleados)

            # Seleccionar una posición aleatoria
            slot = random.randint(0, min(len(empleado1.getActividades()), len(empleado2.getActividades())) - 1)

            # Intercambiar las actividades en la posición seleccionada
            actividad_aux1 = empleado1.getActividades()[slot]
            actividad_aux2 = empleado2.getActividades()[slot]

            empleado1.cambiarActividad(actividad_aux2, slot)
            empleado2.cambiarActividad(actividad_aux1, slot)

            valorActual = FuncionObjetivo(Empleados, 1.5, 2)
            soluciones.append(valorActual)

        valorActual = menorValor(soluciones)

        if valorActual < valorMejor:
            valorMejor = valorActual
            print("Valor actual: " + str(valorActual))
        else:
            fin = False

    print("La suma final de la función objetivo es: " + str(valorMejor))


HillClimbing(Empleados, 500)
tiempoFinal = time.time() #Tiempo final de ejecución

# for empleado in Empleados:
#     print(empleado.getActividades())

print("Tiempo de ejecucion: " + str(tiempoFinal - tiempoInicial)) #Tiempo de ejecución total

