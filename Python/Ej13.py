import random;

#Creamos una lista vacía
numeros = [];

for i in range (1, 11):
#Usamos la librería random, cuya función randint genera un número aleatorio,
#en este caso, es un entero entre 1 y 50
    numeros.append(random.randint(1, 50));


num1 = float(input("Introduce un número: "));
if num1 in numeros :
    print("Bingo!");
else :
    print("El número no está en la lista");
print ("La lista era: ", numeros);
