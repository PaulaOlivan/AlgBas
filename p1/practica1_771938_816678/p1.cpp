/*
* Autores: Hugo Mateo (816678) & Paula Oliván (771938)
* Fecha de creación: 24-02-23
* Información: Fichero que implementa las funciones principales de la práctica
*              1 de la asignatura de Algoritmia Básica
*/

#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include <chrono>

using namespace std;

// Función que comprueba si una mochila cumple la premisa de la mochila fácil
// Entrada: mochila, suma del valor
// Salida: true si cumple la premisa, false en caso contrario
bool mochilaFacil (vector<int> mochila, int &suma)
{
    bool correcto = true;
    int nMochila = mochila.size();

    suma = 0;

    // Para cada dato en la mochila, el dato 0 nunca incumplirá la premisa
    for (int i = 1; i < nMochila; i++) 
    {
        suma += mochila[i-1];

        if (mochila[i] < suma)
            correcto = false;
    }

    suma += mochila[nMochila-1];

    return correcto;
}

// Función que comprueba si un número es primo
// Entrada: número a comprobar
// Salida: true si es primo, false en caso contrario
bool esPrimo (int n)
{
    bool esPrimo = true;

    int sqrtN = int(sqrt(n) + 1);

    for (int i = 2; i < sqrtN; i++)
    {
        if (n % i == 0)
            esPrimo = false;
    }
    return esPrimo;
}

// Función que calcula w^-1 (mod N) para poder realizar el descifrado del
// calculado
// Entrada: N, w
// Salida: w^-1 (mod N)
int inverso (int N, int w)
{
    int inverso = 0;
    int i = 1;

    while (inverso == 0)
    {
        if ((w * i) % N == 1)
            inverso = i;
        i++;
    }

    return inverso;
}

// Función que calcula la clave publica del usuario. La clave publica es el 
// vector con los a_i
// Entrada: N, w, mochila
// Salida: vector con los componentes de la clave publica
vector<int> clavePublica (int N, int w, vector<int> mochila)
{
    vector<int> clavePub;

    int nMochila = mochila.size();

    for (int i = 0; i < nMochila; i++)
    {
        clavePub.push_back((mochila[i] * w) % N);
    }

    return clavePub;
}

// Función auxiliar que genera de manera global el conjunto de números C
// Entrada: array que contendrá los valores de las sumas parciales, size que es
// el tamaño de la mochila concatenada para ser semejante al tamaño del mensaje
// bitmask es el mensaje que se quiere cifrar, bitmaskSize es el tamaño de la
// máscara que debe ser igual al tamaño de la mochila concatenada
void applyBitmask(vector<int> &arr, string bitmask) 
{
    // Recorre los elementos de 8 en 8
    for (int i = 0; i < bitmask.size(); i++) 
    {
        char charMask = bitmask[i];

        for (int j = 0; j < 8; j++)
        {
            int exponente = (128 >> j);
            char bit = charMask & exponente; // Obtiene el bit j del charMask
            
            // Si la mascara es 0, se pone a 0 el elemento
            if (bit == 0) 
                arr[i*8 + j] = 0;
        }
    }
}

// Función que cifra el mensaje pasado como argumento con la clave publica de 
// un usuario
// Entrada: clave publica, mensaje a cifrar
// Salida: vector con los elementos C que actuan como mensaje cifrado
vector<int> cifrar (vector<int> clavePub, string msj)
{
    vector<int> clavePub_extendida;

    // Extender la clave publica para que tenga el mismo tamaño que el mensaje
    while (clavePub_extendida.size() < msj.size()*8)
    {
        clavePub_extendida.insert(clavePub_extendida.end(), clavePub.begin(), clavePub.end());
    }

    // Si la clave publica extendida es mayor que el mensaje, se elimina el exceso
    while (clavePub_extendida.size() > msj.size()*8)
    {
        clavePub_extendida.pop_back();
    }

    // Llamar a la función que aplica la mascara a los bits
    applyBitmask(clavePub_extendida, msj);

    vector<int> mensaje_cifrado;
    
    // Agrupar el resultado en bloques de tamaño de la mochila para obtener los distintos C
    int nElem = clavePub_extendida.size()/clavePub.size();
    for (int i = 0; i < nElem; i++)
    {
        // Sumar los elementos de la mochila
        int suma = 0;
        for (int j = 0; j < clavePub.size(); j++)
        {
            suma += clavePub_extendida[i*clavePub.size()+j];
        }

        mensaje_cifrado.push_back(suma);
    }

    // Devolvemos el vector de elementos C
    return mensaje_cifrado;
}

// Función que descifra el mensaje pasado como argumento con la clave privada de
// un usuario y uno de los elementos C
// Entrada: clave privada, elemento C
// Salida: carácter que corresponde al elemento C descifrado
unsigned char descifrarBloque(vector<int> clavePriv, int numC)
{
    unsigned char bloque = 0;
    
    for (int i=(clavePriv.size()-1); i >= 0; i--){
        
        bloque >>= 1;  // Añade espacio para el bit a la izquierda

        if (clavePriv[i] <= numC){
            numC = numC - clavePriv[i];
            bloque += 128;     // Añade un 1 a la izquierda
        }        
    }

    bloque >>= (8-clavePriv.size());    // Mueve el bloque a la derecha

    return bloque;
}

// Función que permite generar los bits de un char
// Entrada: char a mostrar
// Salida: muestra por pantalla los bits del char
void printCharBits(unsigned char ch)
{    
    for (int k = 0; k < 8; k++)
    {   
        unsigned char bit = 0;

        if (ch >> 7) // Ultimo bit
            bit = 1;

        ch <<= 1;
        cout << int(bit);
    }
}

// Función que descifra el mensaje pasado como argumento con la clave privada de
// un usuario y los elementos C a descifrar
// Entrada: clave privada (N, w, clavePrivada), elementos C
// Salida: vector con los caracteres descifrados
vector<char> descifrado (int N, int w, vector<int> msgCifrado, vector<int> clavePriv){
    int w_inv = inverso(N, w);
    vector<char> msgOriginal;
    //cout << endl << "El primer paso del descifrado da: ";
    for (int &valor : msgCifrado){
        valor = (valor * w_inv) % N;
        //cout << to_string(valor) + " ";
    }
    cout << endl;

    int nBloques = 8/clavePriv.size();
    //cout << endl << "El numero de bloques es: " << nBloques << endl;
    int nChars = msgCifrado.size()/nBloques;
    //cout << endl << "El numero de caracteres es: " << nChars << endl;

    // Aplicamos la mochila, clave privada
    for (int i=0; i < nChars; i++){
        
        unsigned char nDescifrado = 0;
        
        for (int j=0; j < nBloques; j++)
        {
            int posicion = i*nBloques + j;
            int numC = msgCifrado[posicion];

            unsigned char bloque = descifrarBloque(clavePriv, numC);

            // Añade espacio para el bloque en el caracter descifrado
            nDescifrado <<= clavePriv.size();   
            nDescifrado += bloque;
        }

        msgOriginal.push_back(nDescifrado);
    }

    return msgOriginal;
}

int main (int argc, char *argv[]){

    std::chrono::steady_clock::time_point tiempo_inicio = std::chrono::steady_clock::now();

    int N = stoi(argv[1]);
    int w = stoi(argv[2]);

    // Suma de los elementos de la mochila
    int suma;                   

    string msg = argv[3];

    vector<int> mochila;

    for (int i = 4; i < argc; i++)  // Recoge la clave privada
    {
        mochila.push_back(stoi(argv[i]));
    }

    
    float resto = 8 % mochila.size();
    if (resto != 0){
        cerr << "La mochila debe tener un tamaño divisor de 8 debido a que se van a cifrar carácteres" << endl;
    }

    else if (w  < 0 || N < w)
    {
        cerr << "Por favor, intruduzca w y N t.q. 0 < w < N" << endl;
    }
    else if (!esPrimo(w)){
        cerr << "Por favor, intruduzca w t.q. w sea un número primo" << endl;
    }
    else if (!mochilaFacil(mochila, suma))
    {
        cerr << "La mochila debe ser facil (todo e en la mochila es mayor que la suma de las e previas)";
    }
    else if (suma > N)
    {
        cerr << "Por favor, intruduzca N y los elementos de la mochila t.q. N > e_1 + e_2 + ... + e_n" << endl;
    }


    else {

        cout << "El mensaje a cifrar es: " << msg << endl;
        cout << "El número N escogido es: " << N << endl;
        cout << "El número w escogido es: " << w << endl;
        cout << "La mochila escogida como clave privada es: ";
        vector<int> mochilaCopia(mochila);
        
        for (int i=0; i<mochila.size(); i++){
            int elem = mochilaCopia[i];
            cout << elem << " ";
        }
        cout << endl;

        // Calculamos la clave publica
        vector<int> clavePub = clavePublica(N, w, mochila);

        cout << endl << "Clave publica: ";
        for (auto elem : clavePub)
        {
            cout << elem << " ";
        }
        std::chrono::steady_clock::time_point inicio_cifrar = std::chrono::steady_clock::now();
        // Ciframos el mensaje
        vector<int> mensaje_cifrado = cifrar(clavePub, msg);
        std::chrono::steady_clock::time_point fin_cifrar = std::chrono::steady_clock::now();
        std::chrono::duration<double> tiempo_cifrar = std::chrono::duration_cast<std::chrono::duration<double>>(fin_cifrar - inicio_cifrar);
        cout << endl << "Tiempo de cifrado: " << tiempo_cifrar.count() << " segundos" << endl;

        // Mostramos el mensaje cifrado
        cout << endl <<"El mensaje cifrado es: ";

        for (int i = 0; i < mensaje_cifrado.size(); i++)
        {
            cout << mensaje_cifrado[i] << " ";
        }
        cout << endl;

        std::chrono::steady_clock::time_point inicio_descifrar = std::chrono::steady_clock::now();
        // Desciframos el mensaje y lo mostramos por pantalla
        vector<char>origen = descifrado(N, w, mensaje_cifrado, mochila);
        std::chrono::steady_clock::time_point fin_descifrar = std::chrono::steady_clock::now();
        std::chrono::duration<double> tiempo_descifrar = std::chrono::duration_cast<std::chrono::duration<double>>(fin_descifrar - inicio_descifrar);
        cout << endl << "Tiempo de descifrado: " << tiempo_descifrar.count() << " segundos" << endl;
        
        cout << "El mensaje original es: ";
        for (int i=0; i<origen.size(); i++){
            cout << origen[i];
        }
        cout << endl << endl;

        std::chrono::steady_clock::time_point tiempo_final = std::chrono::steady_clock::now();
        std::chrono::duration<double> tiempo_transcurrido = std::chrono::duration_cast<std::chrono::duration<double>>(tiempo_final - tiempo_inicio);
        cout << "Tiempo de ejecución: " << tiempo_transcurrido.count() << " segundos" << endl;
    }
}