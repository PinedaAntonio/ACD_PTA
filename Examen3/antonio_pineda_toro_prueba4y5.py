import logging
import pymongo
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Configuración de logging​
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            "databasemanager_documental.log"
        ),  # Logs guardados en un archivo​
        logging.StreamHandler(),  # Logs también en consola​
    ],
)


class ProductoManager:
    def __init__(self, url, database_name, collection_name):
        """Inicializa el componente ProductoManager."""
        self.url = url
        self.database_name = database_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None

    def conectar(self):
        """Conectar a la base de datos MongoDB"""
        try:
            self.client = MongoClient(self.url)
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            logging.info(
                f"Conectado a MongoDB: {self.database_name}.{self.collection_name}"
            )
        except PyMongoError as e:
            logging.error(f"Error al conectar a MongoDB: {e}")

    def desconectar(self):
        """Cerrar la conexión a MongoDB"""
        if self.client:
            self.client.close()
            logging.info("Conexión a MongoDB cerrada.")

    def insertar_producto(self, producto):
        """Insertar un nuevo producto en la colección"""
        try:
            result = self.collection.insert_one(producto)
            logging.info(f"producto insertado con ID: {result.inserted_id}")
            return result.inserted_id
        except PyMongoError as e:
            logging.error(f"Error al insertar el producto: {e}")

    def consultar_proyeccion_ordenada(self, proyeccion={}, orden={}, filtro={}):
        """Leer productos de la colección según un filtro"""
        try:
            productos = list(self.collection.find(filtro, proyeccion).sort(orden))
            logging.info(f"productos recuperados: {len(productos)}")
            for prod in productos:
                logging.info(prod)
            return productos
        except PyMongoError as e:
            logging.error(f"Error al leer los productos: {e}")
            return []

    def mostrar_todos_productos(self):
        """Leer productos de la colección"""
        try:
            productos = list(self.collection.find())
            logging.info(f"Productos recuperados: {len(productos)}")
            for prod in productos:
                logging.info(prod)
            return productos
        except PyMongoError as e:
            logging.error(f"Error al leer los productos: {e}")
            return []

    def actualizar_producto(self, filtro, actualizacion):
        """Actualizar un producto en la colección"""
        try:
            result = self.collection.update_one(filtro, {"$set": actualizacion})
            if result.modified_count > 0:
                logging.info(f"producto actualizado: {filtro}")
            else:
                logging.warning(f"No se encontró producto para actualizar: {filtro}")
        except PyMongoError as e:
            logging.error(f"Error al actualizar el producto: {e}")

    def eliminar_productos(self, filtro):
        """Eliminar productos de la colección"""
        try:
            result = self.collection.delete_many(filtro)
            if result.deleted_count > 0:
                logging.info(f"productos eliminados: {filtro}")
            else:
                logging.warning(f"No se encontró producto para eliminar: {filtro}")
        except PyMongoError as e:
            logging.error(f"Error al eliminar el producto: {e}")


if __name__ == "__main__":
    # Configurar el componente​
    db_manager = ProductoManager(
        url="mongodb://localhost:27017",
        database_name="1dam",
        collection_name="productos",
    )

db_manager.conectar()

try:
    db_manager.insertar_producto(
        {
            "nombre": "Drone Phantom X",
            "categoria": "Drones",
            "precio": 1200.50,
            "stock": 8,
        }
    )
    db_manager.insertar_producto(
        {
            "nombre": "Auriculares Sonic Boom",
            "categoria": "Auriculares",
            "precio": 299.99,
            "stock": 15,
        }
    )
    db_manager.insertar_producto(
        {
            "nombre": "Cámara Action Pro",
            "categoria": "Cámaras",
            "precio": 499.99,
            "stock": 10,
        }
    )

    db_manager.insertar_producto(
        {
            "nombre": "Asistente SmartBuddy",
            "categoria": "Asistentes Inteligentes",
            "precio": 199.99,
            "stock": 20,
        }
    )

    db_manager.insertar_producto(
        {
            "nombre": "Cargador Solar Ultra",
            "categoria": "Accesorios",
            "precio": 49.99,
            "stock": 3,
        }
    )

    db_manager.mostrar_todos_productos()

    # db_manager.consultar_proyeccion_ordenada(
    #    {"nombre": 1, "categoria": 0, "precio": 1, "stock": 1, "_id": 0},
    #    ("precio", pymongo.DESCENDING),
    # )

    db_manager.actualizar_producto({"nombre": "Drone Phantom X"}, {"precio": 1300})

    db_manager.actualizar_producto({"nombre": "Cámara Action Pro"}, {"precio": 1300})

    db_manager.mostrar_todos_productos()

    db_manager.eliminar_productos({int("stock") < 5})

    db_manager.mostrar_todos_productos()


except Exception as e:
    logging.error(f"Error general: {e}")

finally:
    db_manager.desconectar()
