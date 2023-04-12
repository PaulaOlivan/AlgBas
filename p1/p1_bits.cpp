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

// Función auxiliar que genera de manera global el conjunto de números C
// Entrada: array que contendrá los valores de las sumas parciales, size que es
// el tamaño de la mochila concatenada para ser semejante al tamaño del mensaje
// bitmask es el mensaje que se quiere cifrar, bitmaskSize es el tamaño de la
// máscara que debe ser igual al tamaño de la mochila concatenada
void applyBitmask(vector<int> arr, string bitmask) 
{
    // Recorre los elementos de 8 en 8
    for (int i = 0; i < bitmask.size(); i++) 
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
            suma += clavePub[j];
        }

        mensaje_cifrado.push_back(suma);
    }

    // Devolvemos el vector de elementos C
    return mensaje_cifrado;
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
        /*
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
        }*/

        // Calculamos la clave publica
        vector<int> clavePub = clavePublica(N, w, mochila);

        // Ciframos el mensaje
        vector<int> mensaje_cifrado = cifrar(clavePub, msg);

        // Mostramos el mensaje cifrado
        cout << "El mensaje cifrado es: " << endl;
        for (int i = 0; i < mensaje_cifrado.size(); i++)
        {
            cout << mensaje_cifrado[i] << " ";
        }
    }
}