import ZODB, ZODB.FileStorage, transaction
from persistent import Persistent


# Definir clase Herramienta
class Videojuego(Persistent):
    def __init__(self, nombre, genero, desarrollador, plataforma, fecha_lanzamiento):
        self.nombre = nombre
        self.genero = genero
        self.desarrollador = desarrollador
        self.plataforma = plataforma
        self.fecha_lanzamiento = fecha_lanzamiento


# Establecer conexión
storage = ZODB.FileStorage.FileStorage("1dam.fs")
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

# Almacenar videojuegos
root["Overwatch 2"] = Videojuego(
    "Overwatch 2", "hero shooter", "blizzard", "pc", "04-10-2022 "
)
root["Elden Ring"] = Videojuego(
    "Elden Ring", "rpg", "from software", "ps5", "25-02-2022 "
)
root["Super Smash Bros. Ultimate"] = Videojuego(
    "Super Smash Bros. Ultimate", "paltform fighter", "nintendo", "switch", "07-12-2018 "
)
transaction.commit()

# Filtrar objetos que tienen el atributo "genero", para comprobar que todos lo tienen
print("Mostrando todos los videojuegos que tienen el atributo 'género': ")
for clave, objeto in root.items():
    if hasattr(objeto, "genero"):
        print(
            f"Nombre: {objeto.nombre}, Genero: {objeto.genero}, Desarrollador: {objeto.desarrollador}, "
            f"Plataforma: {objeto.plataforma}, Fecha de lanzamiento: {objeto.fecha_lanzamiento}"
        )
    else:
        print(f"El objeto '{clave}' no tiene el atributo 'genero'")

# Filtrar videojuegos por plataforma
print("Mostrando los videojuegos de la plataforma pc: ")
plataforma_deseada = "pc"
for clave, videojuego in root.items():
    if hasattr(videojuego, "plataforma") and videojuego.plataforma == plataforma_deseada:
        print(
            f"Nombre: {videojuego.nombre}, Genero: {videojuego.genero}, Desarrollador: {videojuego.desarrollador }, Plataforma: {videojuego.plataforma}, Fecha de lanzamiento: {videojuego.fecha_lanzamiento}"
        )

# Cerrar la conexión
connection.close()
db.close()
