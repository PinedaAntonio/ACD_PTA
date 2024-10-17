# Pedir un número al usuario
num = int(input("Introduce un número: "));

print("Numeros pares hasta el ", num);
for i in range(1, num+1):
    if i%2 == 0:
        print(i);
