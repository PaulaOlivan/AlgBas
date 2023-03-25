/*
* Autores: Hugo Mateo (816678) & Paula Oliván (771938)
* Fecha de creación: 24-02-23
* Información: Fichero que implementa las funciones principales de la práctica
*              1 de la asignatura de Algoritmia Básica
*/

#include <iostream>
#include <string>
#include <vector>

using namespace std;

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

bool esPrimo (int n)
{
    bool esPrimo = true;

    int sqrtN = int(sqrt(n)+1);

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

// Función que calcula la clave publica del usuario.
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

// Función que calcula el entero C que se transmite con el mensaje binario
// Entrada: vector con los componentes de la clave publica, mensaje a cifrar
// Salida: entero C
int calcularC (vector<int> clavePub, string msg)
{
    int C = 0;
    
    for (int i = 0; i < msg.size(); i++)
    {
        C = C + (msg[i] * clavePub[i]);
    }

    return C;
}

// REVISAR
// Función que cifra el array con el algoritmo de ElGamal
// Entrada: N, w, mochila cumpliendo los requisitos de la práctica
// Salida: vector con los componentes de cifrado
vector<int> cifrarVector (int N, int w, vector<int> mochila)
{
    vector<int> vecCifr;

    int nMochila = mochila.size();

    for (int i = 0; i < nMochila; i++)
    {
        vecCifr.push_back((mochila[i] * w) % N);
    }

    return vecCifr;
}

// REVISAR
// Función que cifra el mensaje 
// Entrada: vector con los componentes de cifrado, mensaje a cifrar
// Salida: vector con los componentes cifrados del mensaje
vector<int> cifrarMensaje (vector<int> vecCifr, string msg)
{
    vector<int> msgCifr;

    int nVecCifr = vecCifr.size();

    for (int i = 0; i < msg.size(); i++)
    {
        int charCifr = 0;
        for (int j = 0; j < nVecCifr; j++)
        {
            charCifr = charCifr +  (msg[i] * vecCifr[j]);
            msgCifr.push_back((msg[i] * vecCifr[i]));
        }
            
    }

    return msgCifr;
}


// sintaxis: p1 N w e1 e2 e3...
int main (int argc, char *argv[]){

    int N = stoi(argv[1]);
    int w = stoi(argv[2]);
    int suma;                   // Suma de los elementos de la mochila
    string msg = "HAY";         // Mensaje a cifrar VER COMO HACERLO EN LOS ARGUMENTOS

    vector<int> mochila;

    for (int i = 3; i < argc; i++)  // Recoge la clave privada
    {
        mochila.push_back(stoi(argv[i]));
    }

    if (w  < 0 || N < w)
    {
        cerr << "Por favor, intruduzca w y N t.q. 0 < w < N" << endl;
    }

    if (!esPrimo(w)){
        cerr << "Por favor, intruduzca w t.q. w sea un número primo" << endl;
    }

    if (!mochilaFacil(mochila, suma))
    {
        cerr << "La mochila debe ser facil (todo e en la mochila es mayor que la suma de las e previas)";
    }

    if (suma > N)
    {
        cerr << "Por favor, intruduzca N y los elementos de la mochila t.q. N > e_1 + e_2 + ... + e_n" << endl;
    }

    else {
        vector<int>vecCifr  = cifrarVector (N, w, mochila);
        vector<int>msgCifr = cifrarMensaje (vecCifr, msg);
    }

    
}