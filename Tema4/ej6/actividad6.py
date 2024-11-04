import ZODB, ZODB.FileStorage, transaction, copy
from persistent import Persistent
# Definir la clase Videojuego
class Videojuego(Persistent):
    def __init__(self, nombre, genero, desarrollador, plataforma, fecha_lanzamiento, id_tienda):
        self.nombre = nombre
        self.genero = genero
        self.desarrollador = desarrollador
        self.plataforma = plataforma
        self.fecha_lanzamiento = fecha_lanzamiento
        self.id_tienda = id_tienda

class Tienda(Persistent):
    def __init__(self, nombre_tienda, direccion, telefono):
        self.nombre_tienda = nombre_tienda
        self.direccion = direccion
        self.telefono = telefono

# Establecer conexión a la base de datos ZODB
storage = ZODB.FileStorage.FileStorage('1dam.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

if 'videojuegos' not in root:
    root['videojuegos'] = {}
if 'tiendas' not in root:
    root['tiendas'] = {}

root['tiendas']['Game'] = Tienda("Game", "Calle Original n1", "111-222-333")
root['tiendas']['Cex'] = Tienda("Cex", "Avenida Segunda Mano", "222-444-666")

root['videojuegos']['Fortnite'] = Videojuego("Fortnite", "Battle Royale", "Epic Games", "ps4", "12-08-2018", "Game")
root['videojuegos']['Street Fighter 6'] = Videojuego("Street Fighter 6", "Fighting", "Capcom", "xbox one", "21-04-2024", "Game")
root['videojuegos']['PUBG'] = Videojuego("PUBG", "Battle Royale", "Krafton", "pc", "23-03-2017", "Cex")

transaction.commit()

videojuego_original = root['videojuegos']['Fortnite']
videojuego_copia = copy.deepcopy(videojuego_original)
#Tras hacer la copia, cambiamos la plataforma de ps4 a ps5
videojuego_copia.plataforma = "ps5"
transaction.commit()

tienda_seleccionada = "Game"

def mostrar_original_copia():
    try:
        print("Original:")
        print(f"Nombre: {videojuego_original.nombre}, Genero: {videojuego_original.genero}, Desarrollador: {videojuego_original.desarrollador}, "
                        f"Plataforma: {videojuego_original.plataforma}, Fecha de lanzamiento: {videojuego_original.fecha_lanzamiento}, Tienda: {videojuego_original.id_tienda}")
        print("Copia:")
        print(f"Nombre: {videojuego_copia.nombre}, Genero: {videojuego_copia.genero}, Desarrollador: {videojuego_copia.desarrollador}, "
                        f"Plataforma: {videojuego_copia.plataforma}, Fecha de lanzamiento: {videojuego_copia.fecha_lanzamiento}, Tienda: {videojuego_copia.id_tienda}")
    except Exception as e:
        print(f"Error al recuperar videojuegos: {e}")

#Llamar a la función para mostrar videojuegos
mostrar_original_copia()

# Cerrar la conexión a la base de datos ZODB
connection.close()
db.close()