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
# Función para gestionar la inserción de varias videojuegos con transacción
def agregar_videojuegos():
    try:
        print("Iniciando la transacción para agregar videojuegos...")
        # Verificar y crear 'videojuegos' en root si no existe
        if 'videojuegos' not in root:
            root['videojuegos'] = {} # Inicializar una colección de videojuegos si no existe
            transaction.commit() # Confirmar la creación en la base de datos
            # Crear y añadir nuevas videojuegos
            videojuego1 = Videojuego("Overwatch 2", "hero shooter", "blizzard", "pc", "04-10-2022")
            videojuego2 = Videojuego("Elden Ring", "rpg", "from software", "ps5", "25-02-2022")
            videojuego3 = Videojuego("Super Smash Bros Ultimate", "paltform fighter", "nintendo", "switch", "07-12-2018")
            # Añadir videojuegos a la colección en la raíz de ZODB
            root['videojuegos']["Overwatch 2"] = videojuego1
            root['videojuegos']["Elden Ring"] = videojuego2
            root['videojuegos']["Super Smash Bros Ultimate"] = videojuego3
            # Confirmar la transacción
            transaction.commit()
            print("Transacción completada: Viodeojuegos añadidas correctamente.")
    except Exception as e:
        # Si ocurre un error, revertimos la transacción
        transaction.abort()
        print(f"Error durante la transacción: {e}. Transacción revertida.")

def mostrar_videojuegos():
    try:
        print("Videojuegos almacenados en la base de datos:")
        if 'videojuegos' in root:
            for nombre, videojuego in root['videojuegos'].items():
                print(
                    f"Nombre: {videojuego.nombre}, Genero: {videojuego.genero}, Desarrollador: {videojuego.desarrollador}, "
                    f"Plataforma: {videojuego.plataforma}, Fecha de lanzamiento: {videojuego.fecha_lanzamiento}"
                )
        else:
            print("No se encontraron videojuegos en la base de datos.")
    except Exception as e:
        print(f"Error al recuperar videojuegos: {e}")

# Llamar a la función para añadir videojuegos
agregar_videojuegos()
#Llamar a la función para mostrar videojuegos
mostrar_videojuegos()
# Cerrar la conexión a la base de datos ZODB
connection.close()
db.close()