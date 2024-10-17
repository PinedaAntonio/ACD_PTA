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


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS videojuegos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255),
            plataforma VARCHAR(255),
            genero VARCHAR(255),
            desarrollador VARCHAR(255),
            fecha_lanzamiento VARCHAR(255)
        )
    """)


    cursor.execute(
        "INSERT INTO videojuegos (nombre, plataforma, genero, desarrollador, fecha_lanzamiento) VALUES (%s, %s, %s, %s, %s)",
        ("The last of us", "ps3", "aventura", "naughty dog", "14-06-2013")
    )


    conexion.commit()


    cursor.execute("SELECT * FROM videojuegos")
    for fila in cursor.fetchall():
        print(fila)

except MySQLError as e:
    print(f"Error en la operación MySQL: {e}")

finally:

    if 'conexion' in locals() and conexion.open:
        conexion.close()
        print("Conexión cerrada")