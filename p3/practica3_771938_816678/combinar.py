import random
import sys

word_set = list()  # create an empty list
nombre = sys.argv[1]
n_comb = int(sys.argv[2])
nMigalas = int(sys.argv[3])
mutar = sys.argv[4] == "1"

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
            combinaciones.extend(seleccion)  # agregamos la combinación a la lista de combinaciones

        return combinaciones


size = 1


resultado = generar_strings(word_set, size, n_comb)
combinacion = "".join(resultado)  # unimos las palabras seleccionadas con un espacio

prob_mutacion = 1/(len(combinacion)*10)

real = "Si"

# Mutar la combinación
for i in range(len(combinacion)):
    if random.random() < prob_mutacion:
        while True:
            new_character = random.choice('abcdefghijklmnopqrstuvwxyz')
            if new_character != combinacion[i]:
                break
            
        combinacion = combinacion[:i] + new_character + combinacion[i+1:]
        real = "No"


for i in range(nMigalas):
    combinacion = "migala"+combinacion

# Open the file for writing
with open('lista.txt', 'w') as f:
    # Write some data to the file
    #for line in resultado:
    #   f.write(line+"\n")
    f.write(real)

print(combinacion)
