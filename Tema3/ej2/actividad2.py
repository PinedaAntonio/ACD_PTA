from peewee import MySQLDatabase, Model, CharField, IntegerField

# Configurar la base de datos
db = MySQLDatabase(
    "mi_base_datos",  # Nombre de la base de datos
    user="usuario",  # Usuario de MySQL
    password="usuario",  # Contraseña de MySQL
    host="localhost",  # Host
    port=3306,  # Puerto por defecto de MySQLl
)
# Conectar a la base de datos
db.connect()
print("Conexión exitosa a la base de datos.")


class videojuegos(Model):
    nombre = CharField()
    plataforma = CharField()
    genero = CharField()
    desarrollador = CharField()
    plataforma = CharField()
    fecha_lanzamiento = CharField()
    id_tienda = IntegerField()

    class Meta:
        database = db
        table_name = "videojuegos"


def tabla_existe(nombre_tabla):
    consulta = "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s AND table_name = %s"
    cursor = db.execute_sql(consulta, ("mi_base_datos", nombre_tabla))
    resultado = cursor.fetchone()
    return resultado[0] > 0


if tabla_existe:
    print("La base de datos existe")

# Buscar todas las herramientas de tipo 'Manual'
videojuegos_pc = videojuegos.select().where(videojuegos.plataforma == "pc")
for videojuego in videojuegos_pc:
    print(
        f"Nombre: {videojuego.nombre}, Plataforma: {videojuego.plataforma}, Tipo: {videojuego.tipo}"
    )

db.close()
print("Conexión con la base de datos cerrada")
