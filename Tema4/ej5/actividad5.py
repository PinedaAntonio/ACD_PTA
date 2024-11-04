import ZODB, ZODB.FileStorage, transaction
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

tienda_seleccionada = "Game"

def mostrar_videojuegos():
    try:
        print("Videojuegos almacenados en la base de datos:")
        if 'videojuegos' in root:
            for nombre, videojuego in root['videojuegos'].items():
                if hasattr(videojuego, "id_tienda") and videojuego.id_tienda == tienda_seleccionada:
                    print(
                        f"Nombre: {videojuego.nombre}, Genero: {videojuego.genero}, Desarrollador: {videojuego.desarrollador}, "
                        f"Plataforma: {videojuego.plataforma}, Fecha de lanzamiento: {videojuego.fecha_lanzamiento}, Tienda: {videojuego.id_tienda}"
                    )
        else:
            print("No se encontraron videojuegos en la base de datos.")
    except Exception as e:
        print(f"Error al recuperar videojuegos: {e}")


#Llamar a la función para mostrar videojuegos
mostrar_videojuegos()
# Cerrar la conexión a la base de datos ZODB
connection.close()
db.close()