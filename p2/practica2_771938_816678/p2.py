import time
#import p2_gpu
#import numba
#import numpy as np
import sys

# Argumentos: p2.py profundidad(int) i_bola(int) usar_fuerza_bruta(0/1)
#@numba.jit(nopython=False, cache=True)

# Función que calcula el camino que debe seguir la bola i_bola para llegar 
# a la hoja que le corresponda en la profundidad p utilizando Divide y Venceras
def dondeEstaLaBolita (profundidad, i_bolita):
    
    camino = [0]*(profundidad - 1)
    #camino = np.empty(profundidad-1, numba.uint8)
    
    for p in range(1, profundidad):
        indice_en_profundidad = (i_bolita-1) % (1 << p)
        
        if indice_en_profundidad < (1 << (p-1)):
            camino[p-1] = 0
        else: 
            camino[p-1] = 1

    return camino

# Clase que representa un nodo del árbol binario
class Nodo:
    def __init__(self, posicion = 1, direccion = 0):
        self.direccion = direccion
        self.posicion = posicion
        self.left = None
        self.right = None

# Función que crea un árbol binario completo de profundidad p
def create_complete_tree(p, initDir=0, posicion=1):
    if p == 0:
        return None
    root = Nodo(posicion)
    root.left = create_complete_tree(p-1, initDir, posicion*2)
    root.right = create_complete_tree(p-1, initDir, (posicion*2)+1)
    return root

# Función que calcula el camino que debe seguir la bola i_bola para llegar
# a la hoja que le corresponda en la profundidad p utilizando Fuerza Bruta
def colocarBolas (nBolas, nodo, n_bola):
    for i in range(1, nBolas+1):
        camino = bolasFB (i, nodo)

        if i == n_bola:
            return camino

# Función que devuelve el camino que debe seguir la bola i para llegar
def bolasFB (i, nodo):
    if nodo.left == None: # Estoy en el caso base, he llegado a la hoja
        return []
        #print ("La bola", i, "esta en el nodo del arbol", nodo.posicion) 
    elif nodo.direccion == 0:
        nodo.direccion = 1
        camino = [0]
        camino.extend(bolasFB(i, nodo.left))
        return camino
    else:
        nodo.direccion = 0
        camino = [1]
        camino.extend(bolasFB(i, nodo.right))
        return camino

if len(sys.argv) != 3:
    print("Invocar como: p2.py pruebas.txt resultados.txt")
    exit(1)

# Leemos linea a linea el archivo de entrada que contiene la profundidad y las bolas a colocar
with open('pruebas.txt', 'r') as file_in:
    with open('resultados.txt', 'w') as file_out:
         # Leer todas las líneas del archivo de entrada
        lines = file_in.readlines()
        # Eliminar las dos primeras líneas de la lista
        lines = lines[2:]

        # Ecribimos la linea de cabecera
        file_out.write("PosicionBolasLanzadas\tFuerzaBruta\tDivideYVenceras\tGPU")

        for line in lines:
            prof, bol, *resto = line.split() # separar la línea en palabras
            profundidad = int(prof) # convertir el primer número en entero
            bolas = int(bol) # convertir el segundo número en entero


            nBolas = (1 << profundidad-1) # El numero total de bolas es el numero de nodos en la capa de las hojas

            # Ejecutamos el algoritmo de divide y venceras
            init = time.time()
            camino_cpu = dondeEstaLaBolita(profundidad, bolas)
            finAlgoritmo = time.time()
            
            # Mostramos tiempo por pantalla
            print ("Tiempo de ejecucion del algoritmo en CPU:", (finAlgoritmo-init))


            # Ejecutamos el algoritmo de fuerza bruta
            init = time.time()
            raiz = create_complete_tree(profundidad, 0, 1)
            camino_fb = colocarBolas(nBolas, raiz, bolas)
            finFB = time.time()
            print ("Tiempo de ejecucion del metodo de fuerza bruta:", (finFB-init))
            
            # Comprobamos si el resultado es correcto
            if camino_cpu == camino_fb:
                print("Los caminos son iguales")
                print ("Camino:", camino_cpu)
            else:
                print("Los caminos son diferentes")
                print("Camino CPU:", camino_cpu)
                print("Camino FB:", camino_fb)
            
            # Escribimos el resultado en el archivo de salida
            file_out.write(str(bolas) + "\t" + str(finFB-init) + "\t" + str(finAlgoritmo-init) + "\n")


            #init = time.time()
            #camino = p2_gpu.donde_esta_la_bolita_gpu(profundidad, i_bola)
            #finAlgoritmo = time.time()

            #print ("Tiempo de ejecucion del algoritmo en GPU:", (finAlgoritmo-init))


