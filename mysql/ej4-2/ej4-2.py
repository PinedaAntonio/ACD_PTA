import pymysql
from pymysql.err import MySQLError

import time
start_time = time.time()
#Hacemos operaciones

try:
    conexion = pymysql.connect(
        host='localhost',
        user='usuario',
        password='usuario',
        database='mi_base_datos'
    )
    print("Conexión a la base de datos exitosa")
    
    
    a = 0
    cursor = conexion.cursor()
    while a < 9999:
        a += 1 
        cursor.execute("SELECT * FROM videojuegos")
        resultados = cursor.fetchall()
    cursor.close()

except MySQLError as e:
    print(f"Error de conexión a MySQL: {e}")
    
finally:
    if 'conexion' in locals() and conexion.open:
        conexion.close()
        print("Conexión cerrada")

end_time = time.time()
print(f"Tiempo de inserción con pymysql: {end_time - start_time} segundos")