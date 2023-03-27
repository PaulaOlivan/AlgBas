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

// Función que calcula el entero C que se transmite con el mensaje binario
// Se debe calcular un C por cada CHAR del mensaje a transmitir
// Entrada: vector con los componentes de la clave publica, mensaje a cifrar
// Salida: entero C
vector<int> numeroC (vector<int> clavePub, string palabra)
{
    vector <int> C;

    for (auto i = palabra.begin(); i != palabra.end(); i++) {
        
        // Recorremos cada char del string
        int suma = 0;

        for (int j = 0; j < clavePub.size(); j++) // Recorremos cada bit de la letra
        {
            // conseguimos el bit i-esimo del char letra
            char bit = ((*i >> j) & 1) ? '1' : '0';
            suma = suma + (bit * clavePub[j]);
        }

        C.push_back(suma); // Guardamos la suma de la letra iterada en el vector
    }
    return C;
}

// Función que descifra el mensaje
// Entrada: clave privada (mochila), vector con el mensaje cifrado, w, N
// Salida: mensaje descifrado
char letraDescifrada (vector<int> C, vector<int>mochila, int w, int N) // Mirar como guardar la C en un vector
{
    int inversoW = inverso(N, w); // Calculamos el inverso de w (mod N)
    vector<int> C_descifrado; // Vector con los valores de C descifrados

    for (int i = 0; i < C.size(); i++)
    {
        C_descifrado.push_back((C[i] * inversoW)%N); //Obtenemos los valores de C descifrados, en el ejemplo (3, 31, 36)
    }

    // Convertimos cada valor de C_descifrado en una cadena de bits que multiplicaremos por los elementos de la clave privada
    // y sumaremos para obtener el valor de la letra descifrada
    char letra = 0;
    

    // Con el valor de C descifrado y la clave privada (mochila) debemos conseguir el mensaje original

    return letra;
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
        // Para cifrar el mensaje se debe pasar letra a letra del string msg a
        // enviar, de cada letra se calcula el entero C y se enviaría el vector.

        // Para descifrar el mensaje se debe calcular el inverso de w (mod N) y
        // multiplicar el entero C recibido por el inverso de w (mod N).

        // Una vez tenemos el vector de w^-1 * C, se debe calcular el mensaje 
        // original, MIRAR COMO SE HACE EN EL PDF QUE ESTA CONFUSO
    } 
}