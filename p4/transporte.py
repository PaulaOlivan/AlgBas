import sys
import time
import queue

class PrioritizedItem:
    def __init__(self, priority, k, estado):
        self.priority = priority
        self.k = k
        self.estado = estado

    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.priority == other.priority


cola_nodos = queue.PriorityQueue()

nEstaciones = 4
tren_capacidad_maxima = 10

reserva_estacionInicial = []
reserva_estacionFinal = []
reserva_nTickets = []

def nPedidos():
    return len(reserva_nTickets)


coste_minimo_encontrado = 1 << 31
estado_minimo = []


def leer_datos(fichero):
    
    global nEstaciones
    global tren_capacidad_maxima

    global reserva_estacionInicial
    global reserva_estacionFinal
    global reserva_nTickets

    global nTickets_totales
    global coste_minimo_encontrado
    global estado_minimo

    coste_minimo_encontrado = 1 << 31
    estado_minimo = []

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

    for i in range(nPedidos):
        nTickets_totales += reserva_nTickets[i]*(reserva_estacionFinal[i]-reserva_estacionInicial[i])

    if nEstaciones > 7:
        print("El número de estaciones debe ser menor o igual que 7")
        print("---------------------------------")
        return False

    if nPedidos > 22:
        print("El número de pedidos debe ser menor o igual que 22")
        print("---------------------------------")
        return False
        
    return True

    


# Función asociada a ĉ para eliminar ramas del mapa de estados que no sean
# posibles soluciones mejores a la rama actual
def poda ():
    return coste_minimo_encontrado


# Función asociada a ĉ para elegir cual de las ramas a explorar nos va a llevar
# a mejores resultados en un momento de elección más próximo
def heuristica (k, estado):
    valor = 0

    for i in range(k+1):
        if estado[i] == 0:
            valor += reserva_nTickets[i]*(reserva_estacionFinal[i]-reserva_estacionInicial[i])

    return valor


def coste (estado):

    valor = nTickets_totales
    for i in range(nPedidos()):
        if estado[i] == 1:
            valor -= reserva_nTickets[i]*(reserva_estacionFinal[i]-reserva_estacionInicial[i])

    return valor # Tickets que nos hemos dejado por coger



# Devuelve true si el estado es solución, elimina nodos repetidos
def acotador_1(indice_nuevo, indice_anterior):
    return indice_nuevo > indice_anterior


# Devuelve true si el estado es solucion, limita la capacidad del tren
def acotador_2(estado_nuevo):

    for estacion in range(nEstaciones):
        
        volumen = 0
        
        # Suma los pedidos que pasen por esa estacion
        for i in range(nPedidos()):
            if estado_nuevo[i] == 1 and estacion >= reserva_estacionInicial[i] and estacion < reserva_estacionFinal[i]:
                volumen += reserva_nTickets[i]

        if volumen > tren_capacidad_maxima:
            return False

    return True



def generar_hijos(k_anterior, estado_inicial):

    global coste_minimo_encontrado
    global estado_minimo
    global cola_nodos

    terminar = False

    while not terminar:
        # Expande el nodo
        for k in range(nPedidos()):
            estado = estado_inicial.copy()
            estado[k] = 1       # Añadimos el pedido k

            if acotador_1(k, k_anterior) and acotador_2(estado): # Si se cumplen las restricciones
                
                coste_nodo = coste(estado)
                
                if coste_nodo < coste_minimo_encontrado:
                    coste_minimo_encontrado = coste_nodo
                    estado_minimo = estado

                heuristica_nodo = heuristica(k, estado)
                poda_nodo = poda()

                if heuristica_nodo < poda_nodo:              # Si la heurística es prometedora
                    cola_nodos.put(PrioritizedItem(heuristica_nodo, k, estado))

        if cola_nodos.empty():
            terminar = True
        else:
            # Pasa al siguiente nodo a generar
            nodo_nuevo = cola_nodos.get() # Elimina el nodo actual de la cola
            k_anterior = nodo_nuevo.k
            estado_inicial = nodo_nuevo.estado
            

def peek_line(f):
    pos = f.tell()
    line = f.readline()
    f.seek(pos)
    return line


# Main del programa que crea el mapa de estados posibles y lo va explorando
# para conseguir el estado solución que maximice los beneficios de la venta
def main():
    
    if len(sys.argv) < 2:
        print("Llamar como python3 transporte.py <fichero_pruebas>")
        exit(1)

    fichero = open(sys.argv[1], "r")
    #fichero = open("p4/pruebas.txt", "r")

    output = open("resultados.txt", "w")  

    while peek_line(fichero) != "0 0 0" and peek_line(fichero) != "":    
        
        if leer_datos(fichero):
            
            tiempo_init = time.time()

            estado_inicial = [0] * nPedidos()
            generar_hijos(-1, estado_inicial)

            beneficio = nTickets_totales - coste_minimo_encontrado

            print("El estado con mayor beneficio es el", estado_minimo, "con un coste de", beneficio)
            print("---------------------------------")

            tiempo_end = time.time()
            tiempo_total = (tiempo_end-tiempo_init)*1000

            output.write(str(float(beneficio))+" "+str(tiempo_total)+"\n") 

    if peek_line(fichero) == "":
        print("Falta 0 0 0 para finalizar correctamente la lectura del fichero pruebas.txt, el resultado puede ser no válido")
        
        
    fichero.close()

main()