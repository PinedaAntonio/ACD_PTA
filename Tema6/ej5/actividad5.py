import logging
import transaction
from ZODB import DB, FileStorage
from persistent import Persistent

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("databasemanager_object.log"),  # Logs guardados en un archivo
        logging.StreamHandler(),  # Logs también en consola
    ]
)

class Videojuego(Persistent):
    """Clase que representa una videojuego."""
    def __init__(self, nombre, genero, desarrollador, plataforma, fecha_lanzamiento):
        self.nombre = nombre
        self.genero = genero
        self.desarrollador = desarrollador
        self.plataforma = plataforma
        self.fecha_lanzamiento = fecha_lanzamiento

class DatabaseManagerObject:
    """Componente para gestionar bases de datos orientadas a objetos con ZODB."""
    def __init__(self, filepath="2dam.fs"):
        self.filepath = filepath
        self.db = None
        self.connection = None
        self.root = None
        self.transaccion_iniciada = False

    def conectar(self):
        """Conecta a la base de datos ZODB."""
        try:
            storage = FileStorage.FileStorage(self.filepath)
            self.db = DB(storage)
            self.connection = self.db.open()
            self.root = self.connection.root()
            if "videojuegos" not in self.root:
                self.root["videojuegos"] = {}
                transaction.commit()
            logging.info("Conexión establecida con ZODB.")
        except Exception as e:
            logging.error(f"Error al conectar a ZODB: {e}")

    def desconectar(self):
        """Cierra la conexión a la base de datos."""
        try:
            if self.connection:
                self.connection.close()
                self.db.close()
            logging.info("Conexión a ZODB cerrada.")
        except Exception as e:
            logging.error(f"Error al cerrar la conexión a ZODB: {e}")

    def iniciar_transaccion(self):
        """Inicia una transacción."""
        try:
            transaction.begin()
            self.transaccion_iniciada = True
            logging.info("Transacción iniciada.")
        except Exception as e:
            logging.error(f"Error al iniciar la transacción: {e}")

    def confirmar_transaccion(self):
        """Confirma la transacción."""
        if self.transaccion_iniciada:
            try:
                transaction.commit()
                self.transaccion_iniciada = False
                logging.info("Transacción confirmada.")
            except Exception as e:
                logging.error(f"Error al confirmar la transacción: {e}")

    def revertir_transaccion(self):
        """Revierte la transacción."""
        if self.transaccion_iniciada:
            try:
                transaction.abort()
                self.transaccion_iniciada = False
                logging.info("Transacción revertida.")
            except Exception as e:
                logging.error(f"Error al revertir la transacción: {e}")

    def crear_videojuego(self, id, nombre, genero, desarrollador, plataforma, fecha_lanzamiento):
        """Crea y almacena un nuevo videojuego."""
        try:
            if id in self.root["videojuegos"]:
                raise ValueError(f"Ya existe un videojuego con ID {id}.")
            self.root["videojuegos"][id] = Videojuego(nombre, genero, desarrollador, plataforma, fecha_lanzamiento)
            logging.info(f"Videojuego con ID {id} creado exitosamente.")
        except Exception as e:
            logging.error(f"Error al crear la videojuego con ID {id}: {e}")

    def leer_videojuego(self):
        """Lee y muestra todos los videojuegos almacenadas."""
        try:
            videojuegos = self.root["videojuegos"]
            for id, videojuego in videojuegos.items():
                logging.info(
                    f"ID: {id}, Nombre: {videojuego.nombre}, Género: {videojuego.genero}, "
                    f"Desarrollador: {videojuego.desarrollador}, Plataforma: {videojuego.plataforma}, Fecha Lanzamiento: {videojuego.fecha_lanzamiento}"
                )
            return videojuegos
        except Exception as e:
            logging.error(f"Error al leer los videojuegos: {e}")

    def actualizar_videojuego(self, id, nombre, genero, desarrollador, plataforma, fecha_lanzamiento):
        """Actualiza los atributos de una videojuego."""
        try:
            videojuego = self.root["videojuegos"].get(id)
            if not videojuego:
                raise ValueError(f"No existe una videojuego con ID {id}.")
            videojuego.nombre = nombre
            videojuego.genero = genero
            videojuego.desarrollador = desarrollador
            videojuego.plataforma = plataforma
            videojuego.fecha_lanzamiento = fecha_lanzamiento
            logging.info(f"Videojuego con ID {id} actualizada exitosamente.")
        except Exception as e:
            logging.error(f"Error al actualizar la videojuego con ID {id}: {e}")

    def eliminar_videojuego(self, id):
        """Elimina un videojuego por su ID."""
        try:
            if id not in self.root["videojuegos"]:
                raise ValueError(f"No existe una videojuego con ID {id}.")
            del self.root["videojuegos"][id]
            logging.info(f"Videojuego con ID {id} eliminada exitosamente.")
        except Exception as e:
            logging.error(f"Error al eliminar la videojuego con ID {id}: {e}")

if __name__ == "__main__":
    manager = DatabaseManagerObject()
    manager.conectar()
    try:
        # Crear videojuegos con transacción
        manager.iniciar_transaccion()
        manager.crear_videojuego(1, "The Legend of Zelda: Tears of the Kingdom", "aventura", "nintendo", "Switch", "12-05-2023")
        manager.crear_videojuego(2, "Minecraft", "sandbox", "Mojang", "PC", "18-11-2011")
        manager.crear_videojuego(3, "FIFA 24", "deportes", "EA Sports", "Ps5", "30-09-2023")
        manager.confirmar_transaccion()

        manager.iniciar_transaccion()
        manager.crear_videojuego(2, "Super Smash Bros. Ultimate", "platform fighter", "nintendo", "Switch", "07-12-2018")
        manager.confirmar_transaccion()

        # Leer videojuegos
        manager.leer_videojuego()

        # Actualizar una videojuego con transacción
        manager.iniciar_transaccion()
        manager.actualizar_videojuego(1, "The Legend of Zelda: Breath of the Wild", "mundo abierto", "nintendo", "WiiU", "03-03-2017")
        manager.confirmar_transaccion()

        # Eliminar una videojuego con transacción
        manager.iniciar_transaccion()
        manager.eliminar_videojuego(4)
        manager.confirmar_transaccion()

        # Leer videojuegos nuevamente
        manager.leer_videojuego()
    except Exception as e:
        logging.error(f"Error general: {e}")
        manager.revertir_transaccion()
    finally:
        manager.desconectar()
