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

    print("Iniciando transacción...")
    # Insertar un nuevo registro en la tabla Herramientas


    sql_insert = """
        INSERT INTO videojuegos (nombre, plataforma, genero, desarrollador, fecha_lanzamiento, id_tienda)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    datos_videojuegos = ("rocket league", "ps4", "deportes", "psyonix", "04-07-2018", "4")
    #Le introducimos el dato id_tienda = "4", forzando el fallo ya que el solo tenemos hasta el id = "3" en la tabla tiendas
    cursor.execute(sql_insert, datos_videojuegos)
    # Hacer commit si todo va bien
    conexion.commit()
    print("Transacción exitosa: Registro insertado correctamente.")


except MySQLError as e:
    # Si ocurre un error, hacer rollback
    print(f"Error en la transacción: {e}")
    if conexion:
        conexion.rollback()
        print("Se realizó rollback.")
    
finally:
    # Cerrar la conexión a la base de datos si está abierta
    if 'conexion' in locals() and conexion.open:
        cursor.close()
        conexion.close()
        print("Conexión cerrada")