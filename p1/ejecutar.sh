# Script que se encarga de la automatización del compilado del programa y su ejecución
# Autor: Hugo Mateo Trejo (816678) & Paula Oliván Usieto (771938)
# Fecha de creación: 16/04/2023

#!/bin/bash

# Compilar el archivo p1.cpp en C++11 y generar el ejecutable p1
g++ -std=c++11 p1.cpp -o p1

# Agregar permisos de ejecución al archivo p1
chmod +x p1

# Ejecutar el programa si no se proporcionan argumentos al script
if [ $# -eq 0 ]; then
    # Probamos el programa con los datos de prueba con mochila de tamaño 2
    echo "Probamos con una mochila de tamaño 2"
    #./p1 85 11 "Este mensaje no podrá ser descifrado" 15 20
    #./p1 85 11 "Buenos días Mario, ¿qué tal ayer la pesca?" 20 45
    # Probamos el programa con los datos de prueba con mochila de tamaño 4
    echo "Ahora probamos con una mochila de tamaño 4"
    #./p1 85 11 "Continuamos haciendo pruebas aumentando la mochila" 1 15 20 45
    #./p1 1500 11 "Parece que con 4 elementos la mochila sigue funcionando bien :)" 15 20 45 85
    # Probamos el programa con los datos de prueba con mochila de tamaño 8
    echo "Ahora probamos con una mochila de tamaño 8"
    #./p1 1500 11 "Empezamos las pruebas con el máximo tamaño de la mochila" 1 15 20 45 85 170 340 700
    ./p1 1500 11 "Esta es la última prueba del script, ¿irá todo bien?" 1 15 20 45 85 170 340 700
fi