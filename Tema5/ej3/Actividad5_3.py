from pymongo import MongoClient, errors
# Datos de conexión
usuario = "usuario"
clave = "usuario"
base_datos = "2dam"
host = "localhost"
puerto = 27017
try:
    # Intentar conectarse al servidor MongoDB
    client = MongoClient(f"mongodb://{usuario}:{clave}@{host}:{puerto}/{base_datos}", serverSelectionTimeoutMS=5000)

    # Seleccionar la base de datos
    db = client[base_datos]
    # Seleccionar la colección
    coleccion = db.Videojuegos

    # Añadir tres documentos a la colección
    print("Añadiendo tres videojuegos a la colección...")
    videojuegos = [
        { "nombre": "The Legend of Zelda: Tears of the Kingdom", "genero": "aventura", "desarrollador": "nintendo", "plataforma": "Switch", "fecha_lanzamiento": "12-05-2023" },
        { "nombre": "FIFA 24", "genero": "deportes", "desarrollador": "EA Sports", "plataforma": "ps5", "fecha_lanzamiento": "30-09-2023" },
        { "nombre": "Minecraft", "genero": "sandbox", "desarrollador": "Mojang", "plataforma": "PC", "fecha_lanzamiento": "18-11-2011" }
    ]
    coleccion.insert_many(videojuegos)
    print("Tres videojuegos añadidos con éxito.")

    # Actualizar un campo de un documento
    print("Actualizar el género de 'FIFA 24' a 'simulación de deportes'")
    coleccion.update_one(
        {"nombre": "FIFA 24"}, 
        {"$set": {"genero": "simulación de deportes"}} 
    )
    print("Género de 'FIFA 23' actualizado correctamente.")

    # Eliminar un documento 
    print("Eliminando el videojuego 'Minecraft' de la colección")
    coleccion.delete_one({"nombre": "Minecraft"})
    print("El videojuego 'Minecraft' ha sido eliminado.")

    # Mostrar los documentos restantes
    print("Documentos restantes en la colección:")
    documentos = coleccion.find()
    for documento in documentos:
        print(documento)

except errors.ServerSelectionTimeoutError as err:
    # Este error ocurre si el servidor no está disponible o no se puede conectar
    print(f"No se pudo conectar a MongoDB: {err}")
except errors.OperationFailure as err:
    # Este error ocurre si las credenciales son incorrectas o no se tienen los permisos necesarios
    print(f"Fallo en la autenticación o permisos insuficientes: {err}")
except Exception as err:
    # Manejar cualquier otro error inesperado
    print(f"Ocurrió un error inesperado: {err}")
finally:
    # Cerrar la conexión si se estableció correctamente
    if 'client' in locals():
        client.close()
        print("Conexión cerrada.")