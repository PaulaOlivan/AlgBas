import time
import p2_gpu
import numpy as np
import sys

# Argumentos: p2.py profundidad(int) i_bola(int) usar_fuerza_bruta(0/1)

def dondeEstaLaBolita (profundidad, i_bolita):
    
    pos = 1
    camino = []
    for p in range(1, profundidad):
        indice_en_profundidad = (i_bolita-1) % 2**p
        
        if indice_en_profundidad < 2**(p-1):
            pos = pos*2
            camino.append('I')
        else: 
            pos = (pos*2)+1
            camino.append('D')

    return camino, pos


class Nodo:
    def __init__(self, posicion = 1, direccion = 'I'):
        self.direccion = direccion
        self.posicion = posicion
        self.left = None
        self.right = None

def create_complete_tree(p, initDir='I', posicion=1):
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
    elif nodo.direccion == 'I':
        nodo.direccion = 'D'
        camino = ['I']
        camino.extend(bolasFB(i, nodo.left))
        return camino
    else:
        nodo.direccion = 'I'
        camino = ['D']
        camino.extend(bolasFB(i, nodo.right))
        return camino


profundidad = int(sys.argv[1])
i_bola = int(sys.argv[2])
usar_fuerza_bruta = bool(int(sys.argv[3]))


nBolas = np.left_shift(1, profundidad-1) #El numero total de bolas es el número de nodos en la capa de las hojas

init = time.process_time()
camino_cpu, pos = dondeEstaLaBolita(profundidad, i_bola)
finAlgoritmo = time.process_time()

print ("Tiempo de ejecucion del algoritmo en CPU:", finAlgoritmo-init)


if usar_fuerza_bruta:
    init = time.process_time()
    raiz = create_complete_tree(profundidad, 'I', 1)
    camino_fb = colocarBolas(nBolas, raiz, i_bola)
    finFB = time.process_time()
    print ("Tiempo de ejecucion del método de fuerza bruta:", finFB-init)
    
    if np.array_equal(camino_cpu, camino_fb):
        print("Los caminos son iguales")
    else:
        print("Los caminos son diferentes")
        print("Camino CPU:", camino_cpu)
        print("Camino FB:", camino_fb)


init = time.process_time()
camino = p2_gpu.donde_esta_la_bolita_gpu(profundidad, i_bola)
finAlgoritmo = time.process_time()

print ("Tiempo de ejecucion del algoritmo en GPU:", finAlgoritmo-init)

