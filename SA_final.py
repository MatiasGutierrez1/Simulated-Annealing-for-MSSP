# -*- coding: utf-8 -*-
import math
import random
import copy
import time
import matplotlib.pyplot as plt
import numpy as np

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

    #Se establece el mínimo de horas en minutos a trabajar para trabajadores full-time y part-time, el máximo se controla a lo largo de la función
    if empleado.tipo == "full-time":
        minimo = 360 #6 horas

    elif empleado.tipo == "part-time":
        minimo = 180 #3 horas

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

def buscarRestricciones(listaEmpleados, horasMinimas, horasMaximas):
    empleado = random.choice(listaEmpleados) # Se escoge un empleado aleatorio
    slotActividad = random.choice(range(len(empleado.getHorarioMinutos()))) # Se escoge una actividad aleatoria del empleado
    
    empleadoSiguiente = listaEmpleados[(listaEmpleados.index(empleado) + 1) % len(listaEmpleados)] # Se escoge el empleado siguiente al anterior
    slotActividad2 = random.choice(range(len(empleadoSiguiente.getHorarioMinutos()))) # Se escoge una actividad aleatoria del empleado siguiente
    
    minimo = horasMinimas * 60 # Se establece el mínimo de horas en minutos a trabajar para trabajadores full-time y part-time
    maximo = horasMaximas * 60 # Se establece el máximo de horas en minutos a trabajar para trabajadores full-time y part-time
    nAleatorio = random.random() # Se genera un número aleatorio entre 0 y 1 para decidir si se resta o suma 15 minutos a una actividad del empleado

    # Se recorre el horario de cada empleado
    if nAleatorio < 0.5: 
        if empleado.getMinutos() + 15 <= 480: # Si la diferencia no sobrepasa las 8 horas
            if empleadoSiguiente.getMinutos() - 15 >= 360: # Si la diferencia del siguiente no es menor a 6 horas
                if empleadoSiguiente.getHorarioMinutos()[slotActividad2] > minimo: # Si la actividad seleccionada del empleado siguiente es mayor al mínimo
                    empleado.sumar15Minutos(slotActividad)
                    empleadoSiguiente.restar15Minutos(slotActividad2)
                    # print("Se cambia el horario del empleado " + str(listaEmpleados.index(empleado)) + " en el slot " + str(a) + " con el empleado " + str(listaEmpleados.index(empleadoSiguiente)) + " en el slot " + str(b))

    elif nAleatorio >= 0.5:
        if empleado.getMinutos() - 15 >= 360: # Si la diferencia no es menor a las 6 horas
            if empleadoSiguiente.getMinutos() + 15 <= 480:
                if empleadoSiguiente.getHorarioMinutos()[slotActividad2] < maximo: # Si la actividad seleccionada del empleado siguiente es menor al máximo
                    empleado.restar15Minutos(slotActividad)
                    empleadoSiguiente.sumar15Minutos(slotActividad2)
                    # print("Se cambia el horario del empleado " + str(listaEmpleados.index(empleado)) + " en el slot " + str(a) + " con el empleado " + str(listaEmpleados.index(empleadoSiguiente)) + " en el slot " + str(b))  
    
tiempoInicial = time.time() #Tiempo inicial de ejecución

random.seed(1) #Controlar aleatoriedad

# Generar horarios para 50 empleados full-time
Empleados = [Empleado("full-time") for i in range(50)]

# Generar horarios para 200 empleados full-time
# Empleados = [Empleado("full-time") for i in range(200)]

# Generar horarios para 500 empleados full-time
# Empleados = [Empleado("full-time") for i in range(500)]

for i, empleado in enumerate(Empleados, 1):
    generarSchedule(empleado)

print("Solucion inicial: " + str(FuncionObjetivo(Empleados, 1.5, 2)))

def Grafica(lista):
    # Genera valores x
    # lista = lista[:3500]
    valores_x = np.arange(len(lista))

    # Valores de y con la lista de mejores soluciones que se han encontrado
    valores_y = lista

    # Grafica la función
    plt.plot(valores_x, valores_y, label='SA - Soluciones')
    plt.title('Gráfica mejoras en la función objetivo')
    plt.xlabel('Número de iteración')
    plt.ylabel('Mejor valor de la función objetivo')
    plt.legend()
    plt.grid(True)
    plt.show()

def SimulatedAnnealing():
    empleadosAux = copy.deepcopy(Empleados)
    solucionActual = FuncionObjetivo(empleadosAux, 1.5, 2) #Solucion inicial
    mejorSolucion = solucionActual #Mejor solución
    temperatura = 100 #Temperatura inicial
    tasaEnfriamiento = 0.01 #Tasa de enfriamiento
    nSolucion = 0 #Variable para contar en qué solución del algoritmo va
    listaSoluciones = [] #Lista para guardar las mejores soluciones encontradas y graficarlas

    while temperatura > 0.1:
        buscarRestricciones(empleadosAux, 1.5, 2)
        solucionNueva = FuncionObjetivo(empleadosAux, 1.5, 2)
        evaluacion = solucionNueva - solucionActual #Diferencia entre el costo de la solucion nueva y la actual

        if evaluacion < 0: #Si la solución nueva es mejor que la actual, se acepta inmediatamente
            # print("Acepta inmediatamente solucion: " + str(solucionNueva))
            solucionActual = solucionNueva

        elif random.random() < math.exp(-evaluacion / temperatura): #Si no, se acepta con cierta probabilidad
            solucionActual = solucionNueva

        if solucionActual < mejorSolucion: #Si la solución actual es mejor que la mejor solución, se actualiza
            mejorSolucion = solucionActual
            listaSoluciones.append(mejorSolucion)

        else:
            listaSoluciones.append(mejorSolucion)

        temperatura -= tasaEnfriamiento
        nSolucion += 1

        if (nSolucion % 100) == 0: #Imprime cada 100 soluciones la solución actual
            print("Solucion numero " + str(nSolucion) + ": " + str(solucionActual))

    Grafica(listaSoluciones) #Graficar las soluciones encontradas
    return mejorSolucion #Retornar mejor solucióna

print("Solucion final: " + str(SimulatedAnnealing()))
tiempoFinal = time.time() #Tiempo final de ejecución
print("Tiempo de ejecucion: " + str(tiempoFinal - tiempoInicial)) #Tiempo de ejecución total
