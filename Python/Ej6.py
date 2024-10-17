# Pedir dos números al usuario
num1 = float(input("Introduce el primer número: "));
num2 = float(input("Introduce el segundo número: "));

if num1 < num2:
    print("El primer número es mayor");
elif num2 < num1:
    print("El segundo número es mayor");
else:
    print("Son iguales");
