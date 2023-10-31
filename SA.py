# -*- coding: utf-8 -*-
import math
import random
import copy

class Empleado:
    def __init__(self, tipo):
        self.tipo = tipo #Tipo de empleado (full-time o part-time)
        self.horario = [] #Horario del empleado vacío
        self.horarioMinutos = [] #Horario del empleado en minutos en variables enteras vacío
        self.minutosTotalesTrabajados = 0 #Minutos totales trabajados por el empleado

    def insertarSlot(self, slot):
        self.horario.append(slot) #Insertar como string un slot con una actividad, break o almuerzo al horario del empleado

    def insertarSlotInt(self, slot):
        self.horarioMinutos.append(slot) #Insertar como entero un slot con una actividad, sin contar breaks o almuerzos

    def asignarMinutosTotales(self, minutos):
        self.minutosTotalesTrabajados = minutos #Asignar los minutos totales trabajados por el empleado

    #Método para reiniciar el horario del empleado en Simulated Annealing
    def reiniciarHorario(self):
        self.horario = []
        self.horarioMinutos = []
        self.minutosTotalesTrabajados = 0

    def sumar15Minutos(self, nSlot):
        self.horarioMinutos[nSlot] += 15 #Sumar 15 minutos a un slot específico del horario del empleado

    def restar15Minutos(self, nSlot):
        self.horarioMinutos[nSlot] -= 15 #Restar 15 minutos a un slot específico del horario del empleado

    def getMinutos(self):
        return self.minutosTotalesTrabajados #Devolver los minutos totales trabajados por el empleado

    def getHorario(self):
        return self.horario #Devolver el horario del empleado en forma de string
    
    def getHorarioMinutos(self):
        return self.horarioMinutos #Devolver el horario del empleado en forma de enteros

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
        maximo = 480 #8 horas

    elif empleado.tipo == "part-time":
        minimo = 180 #3 horas
        maximo = 360 #6 horas

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

def FuncionObjetivo(listaEmpleados, horasMinimas, horasMaximas):
    Minimo = horasMinimas * 60
    Maximo = horasMaximas * 60
    sumaRestriccion = 0
    sumaTotal = 0

    #Se hace un ciclo para revisar lo que duró cada actividad del empleado, para revisar si trabajó menos o más de lo indicado
    for a in range(len(listaEmpleados)):
        for b in range(len(listaEmpleados[a].getHorarioMinutos())):
            if listaEmpleados[a].getHorarioMinutos()[b] < Minimo:
                sumaRestriccion = (Minimo - listaEmpleados[a].getHorarioMinutos()[b]) / 15
                # print("La suma de la restriccion en minimo es: " + str(sumaRestriccion))

            elif listaEmpleados[a].getHorarioMinutos()[b] > Maximo:
                sumaRestriccion = (listaEmpleados[a].getHorarioMinutos()[b] - Maximo) / 15
                # print("La suma de la restriccion en maximo es: " + str(sumaRestriccion))

            else:
                sumaRestriccion = 0
                # print("La suma de la restriccion es: " + str(sumaRestriccion))

            sumaTotal += sumaRestriccion

    return sumaTotal

random.seed(2) #Controlar aleatoriedad

# Generar horarios para 50 empleados full-time
Empleados = [Empleado("full-time") for i in range(50)]

for i, empleado in enumerate(Empleados, 1):
    # print("Horario del Empleado {} ({})".format(i, empleado.tipo))
    # print("\n")
    generarSchedule(empleado)

    # Imprimir el horario en intervalos de 15 minutos (slots)
    # for j, actividad in enumerate(empleado.getHorario()):
    #     print("Slot {}: {}".format(j + 1, actividad))

    # print("Horas y minutos de trabajo (formato hh:mm): {:02}:{:02}".format(empleado.getMinutos() // 60, empleado.getMinutos() % 60))
    # print("\n")

print("Solucion inicial: " + str(FuncionObjetivo(Empleados, 1.5, 2)))

def SimulatedAnnealing():
    empleadosAux = copy.deepcopy(Empleados)
    solucionActual = FuncionObjetivo(empleadosAux, 1.5, 2) #Solucion inicial
    # mejorSolucion = solucionActual #Mejor solución
    temperatura = 500.0 #Temperatura inicial
    tasaEnfriamiento = 3.0 #Tasa de enfriamiento
    nSolucion = 0 #Variable para contar en qué solución del algoritmo va

    print("Temperatura inicial: " + str(temperatura))

    while temperatura > 0.1:
        # empleadosAux = copy.deepcopy(Empleados) #Crea una copia de la lista de empleados
        # for empleado in empleadosAux:
        #     empleado.reiniciarHorario() #Reinicia el horario de cada empleado a 0

        empleadosSeleccionados = random.sample(empleadosAux, 2) #Selecciona 2 empleados aleatorios
        empleado1 = empleadosSeleccionados[0]
        empleado2 = empleadosSeleccionados[1]
        actividadModificar = random.randint(0, len(empleado1.getHorarioMinutos()) - 1) #Selecciona un slot aleatorio del horario del empleado 1

        if actividadModificar >= len(empleado2.getHorarioMinutos()):
            actividadModificar = len(empleado2.getHorarioMinutos()) - 1

        # print("Empleados seleccionados: " + str(empleado1) + " y " + str(empleado2))
        # print("Slot seleccionado: " + str(actividadModificar))

        if random.random() < 0.5:
            empleado1.restar15Minutos(actividadModificar)
            empleado2.sumar15Minutos(actividadModificar)

        else:
            empleado1.sumar15Minutos(actividadModificar)
            empleado2.restar15Minutos(actividadModificar)

        # for empleado in empleadosAux:
        #     generarSchedule(empleado) #Se vuelve a generar un nuevo horario para cada empleado

        solucionNueva = FuncionObjetivo(empleadosAux, 1.5, 2)

        evaluacion = solucionNueva - solucionActual #Diferencia entre el costo de la solucion nueva y la actual
        # print("Solucion nueva: " + str(solucionNueva))
        # print("Evaluacion: " + str(evaluacion))
        # print("Valor formula: " + str(math.exp(-evaluacion / temperatura)))
        if evaluacion <= 0:
            print("Acepta inmediatamente solucion")
            solucionActual = solucionNueva

        elif random.random() < math.exp(-evaluacion / temperatura):
            print("Acepta con cierta probabilidad")
            # print("Valor de exponencial: " + str(math.exp(-evaluacion / temperatura)))
            # print("Temperatura: " + str(temperatura))
            solucionActual = solucionNueva

        temperatura -= tasaEnfriamiento
        nSolucion += 1

        #Imprime cada 100 soluciones la solución actual
        if (nSolucion % 100) == 0:
            print("Solucion numero " + str(nSolucion) + ": " + str(solucionActual))

    return solucionActual #Retornar mejor solución

print("Solucion final: " + str(SimulatedAnnealing()))

#Reglas a seguir:

#1. Un break tiene una duración de 15 minutos
#2. El almuerzo tiene una duración de 1 hora
#3. Un trabajador part-time puede tomar un break durante su turno
#4. Un trabajador full-time está sujeto a un break, un almuerzo y otro break en ese orden
#5. Cuando un empleado empieza a trabajar en una actividad, trabaja por al menos una hora en esa misma actividad
#6. Almuerzos y breaks están divididos entre dos periodos de trabajo
#7. Un empleado debe tener un break o un almuerzo antes de pasar a una actividad
#8. Los periodos de descanso deben ser organizados al principio o al final del dia
#9. Un empleado part-time debe trabajar un mínimo de 3 horas pero menos que 6 horas al día
#10. Un empleado full-time debe trabajar un mínimo de 6 horas pero máximo 8 horas al día
#11. A horas específicas del día, cuando el negocio está cerrado, cada empleado debe descansar, almorzar o estar en un break