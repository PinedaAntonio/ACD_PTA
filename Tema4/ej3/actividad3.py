import ZODB, ZODB.FileStorage, transaction
from persistent import Persistent
# Definir la clase Videojuego
class Videojuego(Persistent):
    def __init__(self, nombre, genero, desarrollador, plataforma, fecha_lanzamiento):
        self.nombre = nombre
        self.genero = genero
        self.desarrollador = desarrollador
        self.plataforma = plataforma
        self.fecha_lanzamiento = fecha_lanzamiento
# Establecer conexión a la base de datos ZODB
storage = ZODB.FileStorage.FileStorage('1dam.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()
# Recuperar y modificar un objeto
videojuego = root.get('Overwatch 2') # Recuperar el videojuego almacenada con la clave 'Overwatch 2'
if videojuego:
    print("Antes de la modificación:")
    print(f"Nombre: {videojuego.nombre}, Plataforma: {videojuego.plataforma}")
    # Modificar el atributo 'plataforma'
    videojuego.plataforma = 'ps4'
    transaction.commit() # Confirmar los cambios en la base de datos
    print("Después de la modificación:")
    print(f"Nombre: {videojuego.nombre}, Plataforma: {videojuego.plataforma}")
else:
    print("El videojuego no se encontró en la base de datos.")
# Cerrar la conexión
connection.close()
db.close()