import math
numero = input("Introduce un número por favor. ");
numero_int = int(numero);

print("Numeros pares hasta el ", numero);
for i in range(0, numero_int+1, 2):
    print(i);
