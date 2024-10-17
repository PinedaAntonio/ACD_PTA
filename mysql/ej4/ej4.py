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

    #Crear la tabla tiendas
    crear_tienda = """
        CREATE TABLE IF NOT EXISTS tiendas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL,
            direccion VARCHAR(100)
        )
    """
    cursor.execute(crear_tienda)

    #Añadir el campo "id_tienda" a la tabla videojuegos
    
    sql_alter_videojuegos = """
    ALTER TABLE videojuegos ADD id_tienda INT,
    ADD CONSTRAINT fk_tienda
    FOREIGN KEY (id_tienda) REFERENCES tiendas(id)
    """

    cursor.execute(sql_alter_videojuegos)
    print("Relación entre videojuegos y tiendas creada.")

except MySQLError as e:
    print(f"Error de conexión a MySQL: {e}")
    
finally:
    if 'conexion' in locals() and conexion.open:
        conexion.close()
        print("Conexión cerrada")
