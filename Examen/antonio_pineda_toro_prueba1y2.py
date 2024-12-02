import pymysql
from pymysql.err import MySQLError
import csv
import json

class MySQLToFile:
    def __init__(self, connection):
        self.connection = connection  # Recibe la conexión como parámetro

    def write_to_json(self, table_name, json_file, membresia):
        if not self.connection or not self.connection.open:
            print("No se pudo establecer conexión con MySQL.")
            return

        try:
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(f"SELECT * FROM {table_name} where membresía=\"" + membresia + "\"")
            records = cursor.fetchall()

            # Escribir los registros en el archivo JSON
            with open(json_file, 'w') as file:
                json.dump(records, file, indent=4)

            print(f"Datos de '{table_name}' guardados en '{json_file}'.")

        except Exception as e:
            print(f"Error al escribir en JSON: {e}")


    def json_to_csv(self, json_file, csv_file):
        try:
            # Abrir el archivo JSON
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            # Obtener los encabezados del primer elemento
            headers = data[0].keys()
            
            # Abrir el archivo CSV para escritura
            with open(csv_file, 'w', newline='') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=headers)
                csv_writer.writeheader()
                
                # Escribir cada fila del JSON en el CSV
                for row in data:  # Cambiar 'json' a 'data'
                    csv_writer.writerow(row)

            print(f'Conversión de {json_file} a {csv_file} completada.')
        
        except Exception as e:
            print(f"Error en la conversión: {e}")

    def close_connection(self):
        if self.connection and self.connection.open:
            self.connection.close()
            print("Conexión cerrada.")

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
        CREATE TABLE IF NOT EXISTS clientes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255),
            correo VARCHAR(255),
            fecha VARCHAR(255),
            membresía VARCHAR(255)
        )
    """
    #Creamos la tabla
    cursor.execute(crear_tabla)
    print("tabla creada con éxito")
    
    #Insertamos todos los datos en la base de datos
    cursor.execute("""
        INSERT INTO clientes (nombre, correo, fecha, membresía)
        VALUES ("Juan Pérez", "juan.perez@example.com", "2023-01-15", "Premium");
    """)

    cursor.execute("""
        INSERT INTO clientes (nombre, correo, fecha, membresía)
        VALUES ("Ana Garcia", "ana.garcia@example.com", "2022-06-20", "Estándar");
    """
    )

    cursor.execute("""
        INSERT INTO clientes (nombre, correo, fecha, membresía)
        VALUES ("Luis Fernández", "luis.fernandez@example.com", "2023-03-10", "Premium");
    """
    )

    cursor.execute("""
        INSERT INTO clientes (nombre, correo, fecha, membresía)
        VALUES ("María López", "maria.lopez@example.com", "2021-11-05", "Básica");
    """
    )

    cursor.execute("""
        INSERT INTO clientes (nombre, correo, fecha, membresía)
        VALUES ("Pedro Gómez", "pedro.gomez@example.com", "2022-09-01", "Estándar");
    """
    )

    #Confirmamos la inserción
    conexion.commit()

    #Pedimos la introducción de la membresía a filtrar
    membresia_input = input("Introduce la membresía a filtrar (por ejemplo, 'Premium'): ")

    #Buscamos los clientes con esa membresía
    cursor.execute("SELECT * FROM clientes where membresía=\"" + membresia_input + "\"")
    
    clientes_membresia = cursor.fetchall()
    
    #Imprimimos esos clientes
    for cliente in clientes_membresia:
        print(cliente)

    if conexion:  # Solo si la conexión fue exitosa
        db_to_files = MySQLToFile(conexion)  
        #Convertimos los clientes de la membresía elegida a formato json
        db_to_files.write_to_json(table_name="clientes", json_file="data.json", membresia=membresia_input)
        #Convertimos el json a csv
        db_to_files.json_to_csv(json_file="data.json", csv_file="data.csv")
        #Cerramos la conexión
        db_to_files.close_connection()

except MySQLError as e:
    print(f"Error de conexión a MySQL: {e}")

finally:
    if 'conexion' in locals() and conexion.open:
        conexion.close()
        print("Conexión cerrada")