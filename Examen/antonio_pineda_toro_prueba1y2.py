import pymysql
from pymysql.err import MySQLError

try:
    conexion = pymysql.connect(
        host='localhost',
        user='usuario',
        password='usuario',
        database='1dam'
    )
    print("Conexión a la base de datos exitosa")

    cursor = conexion.cursor()

    crear_tabla = """
        CREATE TABLE IF NOT EXISTS libros (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(255),
            genero VARCHAR(255),
            año_publicacion VARCHAR(4),
            libreria_origen VARCHAR(255)
        )
    """

    cursor.execute(crear_tabla)
    print("tabla creada con éxito")
    
    
except MySQLError as e:
    print(f"Error de conexión a MySQL: {e}")

finally:
    if 'conexion' in locals() and conexion.open:
        conexion.close()
        print("Conexión cerrada")