# -*- coding: utf-8 -*-
class Empleado:
    def __init__(self, nombre, periodos):
        self.nombre = nombre
        self.actividades = ["vacio"] * periodos #Se inicializa la lista de actividades que se realizarán en cada periodo
        self.periodos = periodos
        self.disponibilidad = [0] * periodos #Se inicializan los periodos como desocupados

    def estaDisponible(self, periodo): #Define si el empleado está disponible en ese periodo
        if self.disponibilidad[periodo] == 0: #Si el periodo está desocupado
            return True
        
        elif self.disponibilidad[periodo] == 1: #Si el periodo está ocupado
            return False

    def setPeriodo(self, periodo): #Marca el periodo del empleado como ocupado
        self.disponibilidad[periodo] = 1

    def setActividad(self, nombreActividad, periodo):
        self.actividades[periodo] = nombreActividad
    
    def getDisponibilidad(self):
        return self.disponibilidad
    
    def getActividades(self):
        return self.actividades
    
    #Se implementa un método donde dos empleados intercambian sus actividades en cierto horizonte de periodos indicado. Además que se marca la dispoonibilidad correspondiente si es que cambian de actividad
    def swapActividades(self, otroEmpleado, periodoInicial, periodoFinal):
        #Debido a que puede especificarse solo un periodo, se hace la excepción
        if periodoInicial == periodoFinal:
            aux = self.actividades[periodoInicial]
            self.actividades[periodoInicial] = otroEmpleado.actividades[periodoInicial]
            otroEmpleado.actividades[periodoInicial] = aux

            aux2 = self.disponibilidad[periodoInicial]
            self.disponibilidad[periodoInicial] = otroEmpleado.disponibilidad[periodoInicial]
            otroEmpleado.disponibilidad[periodoInicial] = aux2

        else:
            for i in range(periodoInicial, periodoFinal):
                aux = self.actividades[i]
                self.actividades[i] = otroEmpleado.actividades[i]
                otroEmpleado.actividades[i] = aux

                aux2 = self.disponibilidad[i]
                self.disponibilidad[i] = otroEmpleado.disponibilidad[i]
                otroEmpleado.disponibilidad[i] = aux2

    def mostrarInfo(self):
        print("Empleado: " + self.nombre)
        print("Periodos asignados: ")
        for i in range(self.periodos):
            if self.disponibilidad[i] == 1:
                print("- Periodo " + str(i))

        print("Actividades asignadas: ")
        for actividad in self.actividades:
            print("- " + actividad)

class Actividad:
    def __init__(self, nombre, demanda):
        self.nombre = nombre
        self.demanda = demanda #Lista con demanda de empleados por periodo
        self.empleados = []

    def getDemanda(self): #Retorna la lista con demanda de empleados por periodo
        return self.demanda
    
    def getNombre(self):
        return self.nombre
    
    def asignarEmpleado(self, empleado): #Asigna empleado a la actividad en cierto periodo
        self.empleados.append(empleado) #Asigna empleado a la actividad

    def mostrarInfo(self):
        largo = len(self.demanda)
        print("Actividad: " + self.nombre)
        print("Periodos asignados: ")
        for i in range(largo):
            print("- Periodo " + str(i))
        if self.empleados:
            print("Empleados asignados: ")
            for empleado in self.empleados:
                print("- " + empleado.nombre)
        else:
            print("No se han asignado empleados a esta actividad")

Slots = 10

#Se setean los empleados con sus nombres y con 10 periodos de disponibilidad cada uno
Empleado1 = Empleado("Empleado1", Slots)
Empleado2 = Empleado("Empleado2", Slots)
Empleado3 = Empleado("Empleado3", Slots)
Empleado4 = Empleado("Empleado4", Slots)
Empleado5 = Empleado("Empleado5", Slots)
Empleado6 = Empleado("Empleado6", Slots)
Empleado7 = Empleado("Empleado7", Slots)
Empleado8 = Empleado("Empleado8", Slots)
Empleado9 = Empleado("Empleado9", Slots)
Empleado10 = Empleado("Empleado10", Slots)

#Se setean las actividades con sus nombres y con la demanda de empleados por periodo
# Reunion = Actividad("Reunion", [3])
Diseno = Actividad("Diseno", [2, 3, 5, 6])
Tareas = Actividad("Tareas", [1, 2, 4, 6, 7, 3, 5])

Empleados = [Empleado1, Empleado2, Empleado3, Empleado4, Empleado5, Empleado6, Empleado7, Empleado8, Empleado9, Empleado10]
Actividades = [Diseno, Tareas]

def Greedy(Empleados, Actividades):
    for k in Actividades:
        periodos = len(k.getDemanda())

        for i in Empleados:
            for j in range(periodos):
                if k.getDemanda()[j] > 0 and i.estaDisponible(j):
                    i.setPeriodo(j)
                    i.setActividad(k.getNombre(), j)
                    k.asignarEmpleado(i)
                    k.getDemanda()[j] -= 1                                                    

#Función objetivo para minimizar el total de incumplimientos de duración de las actividades
def FuncionObjetivo(Empleados, Actividades):
    restriccion = 0
    minimo = 4 #Para el caso donde la duración mínima son 4 periodos seguidos y la máxima 12
    maximo = 12
    suma = 0 #Suma que retornará la función objetivo

    #Se recorren las actividades y se calcula la restricción para cada una
    for actividad in Actividades:
        #Se recorren los periodos de los empleados, para calcular los periodos consecutivos que trabaja cada uno
        for empleado in Empleados:
            mayor = 0
            consecutivos = 0
            #Se recorren los periodos de disponibilidad del empleado
            # for i in range(len(empleado.getDisponibilidad())):
                #Se recorre la lista de actividades del empleado, buscando las actividades consecutivas que coincidan con la actividad actual, para sacar el mayor número de periodos consecutivos que trabaja en la actividad
            for j in range(len(empleado.getActividades())):
                if empleado.getActividades()[j] == actividad.getNombre():
                    consecutivos += 1
                    if consecutivos > mayor:
                        mayor = consecutivos
                else:
                    consecutivos = 0

            #Se crea la variable "t" para controlar cuando parte la actividad
            t = 0
            #Se recorren los periodos de disponibilidad del empleado, donde t = 1 significa que es el periodo donde el empleado parte trabajando en la actividad, de otra forma, t = 0
            for i in range(len(empleado.getDisponibilidad())):
                if empleado.getActividades()[i] == actividad.getNombre() and t == 0:
                    t = 1

            if mayor < minimo:
                restriccion = minimo - mayor

            elif mayor > maximo:
                restriccion = mayor + t - maximo - 1 

            else:
                restriccion = 0

            suma += restriccion
        
    return suma

def HillClimbingMejorMejora(Empleados, Actividades):
    EmpleadosAux = Empleados
    ActividadesAux = Actividades

    sumaInicial = FuncionObjetivo(Empleados, Actividades)

    print("Suma inicial: " + str(sumaInicial))

    #Se calcula la función objetivo inicial
    funcionObjetivoInicial = FuncionObjetivo(Empleados, Actividades)

    for i in Empleados:
        for j in Empleados:
            for k in range(len(i.getDisponibilidad())):
                for l in range(len(j.getDisponibilidad())):
                    i.swapActividades(j, k, l)
                    funcionObjetivoActual = FuncionObjetivo(Empleados, Actividades)

                    if funcionObjetivoActual < funcionObjetivoInicial:
                        funcionObjetivoInicial = funcionObjetivoActual
                        EmpleadosAux = Empleados
                        ActividadesAux = Actividades

                    else:
                        i.swapActividades(j, k, l)

    sumaFinal = FuncionObjetivo(EmpleadosAux, ActividadesAux)

    if  sumaFinal < sumaInicial:
        print("Ejecutando Hill Climbing denuevo")
        HillClimbingMejorMejora(EmpleadosAux, ActividadesAux)

    else:
        print("La suma final de la funcion objetivo es: " + str(sumaFinal))

Greedy(Empleados, Actividades)
# print(FuncionObjetivo(Empleados, Actividades))

HillClimbingMejorMejora(Empleados, Actividades)
# Para imprimir el estado de los empleados y de las actividades
# for i in Empleados:
#     i.mostrarInfo()

# for i in Actividades:
#     i.mostrarInfo()
    
