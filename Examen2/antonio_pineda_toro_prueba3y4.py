from peewee import MySQLDatabase, Model, CharField, IntegerField, PrimaryKeyField
import ZODB, ZODB.FileStorage, transaction
from persistent import Persistent

# Configurar la base de datos
db = MySQLDatabase(
    "1dam",  # Nombre de la base de datos
    user="usuario",  # Usuario de MySQL
    password="usuario",  # Contraseña de MySQL
    host="localhost",  # Host
    port=3306,  # Puerto por defecto de MySQLl
)
# Conectar a la base de datos
db.connect()
print("Conexión exitosa a la base de datos.")

class Libros(Model):
    id = PrimaryKeyField()
    titulo = CharField(100)
    autor = CharField(100)
    anio_publicacion = IntegerField()
    genero = CharField(50)
    class Meta:
        database = db
        table_name = "Libros"

class Prestamo(Persistent):
    def __init__(self, libro_id, nombre_usuario, fecha_prestamo, fecha_devolucion):
        self.libro_id = libro_id
        self.nombre_usuario = nombre_usuario
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion

# Establecer conexión a la base de datos ZODB
storage = ZODB.FileStorage.FileStorage('1dam.fs')
db2 = ZODB.DB(storage)
connection = db2.open()
root = connection.root()

if 'prestamos' not in root:
    root['prestamos'] = {}

db.create_tables([Libros])
print("Tabla creada o ya existente")


Libros.create(titulo = "Cien Años de Soledad", autor = "Gabriel García Márquez", anio_publicacion = "1967", genero = "Novela")
Libros.create(titulo = "Don Quijote de la Mancha", autor = "Miguel de Cervantes", anio_publicacion = "1605,", genero = "Novela")
Libros.create(titulo = "El Principito", autor = "Antoine de Saint-Exupéry", anio_publicacion = "1943", genero = "Infantil")
Libros.create(titulo = "Crónica de una muerte anunciada", autor = "Gabriel García Márquez", anio_publicacion = "1981", genero = "Novela")
Libros.create(titulo = "1984", autor = "George Orwell", anio_publicacion = "1967", genero = "Distopía")
print("Libros insertados")

try:
    root["prestamos"]["1"] = Prestamo("1", "Juan Perez", "2023-10-01", "2023-11-01")
    root["prestamos"]["2"] = Prestamo("2", "Ana Lopez", "2023-09-15", "2023-10-15")
    root["prestamos"]["4"] = Prestamo("4", "Maria Gomez", "2023-09-20", "2023-10-20")
    print("Préstamos insertados con éxito")
    transaction.commit()
except Exception as e:
    transaction.abort()
    print("Eror al insertar préstamos: " + e)

def buscar_prestamos_por_genero(genero):
    libros_novela = Libros.select().where(Libros.genero == genero)
    if libros_novela.exists():
        print(f"Prestamos del género: '{genero}'")
        for libro in libros_novela:
            if 'prestamos' in root:
                for titulo, prestamo in root["prestamos"].items():
                    v1 = int(prestamo.libro_id)
                    v2 = int(libro.id)
                    #La comparativa no funciona a no ser que hagamos un casting del int
                    if v1 == v2:
                        print(
                            f"Libro: {libro.titulo}, Género: {libro.genero}, Fecha Préstamo: {prestamo.fecha_prestamo}, Fecha Devolución: {prestamo.fecha_devolucion}"
                        )
            else:
                print("No está disponible 'préstamos' en ZODB")
    else:
        print(f"El género '{genero}' no existe en la base de datos")
    print("")

buscar_prestamos_por_genero("Novela")