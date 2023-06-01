import sys
import time

from pulp import *

# Variables para almacenar los datos de entrada de los pedidos
reserva_estacionInicial = []
reserva_estacionFinal = []
reserva_nTickets = []

def nPedidos():
    return len(reserva_nTickets)

# Variables para almacenar los datos resultado que se mostrarán
mayor_beneficio_encontrado = 0
estado_mejor = []



def leer_datos(fichero):
    
    # Creamos todas las variables necesarias para leer datos y resolver bloques
    global nEstaciones
    global tren_capacidad_maxima

    global reserva_estacionInicial
    global reserva_estacionFinal
    global reserva_nTickets

    global nTickets_totales
    global mayor_beneficio_encontrado
    global estado_mejor

    mayor_beneficio_encontrado = 0
    estado_mejor = []

    nEstaciones = 0
    reserva_estacionInicial = []
    reserva_estacionFinal = []
    reserva_nTickets = []

    # Lee los datos de un fichero con sintaxis: 
    # capacidad estacion_final nPedidos
    # estacion_inicial estacion_final nTickets\n

    lineaInicial = fichero.readline()
    split_linea = lineaInicial.split(" ")

    tren_capacidad_maxima = int(split_linea[0])
    nEstaciones = int(split_linea[1])
    nPedidos = int(split_linea[2])

    # Mostramos error en el bloque si incumple la limitación de 1000 tickets 
    # maximo. Y analizamos el resto de bloques para generar los distintos 
    # poblemas que se van a resolver
    for i in range(nPedidos):
        linea = fichero.readline()

        if linea == "" or linea == "0 0 0":
            print("Error en el fichero de entrada: se esperaban", nPedidos, "pedidos y se han leido", i)
            exit(1)

        split_linea = linea.split(" ")

        estacion_inicial = int(split_linea[0])
        estacion_final = int(split_linea[1])
        nTickets = int(split_linea[2])

        reserva_estacionInicial.append(estacion_inicial)
        reserva_estacionFinal.append(estacion_final)
        reserva_nTickets.append(nTickets)

    nTickets_totales = 0

    # Calculamos el número de tickets totales que se pueden vender
    for i in range(nPedidos):
        nTickets_totales += reserva_nTickets[i]*(reserva_estacionFinal[i]-reserva_estacionInicial[i])

    # Mostramos error en el bloque si incumple la limitación de 7 estaciones maximo
    if nEstaciones > 7:
        print("El número de estaciones debe ser menor o igual que 7, es", nEstaciones)
        print("---------------------------------")
        return False

    # Mostramos error en el bloque si incumple la limitación de 22 pedidos maximo
    if nPedidos > 22:
        print("El número de pedidos debe ser menor o igual que 22, es ", nPedidos)
        print("---------------------------------")
        return False
        
    return True

# Función para calcular el coste de un pedido
def coste_reserva(i):
    return reserva_nTickets[i]*(reserva_estacionFinal[i]-reserva_estacionInicial[i])

def debugging(val):
    print("value:", val)
    return val

# Función que resuelve el problema de PL con los datos obtenidos
def resolver_problema():

    global mayor_beneficio_encontrado
    global estado_mejor

    # Definimos cual es el problema de PL que queremos resolver
    prob = LpProblem("Maximización_de_beneficios_de_venta_de_billetes_de_tren", LpMaximize)

    # Creamos las variables necesarias para tomar las decisiones a la hora de
    # movernos entre los nodos solución
    x = [LpVariable(f"x{i}", cat='Binary') for i in range(nPedidos())]


    # Creamos la función objetivo
    prob += lpSum(x[i] * coste_reserva(i) for i in range(nPedidos()))


    # Definimos las distintas restricciones del problema para eliminar nodos 
    # solución que no sean factibles
    for estacion in range(nEstaciones):
        volumen = lpSum(x[i] * reserva_nTickets[i] for i in range(nPedidos()) if estacion >= reserva_estacionInicial[i] and estacion < reserva_estacionFinal[i])
        prob += volumen <= tren_capacidad_maxima


    # Resolvemos el problema con todo lo anterior ya definido correctamente
    prob.solve()

    # Obtenemos el resultado que hemos conseguido
    mayor_beneficio_encontrado = value(prob.objective)
    estado_mejor = [x[i].value() for i in range(nPedidos())]


def peek_line(f):
    pos = f.tell()
    line = f.readline()
    f.seek(pos)
    return line


# Main del programa que crea el mapa de estados posibles y lo va explorando
# para conseguir el estado solución que maximice los beneficios de la venta
def main():
    
    global mayor_beneficio_encontrado

    if len(sys.argv) < 2:
        print("Llamar como python3 transporte.py <fichero_pruebas>")
        exit(1)

    fichero = open(sys.argv[1], "r")
    #fichero = open("p4/pruebas.txt", "r")

    output = open("resultados_pl.txt", "w")  

    while peek_line(fichero) != "0 0 0" and peek_line(fichero) != "":    
        
        if leer_datos(fichero):
            
            tiempo_init = time()

            resolver_problema()

            print("El estado con mayor beneficio es el", estado_mejor, "con un coste de", mayor_beneficio_encontrado)
            print("---------------------------------")

            tiempo_end = time()
            tiempo_total = (tiempo_end-tiempo_init)*1000

            output.write(str(float(mayor_beneficio_encontrado))+" "+str(tiempo_total)+"\n") 

    if peek_line(fichero) == "":
        print("Falta 0 0 0 para finalizar correctamente la lectura del fichero pruebas.txt, el resultado puede ser no válido")
        
        
    fichero.close()

main()