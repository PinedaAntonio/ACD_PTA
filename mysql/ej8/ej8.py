import pymysql
from pymysql.err import MySQLError

try:
    conexion = pymysql.connect(
        host='localhost',
        user='usuario',
        password='usuario',
        database='mi_base_datos'
    )
    print("Conexión a la base de datos exitosa")

    cursor = conexion.cursor()

    cursor.callproc('contar_juegos')
    # se usa un metodo diferente ya que pymysql no tiene función stored_results
    resultados = cursor.fetchall()
    for resultado in resultados:
        print(resultado)

except MySQLError as e:
    print(f"Error de conexión a MySQL: {e}")
    
finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
    # Cerrar la conexión a la base de datos si está abierta
    if 'conexion' in locals() and conexion.open:
        conexion.close()
        print("Conexión cerrada")