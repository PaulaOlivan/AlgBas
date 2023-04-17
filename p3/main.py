import sys
import time

word_set = set()  # create an empty hash set
nombre = "/home/hsunekichi/Escritorio/algBas/p3/dicc100" #sys.argv[1]

with open(nombre+".txt", "r") as f:
    for line in f:
        word = line.strip().lower()  # remove leading/trailing whitespaces and newline characters
        word_set.add(word)   # add word to the hash set


def flatten(lst):
    """
    Flatten a list of lists recursively.
    
    Args:
    - lst (list): List of lists to be flattened.
    
    Returns:
    - list: Flattened list.
    """
    flattened = []
    for item in lst:
        if isinstance(item, list):
            flattened.extend(flatten(item))  # Recursively flatten inner lists
        else:
            flattened.append(item)
    return flattened

def serialize(lst):
    """
    Serialize a list of lists recursively.
    
    Args:
    - lst (list): List of lists to be serialized.
    
    Returns:
    - list: Serialized list.
    """
    serialized = []
    for item in lst:
        if isinstance(item, list):
            serialized.extend(serialize(item))  # Recursively serialize inner lists
        else:
            serialized.append(item)
    return serialized


#Función que devuelve verdad si y solo si palabra existe en el word set creado
def existePalabra (palabra):
    return palabra in word_set

# Almacena valores ya calculados
hash_precalculado = {}

def separarPalabras(input, init = 0):
    # Función que separa las palabras de un string y las devuelve en una lista
    # input: string
    # len_comparacion: longitud de las palabras a comparar
    # output: lista de palabras
    
    # Si ya había sido calculado, se devuelve el valor
    if init in hash_precalculado:
        return hash_precalculado[init]
                
    len_comparacion = len(input)-init
    listas = []

    end = init + len_comparacion + 1

    # Se recorre el string letra a letra
    for i in range(init+1, end):
        palabra = input[init:i]

        encontradas = []
        # Se comprueba si la palabra es de la longitud deseada
        if existePalabra(palabra):
            if len(input[i:]) != 0:
                
                encontradas = separarPalabras(input, i)
                hash_precalculado[init] = encontradas
                
                # Se añade la palabra a las listas encontradas
                if len(encontradas) > 0:
                    for lista in encontradas:
                            lista.insert(0, [palabra])
            else:
                encontradas.insert(0, [palabra])

            listas.append(encontradas)


    # Se devuelve la lista de palabras
    return listas



init = time.time_ns() 
#input = input()
input = "migala"
input = input.lower()
out = separarPalabras(input)
end = time.time_ns()
print("Exec time: ", (end-init)/1000000000, "s")
print(out)
print(serialize(out))
print(flatten(out))