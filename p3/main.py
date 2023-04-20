import sys
import time

sys.setrecursionlimit(200000)
word_set = set()  # create an empty hash set
nombre = sys.argv[1]
#nombre = "dicc100"

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


def separate(lst):
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
            if len(item) > 2 and isinstance(item[1], list):
                # If the item is a list with more than one element,
                # create a new list with the first element and the rest of the list
                for i in range(1, len(item)):
                    new_lst = [item[0]]
                    flattened.extend(separate(new_lst))  # Recursively flatten the new list
                    new_lst.append(item[i])

            else:
                # If the item is a list with only one element, flatten it recursively
                flattened.extend(separate(item))
        else:
            flattened.append(item)
    return flattened



def sublist_is_in_list(sublist, lst):
    # Check for Sublist in List
    # Using loop + list slicing
    res = False
    for idx in range(len(lst) - len(sublist) + 1):

        if lst[idx: idx + len(sublist)] == sublist:
            res = True
            break

    return res

def read_words_from_file(file_name):
    with open(file_name, 'r') as file:
        words = [line.strip() for line in file]
    return words

    

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
                hash_precalculado[i] = [flatten(encontradas).copy()]
                
                # Se añade la palabra a las listas encontradas
                if len(encontradas) > 0:
                    if isinstance(encontradas[0], list):
                        for lista in encontradas:
                                lista.insert(0, [palabra])
            else:
                encontradas.insert(0, [palabra])

            if len(encontradas) > 0:
                listas.append(encontradas)


    # Se devuelve la lista de palabras
    return listas


init = time.time_ns() 
input = input()
#input = "cuernoshipnotizarafilarmigala"
#input = input.lower()
out = separarPalabras(input)
end = time.time_ns()
print("Exec time: ", (end-init)/1000000000, "s")

flattened_out = separate(out)
#print(out)
#print(flattened_out)

query_inicial = read_words_from_file("lista.txt")
#query_inicial = ["mi", "gala", "servir", "toallero"]
#print(query_inicial)
#print(sublist_is_in_list(query_inicial, flattened_out))