import os
import sys 
import subprocess

outs = []

# Ejecuta 100 veces p3.py y compara la ultima linea de la salida con "True"
for i in range(10):
    # Llamar al script y capturar su salida
    first_command = ["python3", "combinar.py", "dicc10", "100", "0", "1"]

    # Run the second command and pass the output from the first command as input
    second_command = ["python3", "separarPalabras.py", "dicc10", "1", "1", "0"]

    process1 = subprocess.Popen(first_command, stdout=subprocess.PIPE)
    output1, _ = process1.communicate()

    process2 = subprocess.Popen(second_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    output, _ = process2.communicate(input=output1)

    # Decodificar la salida y obtener la última línea
    last_line = output.decode().strip().split('\n')[-1]

    outs.append(last_line=="True")

# Comprobar si todas las salidas son True
for i in outs:
    if i == False:
        print("Error en linea "+str(outs.index(i)))
        sys.exit(1)

print("Todo correcto")