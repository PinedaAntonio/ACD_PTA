import logging
from peewee import Model, CharField, ForeignKeyField, MySQLDatabase
# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
    logging.FileHandler("databasemanager_orm.log"),
    logging.StreamHandler()
    ]
)

# Configuración de la base de datos MySQL
db = MySQLDatabase(
    "mi_base_datos", # Nombre de la base de datos
    user="usuario", # Usuario de MySQL
    password="usuario", # Contraseña de MySQL
    host="localhost", # Host
    port=3306 # Puerto por defecto de MySQL
)

# Modelos de la base de datos
class Proveedor(Model):
    nombre = CharField()
    direccion = CharField()
    class Meta:
        database = db

class Herramienta(Model):
    nombre = CharField()
    tipo = CharField()
    marca = CharField()
    uso = CharField()
    material = CharField()
    proveedor = ForeignKeyField(Proveedor, backref='herramientas')
    class Meta:
        database = db

# Componente DatabaseManagerORM
class DatabaseManagerORM:
    def __init__(self):
        self.db = db

    def conectar(self):
        """Conecta la base de datos y crea las tablas."""
        self.db.connect()
        self.db.create_tables([Proveedor, Herramienta])
        logging.info("Conexión establecida y tablas creadas.")
    
    def desconectar(self):
        """Cierra la conexión a la base de datos."""
        if not self.db.is_closed():
            self.db.close()
            logging.info("Conexión cerrada.")
    
    def iniciar_transaccion(self):
        """Inicia una transacción."""
        self.db.begin()
        logging.info("Transacción iniciada.")

    def confirmar_transaccion(self):
        """Confirma (commit) una transacción."""
        self.db.commit()
        logging.info("Transacción confirmada.")
    
    def revertir_transaccion(self):
        """Revierte (rollback) una transacción."""
        self.db.rollback()
        logging.info("Transacción revertida.")

    def crear_proveedor(self, nombre, direccion):
        """Inserta un nuevo proveedor."""
        proveedor = Proveedor.create(nombre=nombre, direccion=direccion)
        logging.info(f"Proveedor creado: {proveedor.nombre} - {proveedor.direccion}")
        return proveedor
    
    def crear_herramienta(self, nombre, tipo, marca, uso, material, proveedor):
        """Inserta una nueva herramienta."""
        try:
            herramienta = Herramienta.create(
                nombre=nombre, tipo=tipo, marca=marca, uso=uso, material=material, proveedor=proveedor
            )
            logging.info(f"Herramienta creada: {herramienta.nombre} - {herramienta.tipo}")
            return herramienta
        except Exception as e:
            print(e)
    
    def leer_herramientas(self):
        """Lee todas las herramientas."""
        herramientas = Herramienta.select()
        logging.info("Leyendo herramientas:")
        for herramienta in herramientas:
            logging.info(f"{herramienta.nombre} - {herramienta.tipo}({herramienta.proveedor.nombre})")
        return herramientas

    def leer_herramientas_proveedor(self, proveedor_n):
        """Lee las herramientas de un proveedor."""
        herramientas = Herramienta.select().join(Proveedor).where(Proveedor.nombre == proveedor_n)
        logging.info(f"Leyendo herramientas del proveedor: {proveedor_n}")
        for herramienta in herramientas:
            logging.info(f"{herramienta.nombre} - {herramienta.tipo}({herramienta.proveedor.nombre})")
        return herramientas
    
    def actualizar_proveedor(self, n, direccionNueva):
        """Actualiza un proveedor"""
        proveedor = Proveedor.get(Proveedor.nombre == n)
        if proveedor:
            proveedor.direccion = direccionNueva
            logging.info(f"Proveedor actualizado: {proveedor.nombre} - {proveedor.direccion}" )
        else:
            logging.info(f"Proveedor no actualizado")
        return proveedor
    
    def eliminar_proveedor(self, n):
        """Elimina un proveedor"""
        try:
            proveedor = Proveedor.get(Proveedor.nombre == n)
            if proveedor:
                proveedor.delete_instance()
                logging.info(f"Proveedor eliminado: {n}" )
            else:
                logging.info(f"Proveedor no eliminado")
            return proveedor
        except Exception as e:
            print (e)

    def actualizar_herramienta(self, n, tipoNuevo):
        """Actualiza una herramienta"""
        herramienta = Herramienta.get(Herramienta.nombre == n)
        if herramienta:
            herramienta.tipo = tipoNuevo
            logging.info(f"Herramienta actualizada: {herramienta.nombre} - {herramienta.tipo}" )
        else:
            logging.info(f"Herramienta no actualizada")
        return herramienta

    def eliminar_herramienta(self, n):
        """Elimina una herramienta"""
        herramienta = Herramienta.get(Herramienta.nombre == n)
        if herramienta:
            herramienta.delete_instance()
            logging.info(f"Herramienta eliminada: {n}" )
        else:
            logging.info(f"Herramienta no eliminada")
        return herramienta        
    
db_manager = DatabaseManagerORM()
db_manager.conectar()
db_manager.iniciar_transaccion()
try:
    db_manager.crear_proveedor("Proveedor A", "123-456-789")
    db_manager.crear_proveedor("Proveedor B", "987-654-321")
    db_manager.confirmar_transaccion()
except Exception:
    db_manager.revertir_transaccion()

print("Actualizar proveedor")
db_manager.iniciar_transaccion()
try:
    db_manager.actualizar_proveedor("Proveedor A", "30284761V")
    db_manager.confirmar_transaccion()
except Exception:
    db_manager.revertir_transaccion()

print("Eliminar proveedor b")
db_manager.iniciar_transaccion()
try:
    db_manager.eliminar_proveedor("Proveedor B")
    db_manager.confirmar_transaccion()
except Exception:
    db_manager.revertir_transaccion()

print("Crear herramientas")
db_manager.iniciar_transaccion()
try:
    db_manager.crear_herramienta("Martillo", "Manual", "Obra", "Bosch", "Acero", "1")
    db_manager.crear_herramienta("Taladro", "Eléctrico", "Obra", "Hilti", "Hierro", "1")
    db_manager.confirmar_transaccion()
except Exception:
    db_manager.revertir_transaccion()

print("leer herramientas proveedor a")
db_manager.iniciar_transaccion()
try:
    db_manager.leer_herramientas_proveedor("Proveedor A")
    db_manager.confirmar_transaccion()
except Exception:
    db_manager.revertir_transaccion()

print("actualizar herramienta")
db_manager.iniciar_transaccion()
try:
    db_manager.actualizar_herramienta("Martillo", "Reforzado")
    db_manager.confirmar_transaccion()
except Exception:
    db_manager.revertir_transaccion()

db_manager.iniciar_transaccion()
print("eliminar herramienta")
try:
    db_manager.eliminar_herramienta("Taladro")
    db_manager.confirmar_transaccion()
except Exception:
    db_manager.revertir_transaccion()