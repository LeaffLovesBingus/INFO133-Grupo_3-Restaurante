import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta


def generar_datos_random():
    global conn_dr
    global cur_dr

    conn_dr = psycopg2.connect(
        host="localhost",
        database="sistema_restaurante",
        user="usuario_restaurante",
        password="1234"
    )
    cur_dr = conn_dr.cursor()

    generarMedioPago()
    generarMeseros(15)
    generarCocineros(15)
    generarIngredientes() #5
    generarConsumibles(5) #5
    print("Datos generados correctamente")
    generarVentas(800)
    print("Ventas generadas correctamente")
    
    conn_dr.commit()
    cur_dr.close()
    conn_dr.close()


fake = Faker('es_CL')

ingredientes_por_consumible = {
    'Completo italiano': {
        'Pan': 1,
        'Salchicha': 1,
        'Palta': 1,
        'Mayonesa': 1
    },
    'Hamburguesa doble': {
        'Pan': 2,
        'Hamburguesa': 2,
        'Queso': 1,
        'Ketchup': 1
    },
    'Puré con carne': {
        'Puré': 1,
        'Carne de vacuno': 1
    },
    'Arroz con pollo': {
        'Arroz': 1,
        'Pollo': 1
    },
    'Pan con queso': {
        'Pan': 1,
        'Queso': 1
    },
    'Jugo natural': {},
    'Helado': {}
}

def generarMeseros(n):
    for _ in range(n):
        nombre = fake.first_name()
        apellido = fake.last_name()
        correo = fake.email()
        sueldo = random.choice([500000,800000])
        cur_dr.execute("""
            INSERT INTO "Mesero" ("Nombre", "Apellido", "Correo", "Sueldo")
            VALUES (%s, %s, %s, %s)
            """, (nombre, apellido, correo, sueldo))

def generarMedioPago():
    medios = ['Efectivo', 'Tarjeta Crédito', 'Tarjeta Débito', 'Transferencia', 'Cheque']
    for medio in medios:
        cur_dr.execute("""
            INSERT INTO "Medio_Pago" ("Medio_Pago")
            VALUES (%s)
        """, (medio,))

def generarCocineros(n):
    for _ in range(n):
        nombre = fake.first_name()
        apellido = fake.last_name()
        correo = fake.email()
        sueldo = random.choice([500000, 800000])
        cur_dr.execute("""
            INSERT INTO "Cocinero" ("Nombre", "Apellido", "Correo", "Sueldo")
            VALUES (%s, %s, %s, %s)
        """, (nombre, apellido, correo, sueldo))

def generarIngredientes():
    tipos = {
        'Verdura': ['Tomate', 'Lechuga', 'Palta'],
        'Carne': ['Hamburguesa', 'Salchicha','Carne de vacuno','Pollo'],
        'Aderezo': ['Mayonesa', 'Mostaza', 'Ketchup'],
        'Misc': ['Puré', 'Arroz'],
        'Lácteo': ['Queso'],
        'Masas': ['Pan']
    }
    for tipo, lista in tipos.items():
        for nombre_ingrediente in lista:
            cantidad = random.randint(3,5)
            cur_dr.execute("""
            INSERT INTO "Ingredientes" ("Nombre", "Tipo", "Cantidad")
            VALUES (%s, %s, %s)
            """, (nombre_ingrediente, tipo, cantidad))
            

def generarConsumibles(n):
    nombre_menu = {
        'Hamburguesa doble': (3500, 'Plato'),
        'Completo italiano': (2500, 'Entrada'),
        'Puré con carne': (3000, 'Plato'),
        'Arroz con pollo': (3200, 'Plato'),
        'Pan con queso': (900, 'Entrada'),
        'Jugo natural': (1500, 'Bebida'),
        'Helado': (1200, 'Postre')
    }
    for _ in range(n):
        nombre = random.choice(list(nombre_menu.keys()))
        precio, categoria = nombre_menu[nombre]
        cur_dr.execute("""
            INSERT INTO "Consumibles" ("Nombre", "Precio_unidad", "Categoria")
            VALUES (%s, %s, %s)
        """, (nombre, precio, categoria))

def registrarIngredientesUsados(id_venta, detalles):
    for id_cons, cantidad_vendida in detalles:
        cur_dr.execute('SELECT "Nombre" FROM "Consumibles" WHERE "Id_consumibles" = %s', (id_cons,))
        res = cur_dr.fetchone()
        if not res:
            continue
        nombre_consumible = res[0]
        if nombre_consumible not in ingredientes_por_consumible:
            continue
        ingredientes = ingredientes_por_consumible[nombre_consumible]
        for nombre_ingrediente, cant_por_unidad in ingredientes.items():
            cantidad_total = cant_por_unidad * cantidad_vendida
            cur_dr.execute('SELECT "Id_ingrediente" FROM "Ingredientes" WHERE "Nombre" = %s', (nombre_ingrediente,))
            res_ing = cur_dr.fetchone()
            if res_ing is None:
                continue
            id_ingrediente = res_ing[0]
            cur_dr.execute('SELECT "Id_cocinero" FROM "Cocinero" ORDER BY RANDOM() LIMIT 1')
            id_cocinero = cur_dr.fetchone()[0]
            cur_dr.execute("""
                INSERT INTO "Hechos_Ingredientes_Usados"
                ("FK_Id_consumible", "FK_Id_ingrediente", "Cantidad", "Fecha_uso", "FK_Id_cocinero")
                VALUES (%s, %s, %s, NOW(), %s)
            """, (id_cons, id_ingrediente, cantidad_total, id_cocinero))

def generarVentas(n):
    cur_dr.execute('SELECT "Id_mesero" FROM "Mesero"')
    meseros = [row[0] for row in cur_dr.fetchall()]
    cur_dr.execute('SELECT "Id_Medio_Pago" FROM "Medio_Pago"')
    medios = [row[0] for row in cur_dr.fetchall()]
    cur_dr.execute('SELECT "Id_consumibles", "Precio_unidad" FROM "Consumibles"')
    consumibles = cur_dr.fetchall()
    if not meseros or not medios or not consumibles:
        return
    for _ in range(n):
        cantidad_clientes = random.randint(1, 6)
        id_mesero = random.choice(meseros)
        id_medio = random.choice(medios)
        id_mesa = random.randint(1, 10)
        fecha_venta = fake.date_time_between(start_date='-30d', end_date='now')
        num_productos = random.randint(1, 5)
        productos_vendidos = random.sample(consumibles, min(num_productos, len(consumibles)))
        monto_total = 0
        detalles = []
        for id_prod, precio in productos_vendidos:
            cantidad = random.randint(1, 3)
            monto_total += precio * cantidad
            detalles.append((id_prod, cantidad))
        cur_dr.execute("""
            INSERT INTO "Hechos_Ventas" 
            ("Cantidad_Productos", "Cantidad_clientes", "Monto_Total", "Fecha_Venta", "FK_Id_Mesero", "Id_Mesa", "FK_Id_Medio_Pago")
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING "Id_Venta"
        """, (num_productos, cantidad_clientes, monto_total, fecha_venta, id_mesero, id_mesa, id_medio))
        id_venta = cur_dr.fetchone()[0]
        for id_prod, cantidad in detalles:
            cur_dr.execute("""
                INSERT INTO "Consumibles_Vendidos" ("FK_Id_Venta", "FK_Id_Consumible", "Cantidad")
                VALUES (%s, %s, %s)
            """, (id_venta, id_prod, cantidad))
        registrarIngredientesUsados(id_venta, detalles)