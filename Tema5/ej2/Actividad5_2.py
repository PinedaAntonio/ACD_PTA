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
    
    # Realizar una consulta para obtener los videojuegos del género "fps"
    print("Consultando videojuegos del género fps:")
    resultados = db.Videojuegos.find({"genero": "fps"})
    for juego in resultados:
        print(juego)

    # Realizar una proyección para mostrar solo el nombre y la plataforma de los videojuegos del género "fps"
    print("Mostrar nombre y plataforma de los videojuegos del género fps:")
    resultados = db.Videojuegos.find(
        {"genero": "fps"}, {"nombre": 1, "plataforma": 1, "_id": 0}
    )
    for juego in resultados:
        print(juego)

    # Limitar los resultados a 2 documentos y ordenarlos alfabéticamente por nombre
    print("\nLimitar a 2 resultados y ordenar alfabéticamente por nombre:")
    resultados = db.Videojuegos.find(
        {"genero": "fps"}, {"nombre": 1, "plataforma": 1, "_id": 0}
    ).limit(2).sort("nombre", 1)  # 1 es para orden ascendente
    for juego in resultados:
        print(juego)

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