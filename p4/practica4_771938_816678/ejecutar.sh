# Script que se encarga de la automatización del compilado del programa y su ejecución
# Autor: Hugo Mateo Trejo (816678) & Paula Oliván Usieto (771938)
# Fecha de creación: 17/04/2023

#!/bin/bash

# Agregar permisos de ejecución al archivo p1
chmod +x transporte.py
chmod +x transporte_pl.py
chmod +x transporte_profundidad.py
chmod +r pruebas.txt
chmod +r errores.txt
chmod +r rendimiento.txt

# Ejecutar el programa si no se proporcionan argumentos al script
if [ $# -eq 0 ]; 
then

    # Probamos el programa con los datos de prueba
    echo "Lanzamos el programa para probar los datos de pruebas.txt con ramificación y poda"
    python3 transporte.py pruebas.txt

    # Probamos el programa con los datos en prueba en PL
    echo "Lanzamos el programa para probar los datos de pruebas.txt con PL"
    python3 transporte_pl.py pruebas.txt

    # Probamos el programa con los datos de prueba en profundidad 
    echo "Lanzamos el programa para probar los datos de pruebas.txt con búsqueda en profundidad, añadido como extra"
    python3 transporte_profundidad.py pruebas.txt


    # Probamos el programa con los datos incorrectos para comprobar los casos 
    # de error
    #echo "Lanzamos el programa para probar las pruebas de error de errores.txt"
    #python3 transporte.py errores.txt
    #python3 transporte_pl.py errores.txt
    #python3 transporte_profundidad.py errores.txt

    # Probamos el programa con los datos de rendimeinto para comprobar la eficiencia 
    # de nuestros programas
    #echo "Lanzamos el programa para probar las pruebas de rendimiento de rendimiento.txt"
    #python3 transporte.py rendimiento.txt
    #python3 transporte_pl.py rendimiento.txt
    #python3 transporte_profundidad.py rendimiento.txt

fi