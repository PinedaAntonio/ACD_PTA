from peewee import MySQLDatabase, Model, CharField, IntegerField, IntegrityError

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

if tabla_existe(videojuegos._meta.table_name):
    print(f"La tabla '{videojuegos._meta.table_name}' existe.")
    db.drop_tables([videojuegos], cascade=True)
    print(f"Tabla '{videojuegos._meta.table_name}' eliminada con éxito.")
else:
    print(f"La tabla '{videojuegos._meta.table_name}' no existe.")

db.create_tables([videojuegos])
print("Tabla 'videojuegos' creada o ya existente.")

try:
# Iniciar una transacción utilizando db.atomic()
    with db.atomic():
    # Insertar varios videojuegos dentro de la transacción
        videojuegos.create(nombre='Overwatch 2',plataforma='pc',genero='hero shooter',desarrollador='blizzard', fecha_lanzamiento='04-10-2022', id_tienda='3')
        videojuegos.create(nombre='Counter Strike 2',plataforma='pc',genero='tactical shooter',desarrollador='valve', fecha_lanzamiento='27-10-2023', id_tienda='1')
        videojuegos.create(nombre='Dragon Ball: Sparking Zero',plataforma='ps5',genero='arena fighter',desarrollador='spike chunsoft', fecha_lanzamiento='07-10-2024', id_tienda='2')
        videojuegos.create(nombre='Super Smash Bros Ultimate',plataforma='switch',genero='platform fighter',desarrollador='nintendo', fecha_lanzamiento='07-12-2018', id_tienda='3')
        videojuegos.create(nombre='Elden Ring',plataforma='ps5',genero='rpg',desarrollador='from software', fecha_lanzamiento='25-02-2022', id_tienda='1')
        print("Videojuegos insertados correctamente.")
except IntegrityError as e:
    print(f"Error al insertar videojuegos: {e}")


print("videojuegos insertados en la base de datos")

db.close()
print("Conexión con la base de datos cerrada")