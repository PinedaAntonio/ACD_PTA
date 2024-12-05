import numpy as np

array = np.random.randint(0, 51, 20)
print("Array original:")
print(array)

matriz = array.reshape(4, 5)
print("Matriz reestructurada a 4x5:")
print(matriz)

suma_columnas = matriz.sum(axis=0)
print("Suma de cada columna:")
print(suma_columnas)
