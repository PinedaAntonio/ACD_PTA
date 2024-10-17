num1 = float(input("Introduce el primer número: "));
num2 = float(input("Introduce el segundo número: "));


def mayor (a, b):
    if a < b:
        return b;
    elif b < a:
        return a;
    


if num1 == num2:
    print("Son iguales");
else:
    print("El número mayor es: ", mayor(num1, num2));

