import random
import mysql.connector
from mysql.connector import Error

import time
start_time = time.time()
#Hacemos operaciones

plataformas = ['ps4', 'xbox one', 'pc', 'switch']
generos = ['shooter', 'supervivencia', 'aventura', 'puzles']
desarrolladores = ['ubisoft', 'square enix', 'naughty dog', 'blizzard']
fechas = ['4/24', '3/23', '7/24', '9/23']

try:
    conexion = mysql.connector.connect(
        host='localhost',
        user='usuario',
        password='usuario',
        database='mi_base_datos'
    )
    if conexion.is_connected():
        print("Conexión a la base de datos exitosa")
    
    a = 0
    cursor = conexion.cursor()
    while a < 9999:
        a += 1
        nombre = f"Juego {a+1}"
        plataforma = random.choice(plataformas)
        genero = random.choice(generos)
        desarrollador = random.choice(desarrolladores)
        fecha = random.choice(fechas)  
        cursor.execute(
        "INSERT INTO videojuegos (nombre, plataforma, genero, desarrollador, fecha_lanzamiento) VALUES (%s, %s, %s, %s, %s)",
        (nombre, plataforma, genero, desarrollador, fecha)
    )
        

except Error as e:
    print(f"Error de conexión: {e}")
finally:
    if conexion.is_connected():
        conexion.close()
        print("Conexión cerrada")

end_time = time.time()
print(f"Tiempo de inserción con mysql-connector: {end_time - start_time} segundos")