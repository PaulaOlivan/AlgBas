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
#include <bitset>

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

// Función que transforma un string en una cadena de bits
// Entrada: string normal
// Salida: vector de bits
bitset<8> aBits (string mensaje){
    bitset<8> bits;
    for (int i = 0; i < mensaje.size(); i++)
    {
        bits += bitset<8>(mensaje[i]); // Concatenar a los bits anteriores los nuevos bits del string
    }
    return bits;
}

// Función auxiliar que genera de manera global el conjunto de números C
// Entrada: array que contendrá los valores de las sumas parciales, size que es
// el tamaño de la mochila concatenada para ser semejante al tamaño del mensaje
// bitmask es el mensaje que se quiere cifrar, bitmaskSize es el tamaño de la
// máscara que debe ser igual al tamaño de la mochila concatenada
void applyBitmask(int* arr, int size, const char* bitmask, int bitmaskSize) 
{
    // Recorre los elementos de 8 en 8
    for (int i = 0; i < bitmaskSize; i++) 
    {
        char charMask = bitmask[i];
        
        for (int j = 0; j < 8; j++)
        {
            char bit = charMask & (1 << j); // Obtiene el bit j del charMask
             
            // Si la mascara es 0, se pone a 0 el elemento
            if (bit == 0) 
                arr[i*8 + j] = 0;
        }
    }
}

// Función que calcula el entero C que se transmite con el mensaje binario
// Se debe calcular un C por cada conjunto de 
// Entrada: vector con los componentes de la clave publica, mensaje a cifrar
// Salida: entero C
vector<int> numeroC (vector<int> clavePub, bitset<8> msgBits)
{
    // Llamar a la función que aplica la mascara a los bits

    // Agrupar el resultado en bloques de tamaño de la mochila para obtener los distintos C

    // Devolvemos el vector de elementos C
}


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
        std::bitset msgBits = aBits(msg); //Convertimos el mensaje a bits
        // Como el mensaje debe tener una longitud multiplo del tamaño de la mochila añadimos 0 hasta tener un tamaño multiplo
        while (msgBits.length() % mochila.size() != 0){
            msgBits = msgBits + bitset<8>(0).to_string();
        }
        cout << "Debido a que el mensaje y la mochila pueden tener tamaños no compatibles se añadiran 0 a los bits del mensaje hasta que sean compatibles" << endl;
        cout << "El mensaje final ha cifrar será el siguiente: " << msgBits.to_string() << endl;

        // Ciframos ahora el mensaje calculando el número C de cada bloque del tamaño de la mochila
        vector<int> numC;
        for (int i = 0; i<mochila.size(); i++){
            numC.push_back(calcularC())
        }
    }
}