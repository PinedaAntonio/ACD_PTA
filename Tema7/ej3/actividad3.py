import numpy as np
array = np.random.randint(0, 101, 10)
print("Array original:")
print(array)
valores_mayores_50 = array[array > 50]
print("Valores mayores a 50:")
print(valores_mayores_50)