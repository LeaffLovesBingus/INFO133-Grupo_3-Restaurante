import psycopg2
from faker import Faker
import random
from datetime import datetime

# no ventas, ingredientes usados , reserva

def generar_datos():
    global conn_dr
    global cur_dr
    
    conn_dr = psycopg2.connect(
        host="localhost",
        database="sistema_restaurante",
        user="usuario_restaurante",
        password="1234"
    )
    cur_dr = conn_dr.cursor()

    generarMesas(8)
    generarMedioPago()
    generarMeseros(10)
    generarCocineros(5)
    generarConsumibles()
    generarIngrediente()

    conn_dr.commit()
    cur_dr.close()
    conn_dr.close()
    ###

fake = Faker('es_CL')
def generarMesas(n):
    for i in range(n):
        capacidad = random.choice([2,4])
        cur_dr.execute("""
            INSERT INTO "Mesas" ("Capacidad")
            VALUES (%s)
            """, (capacidad,)) # si se devuelve 1 cosa se coloca (,) aca
        
def generarMedioPago():
    medios = ['Efectivo', 'Tarjeta Crédito', 'Tarjeta Débito', 'Transferencia', 'Cheque']
    for medio in medios:
        cur_dr.execute("""
            INSERT INTO "Medio_Pago" ("Medio_Pago")
            VALUES (%s)
        """, (medio,))

def generarMeseros(n):
    for i in range(n):
        nombre = fake.first_name()
        apellido = fake.last_name()
        correo = fake.email()
        sueldo = random.choice([500000,650000])
        cur_dr.execute("""
            INSERT INTO "Empleados" ("Nombre", "Apellido", "Correo", "Sueldo")
            VALUES (%s, %s, %s, %s)
            RETURNING "Id_empleado"
        """, (nombre, apellido, correo, sueldo))
        id_empleado = cur_dr.fetchone()[0]

        cur_dr.execute("""
            INSERT INTO "Mesero" ("Id_mesero")
            VALUES (%s)
        """, (id_empleado,))

def generarCocineros(n):
    for i in range(n):
        nombre = fake.first_name()
        apellido = fake.last_name()
        correo = fake.email()
        sueldo = random.choice([700000,800000])
        cur_dr.execute("""
                       INSERT INTO "Empleados" ("Nombre", "Apellido", "Correo", "Sueldo")
                       VALUES (%s,%s,%s,%s)
                       """, (nombre,apellido,correo,sueldo))
        id_empleado = cur_dr.fetchone()[0]
        cur_dr.execute("""
                       INSERT INTO "Cocinero" ("Id_cocinero")
                       VALUES (%s)
        """, (id_empleado,))
        
def generarConsumibles():
    menu = {
        'Hamburguesa doble': (3500, 'Plato'),
        'Completo italiano': (2500, 'Entrada'),
        'Puré con carne': (3000, 'Plato'),
        'Arroz con pollo': (3200, 'Plato'),
        'Pan con queso': (900, 'Entrada'),
        'Jugo natural': (1500, 'Bebida'),
        'Helado': (1200, 'Postre')
    }

    for nombre, (precio, categoria) in menu.items():
        cur_dr.execute("""
            INSERT INTO "Consumibles" ("Nombre", "Precio_unidad", "Categoria")
            VALUES (%s, %s, %s)
        """, (nombre, precio, categoria))
        
def generarIngrediente():
    tipos = {
        'Verdura': ['Tomate', 'Lechuga', 'Palta'],
        'Carne': ['Hamburguesa', 'Salchicha','Carne de vacuno','Pollo'],
        'Aderezo': ['Mayonesa', 'Mostaza', 'Ketchup'],
        'Misc': ['Puré', 'Arroz'],
        'Lácteo': ['Queso'],
        'Masas': ['Pan']
    }

    for tipo,lista in tipos.items():
        for nombre in lista:
            cantidad = random.randint(5,20)
            cur_dr.execute("""
                           INSERT INTO "Ingredientes" ("Nombre","Tipo","Cantidad")
                           VALUES (%s,%s,%s)
                           """, (nombre,tipo,cantidad))
            



