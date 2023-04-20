import random
import sys
import numpy as np

word_set = list()  # create an empty list
nombre = sys.argv[1]

with open(nombre+".txt", "r") as f:
    for line in f:
        word = line.strip().lower()  # remove leading/trailing whitespaces and newline characters
        word_set.append(word)   # add word to the hash set




def generar_strings(lista_palabras, size, n_comb=10):
    combinaciones = []
    if size > len(lista_palabras):
        return "Error: n es mayor que el tamaño de la lista"
    else:
        for i in range(n_comb):  # generamos n_comb combinaciones aleatorias
            seleccion = random.sample(lista_palabras, size)  # seleccionamos n palabras aleatorias de la lista
            #combinacion = "".join(seleccion)  # unimos las palabras seleccionadas con un espacio
            combinaciones = np.append(combinaciones, seleccion, axis=0)  # agregamos la combinación a la lista de combinaciones

        return combinaciones


# Ejemplo de uso:
size = int(sys.argv[2])
n_comb = int(sys.argv[3])

resultado = generar_strings(word_set, size, n_comb)
combinacion = "".join(resultado)  # unimos las palabras seleccionadas con un espacio

#for i in range(15):
    #combinacion = "migala"+combinacion

# Open the file for writing
with open('lista.txt', 'w') as f:
    # Write some data to the file
    for line in resultado:
        f.write(line+"\n")


print(combinacion)