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

    cursor.execute("UPDATE videojuegos SET id_tienda = %s WHERE nombre = %s", (2, 'concord'))
    conexion.commit()
    print(cursor.rowcount, "registro(s) actualizado(s)")

except MySQLError as e:
    print(f"Error de conexión a MySQL: {e}")
    
finally:
    if 'conexion' in locals() and conexion.open:
        conexion.close()
        print("Conexión cerrada")
