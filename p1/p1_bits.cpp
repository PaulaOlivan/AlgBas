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

string aBits (string mensaje){
    string bits = "";
    for (int i = 0; i < mensaje.size(); i++)
    {
        bits += bitset<8>(mensaje[i]).to_string();
    }
    return bits;
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

    else{

    }
}