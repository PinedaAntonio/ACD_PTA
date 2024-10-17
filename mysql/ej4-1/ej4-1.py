import mysql.connector
from mysql.connector import Error

import time
start_time = time.time()
#Hacemos operaciones

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
        cursor.execute("SELECT * FROM videojuegos")
        resultados = cursor.fetchall()
        
    cursor.close()
except Error as e:
    print(f"Error de conexión: {e}")
finally:
    if conexion.is_connected():
        conexion.close()
        print("Conexión cerrada")

end_time = time.time()
print(f"Tiempo de inserción con mysql-connector: {end_time - start_time} segundos")