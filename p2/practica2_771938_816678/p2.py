import time
#import p2_gpu
#import numba
#import numpy as np
import sys

# Argumentos: p2.py profundidad(int) i_bola(int) usar_fuerza_bruta(0/1)
#@numba.jit(nopython=False, cache=True)
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


class Nodo:
    def __init__(self, posicion = 1, direccion = 0):
        self.direccion = direccion
        self.posicion = posicion
        self.left = None
        self.right = None

def create_complete_tree(p, initDir=0, posicion=1):
    if p == 0:
        return None
    root = Nodo(posicion)
    root.left = create_complete_tree(p-1, initDir, posicion*2)
    root.right = create_complete_tree(p-1, initDir, (posicion*2)+1)
    return root

def colocarBolas (nBolas, nodo, n_bola):
    for i in range(1, nBolas+1):
        camino = bolasFB (i, nodo)

        if i == n_bola:
            return camino

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

if len(sys.argv) != 4:
    print("Invocar como: p2.py profundidad i_bola usar_fuerza_bruta")
    exit(1)

profundidad = int(sys.argv[1])
i_bola = int(sys.argv[2])
usar_fuerza_bruta = bool(int(sys.argv[3]))


nBolas = (1 << profundidad-1) #El numero total de bolas es el numero de nodos en la capa de las hojas

init = time.time()
camino_cpu = dondeEstaLaBolita(profundidad, i_bola)
finAlgoritmo = time.time()

print ("Tiempo de ejecucion del algoritmo en CPU:", (finAlgoritmo-init))


if usar_fuerza_bruta:
    init = time.time()
    raiz = create_complete_tree(profundidad, 0, 1)
    camino_fb = colocarBolas(nBolas, raiz, i_bola)
    finFB = time.time()
    print ("Tiempo de ejecucion del metodo de fuerza bruta:", (finFB-init))
    
    if camino_cpu == camino_fb:
        print("Los caminos son iguales")
    else:
        print("Los caminos son diferentes")
        print("Camino CPU:", camino_cpu)
        print("Camino FB:", camino_fb)


init = time.time()
#camino = p2_gpu.donde_esta_la_bolita_gpu(profundidad, i_bola)
finAlgoritmo = time.time()

print ("Tiempo de ejecucion del algoritmo en GPU:", (finAlgoritmo-init))

