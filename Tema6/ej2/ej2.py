import logging
import mysql.connector
from mysql.connector import Error
# Configuración de logging
logging.basicConfig(
 level=logging.INFO,
 format="%(asctime)s - %(levelname)s - %(message)s",
 handlers=[
 logging.FileHandler("databasemanager.log"), # Logs guardados en un archivo
 logging.StreamHandler(), # Logs también en consola
 ]
)
class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def conectar(self):
        """Conectar a la base de datos MySQL"""
        try:
            self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
            )
            if self.connection.is_connected():
                logging.info("Conexión exitosa a la base de datos.")
        except Error as e:
            logging.error(f"Error al conectar a la base de datos: {e}")

    def desconectar(self):
        """Cerrar la conexión a la base de datos"""
        if self.connection.is_connected():
            self.connection.close()
            logging.info("Conexión cerrada.")

    def crear_videojuego(self, nombre, genero, desarrollador, plataforma, fecha_lanzamiento, tienda):
        """Insertar un nuevo videojuego en la base de datos"""
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO videojuegos (nombre, genero, desarrollador, plataforma, fecha_lanzamiento, id_tienda)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (nombre, genero, desarrollador, plataforma, fecha_lanzamiento, tienda))
            logging.info(f"Videojuego '{nombre}' insertada exitosamente.")
        except Error as e:
            logging.error(f"Error al insertar el videojuego '{nombre}': {e}")
    
    def leer_videojuegos(self):
        """Leer todos los videojuegos de la base de datos"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM videojuegos")
            videojuegos = cursor.fetchall()
            logging.info("Videojuegos recuperadas:")
            for videojuego in videojuegos:
                logging.info(videojuego)
            return videojuegos
        except Error as e:
            logging.error(f"Error al leer las videojuegos: {e}")
            return None
        
    def actualizar_videojuego(self, nombre, genero, desarrollador, plataforma, fecha_lanzamiento, tienda, id):
        """Actualizar un videojuego en la base de datos"""
        try:
            cursor = self.connection.cursor()
            query = """
                UPDATE videojuegos
                SET nombre = %s, genero = %s, desarrollador = %s, plataforma = %s, fecha_lanzamiento = %s, id_tienda = %s
                WHERE id = %s
            """
            cursor.execute(query, (nombre, genero, desarrollador, plataforma, fecha_lanzamiento, tienda, id))
            self.connection.commit()
            logging.info(f"Videojuego con ID {id} actualizado exitosamente.")
        except Error as e:
            logging.error(f"Error al actualizar el videojuego con ID {id}: {e}")


    def eliminar_videojuego(self, id):
        """Eliminar un videojuego de la base de datos"""
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM videojuegos WHERE id = %s"
            cursor.execute(query, (id,))
            logging.info(f"videojuego con ID {id} eliminada exitosamente.")
        except Error as e:
            logging.error(f"Error al eliminar el videojuego con ID {id}: {e}")

    def iniciar_transaccion(self):
        """Iniciar una transacción"""
        try:
            if self.connection.is_connected():
                self.connection.start_transaction()
                logging.info("Transacción iniciada.")
        except Error as e:
            logging.error(f"Error al iniciar la transacción: {e}")

    def confirmar_transaccion(self):
        """Confirmar (commit) una transacción"""
        try:
            if self.connection.is_connected():
                self.connection.commit()
                logging.info("Transacción confirmada.")
        except Error as e:
            logging.error(f"Error al confirmar la transacción: {e}")

    def revertir_transaccion(self):
        """Revertir (rollback) una transacción"""
        try:
            if self.connection.is_connected():
                self.connection.rollback()
                logging.info("Transacción revertida.")
        except Error as e:
            logging.error(f"Error al revertir la transacción: {e}")

# Ejemplo de uso del componente DatabaseManager
if __name__ == "__main__":
    db_manager = DatabaseManager("localhost", "usuario", "usuario", "mi_base_datos")
    db_manager.conectar()

    # Insertar una nueva videojuego
    db_manager.crear_videojuego("Overwatch 2", "hero shooter", "blizzard", "pc", "04-10-2022", "1")
    db_manager.confirmar_transaccion()
    # Leer todos los videojuegos
    db_manager.leer_videojuegos()

    # Actualizar un videojuego
    db_manager.actualizar_videojuego("Overwatch 2", "hero shooter", "blizzard", "pc", "04-10-2022", "3", "14") 
    #el id es 14 porque ya había insertado varios objetos anteriormente
    db_manager.confirmar_transaccion()
    # Eliminar un videojuego
    db_manager.eliminar_videojuego(14)
    db_manager.confirmar_transaccion()
    # Gestionar transacciones
    db_manager.iniciar_transaccion()
    db_manager.crear_videojuego("Elden Ring", "rpg", "from software", "ps5", "12-03-2023", "2")
    db_manager.revertir_transaccion() 
    db_manager.desconectar()