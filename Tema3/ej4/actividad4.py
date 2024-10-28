from peewee import MySQLDatabase, Model, CharField, IntegerField, IntegrityError

# Configurar la base de datos
db = MySQLDatabase(
    "mi_base_datos",  # Nombre de la base de datos
    user="usuario",  # Usuario de MySQL
    password="usuario",  # Contraseña de MySQL
    host="localhost",  # Host
    port=3306,  # Puerto por defecto de MySQLl
)

print("Tarea 1...")
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


if tabla_existe("videojuegos"):
    print("La base de datos existe")


# Función para mostrar todos los objetos
def videojuegos_all(nombre_tabla):
    videojuegos_pc = videojuegos.select().where(videojuegos.id_tienda > 0)
    consulta = "SELECT * FROM information_schema.tables WHERE table_schema = %s AND table_name = %s"
    cursor = db.execute_sql(consulta, ("mi_base_datos", nombre_tabla))
    resultado = cursor.fetchall()
    print("Todos los resultados:")
    for videojuego in videojuegos_pc:
        print(
            f"Nombre: {videojuego.nombre}, Género: {videojuego.genero}, Plataforma: {videojuego.plataforma}, Desarrollador: {videojuego.desarrollador}, Fecha de lanzamiento: {videojuego.fecha_lanzamiento}, id_tienda: {videojuego.id_tienda}"
        )
    print("")

videojuegos_all("videojuegos")

try:
# Iniciar una transacción utilizando db.atomic()
    with db.atomic():
    # Insertar varios videojuegos dentro de la transacción
        # Buscar todos los juegos de la plataforma 'pc'
        videojuegos_pc = videojuegos.select().where(videojuegos.plataforma == "pc")
        print("juegos de la plataforma pc")
        for videojuego in videojuegos_pc:
            print(
                f"Nombre: {videojuego.nombre}, Género: {videojuego.genero}"
            )
        print("")
except IntegrityError as e:
    print(f"Error al insertar videojuegos: {e}")

try:
# Iniciar una transacción utilizando db.atomic()
    with db.atomic():
        print("Tarea 2...")
        # Buscar el primer juego de la plataforma 'pc' y que tengan id_tienda '1'. Al usar '&', podemos concatenar dos condiciones para el where.
        videojuego_a_eliminar = videojuegos.select().where(
            (videojuegos.plataforma == "pc") & (videojuegos.id_tienda == 1)
        ).first()  # Selecciona el primer registro que coincida con .first

        if videojuego_a_eliminar:
            videojuego_a_eliminar.delete_instance()  # Elimina solo este registro
            print(f"Se eliminó el videojuego: {videojuego_a_eliminar.nombre}")
        else:
            print("No se encontraron registros para eliminar.")
        videojuegos_all("videojuegos")
except IntegrityError as e:
    print(f"Error al insertar videojuegos: {e}")

try:
# Iniciar una transacción utilizando db.atomic()
    with db.atomic():
        print("Tarea 3...")
        # Buscar todos los juegos de la plataforma 'ps5'
        videojuegos_ps5 = videojuegos.select().where(videojuegos.plataforma == "ps5")

        # Mostrar los registros que serán eliminados
        if videojuegos_ps5.exists():
            print("Registros que serán eliminados:")
            for videojuego in videojuegos_ps5:
                print(
                    f"Nombre: {videojuego.nombre}"
                )

            # Ejecutar la eliminación de los registros
            eliminar_videojuegos_ps5 = videojuegos.delete().where(videojuegos.plataforma == "ps5")
            eliminados = eliminar_videojuegos_ps5.execute()
            print(f"Se eliminaron {eliminados} registros con plataforma 'ps5'.")
        else:
            print("No se encontraron registros con la plataforma 'ps5' para eliminar.")
        videojuegos_all("videojuegos")
except IntegrityError as e:
    print(f"Error al insertar videojuegos: {e}")

db.close()
print("Conexión con la base de datos cerrada")
