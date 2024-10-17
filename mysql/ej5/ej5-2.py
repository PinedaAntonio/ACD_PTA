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

    cursor.execute("DELETE FROM videojuegos WHERE id_tienda = %s", (2))
    conexion.commit()
    print(cursor.rowcount, "registro(s) eliminado(s)")

except MySQLError as e:
    print(f"Error de conexión a MySQL: {e}")
    
finally:
    if 'conexion' in locals() and conexion.open:
        conexion.close()
        print("Conexión cerrada")
