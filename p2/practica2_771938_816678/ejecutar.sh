# Script que se encarga de la automatización del compilado del programa y su ejecución
# Autor: Hugo Mateo Trejo (816678) & Paula Oliván Usieto (771938)
# Fecha de creación: 17/04/2023

#!/bin/bash

# Agregar permisos de ejecución al archivo p1
chmod +x p1

# Ejecutar el programa si no se proporcionan argumentos al script
if [ $# -eq 0 ]; then
    # Probamos el programa con los datos de prueba
    echo "Lanzamos el programa para probar los datos de pruebas.txt"
    ./python3 p2.py pruebas.txt resultados.txt 

fi