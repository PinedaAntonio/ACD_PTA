import numpy as np
random = np.random.randint(1, 10, (4, 4))
print(random)
primer_numero_DNI = 3 #Mi dni es 30284761V
np.fill_diagonal(random, primer_numero_DNI)

print("Matriz modificada:")
print(random)