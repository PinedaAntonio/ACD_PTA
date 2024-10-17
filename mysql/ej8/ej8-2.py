import pymysql
from pymysql.err import MySQLError

try:
    # Conectar a la base de datos
    conexion = pymysql.connect(
        host='localhost',
        user='usuario',
        password='usuario',
        database='mi_base_datos'
    )
    print("Conexión a la base de datos exitosa")

    plataforma_input = input("Introduce la plataforma (por ejemplo, 'pc'): ")

    cursor = conexion.cursor()

    cursor.callproc('contar_juegos2', (plataforma_input,))

    resultados = cursor.fetchall()
    for resultado in resultados:
        print(f"Número de juegos para la plataforma '{plataforma_input}': {resultado[0]}")

except MySQLError as e:
    print(f"Error de conexión a MySQL: {e}")
    
finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'conexion' in locals() and conexion.open:
        conexion.close()
        print("Conexión cerrada")
