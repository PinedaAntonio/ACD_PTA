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

    cursor.execute("SELECT id, nombre, plataforma, genero, desarrollador, fecha_lanzamiento, id_tienda FROM videojuegos LIMIT 5")
    
    print("\nMostrando resultados uno por uno:")
    
    fila = cursor.fetchone()
    while fila:
        print(f"ID: {fila[0]}, Nombre: {fila[1]}, Plataforma: {fila[2]}, Género: {fila[3]}, Desarrollador: {fila[4]}, Fecha de Lanzamiento: {fila[5]}, ID Tienda: {fila[6]}")
        fila = cursor.fetchone()

    cursor.close()

    cursor = conexion.cursor()

    cursor.execute("SELECT id, nombre, plataforma, genero, desarrollador, fecha_lanzamiento, id_tienda FROM videojuegos LIMIT 5")
    
    print("\nMostrando resultados uno por uno de nuevo:")
    
    fila = cursor.fetchone()
    while fila:
        print(f"ID: {fila[0]}, Nombre: {fila[1]}, Plataforma: {fila[2]}, Género: {fila[3]}, Desarrollador: {fila[4]}, Fecha de Lanzamiento: {fila[5]}, ID Tienda: {fila[6]}")
        fila = cursor.fetchone()

    cursor.close()

except MySQLError as e:
    print(f"Error de conexión a MySQL: {e}")
    
finally:
    # Cerrar la conexión a la base de datos si está abierta
    if 'conexion' in locals() and conexion.open:
        conexion.close()
        print("Conexión cerrada")
