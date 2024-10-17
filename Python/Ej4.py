import math
numero = input("Introduce un número por favor. ");
numero_float = float(numero);
a = int(1);

print("Tabla del ", numero);
while a < 11:
    print(numero, "x", a, "=", math.trunc(numero_float * a));
    a += 1
