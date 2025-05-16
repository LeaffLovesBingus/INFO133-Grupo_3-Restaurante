import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta

conn = psycopg2.connect(
    host="localhost",
    database="restaurante",
    user="(usuario del postgres)",
    password="(la clave)"
)
cur = conn.cursor()

# nota: no me podido probar si esto funciona porque aun tengo que solucionar algo con mi pc
# segun yo tiene sentido y el chatgpt me dice que esta bien

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
        sueldo = random.randint(500000,800000)
        cur.execute("""
            INSERT INTO "Mesero" (Nombre, Apellido, Correo, Sueldo)
            VALUES (%s, %s, %s, %s)
            """, (nombre, apellido, correo, sueldo))

def generarMedioPago():
    medios = ['Efectivo', 'Tarjeta Crédito', 'Tarjeta Débito', 'Transferencia', 'Cheque']
    for medio in medios:
        cur.execute("""
            INSERT INTO "Medio_Pago" (Medio_Pago)
            VALUES (%s)
        """, (medio,))

def generarCocineros(n):
    for _ in range(n):
        nombre = fake.first_name()
        apellido = fake.last_name()
        correo = fake.email()
        sueldo = random.randint(500000, 800000)
        cur.execute("""
            INSERT INTO "Cocinero" (Nombre, Apellido, Correo, Sueldo)
            VALUES (%s, %s, %s, %s)
        """, (nombre, apellido, correo, sueldo))

def generarIngredientes(n):
    tipos = {
        'Verdura': ['Tomate', 'Lechuga', 'Palta'],
        'Carne': ['Hamburguesa', 'Salchicha','Carne de vacuno','Pollo'],
        'Aderezo': ['Mayonesa', 'Mostaza', 'Ketchup'],
        'Misc': ['Puré', 'Arroz'],
        'Lácteo': ['Queso'],
        'Masas': ['Pan']
    }
    todos_ingredientes = [ing for sublist in tipos.values() for ing in sublist]
    ingredientes_seleccionados = random.sample(todos_ingredientes, min(n, len(todos_ingredientes)))
    for nombre in ingredientes_seleccionados:
        tipo = next((key for key, lista in tipos.items() if nombre in lista), 'Misc')
        cantidad = random.randint(3, 5)
        cur.execute("""
            INSERT INTO "Ingredientes" (Nombre, Tipo, Cantidad)
            VALUES (%s, %s, %s)
        """, (nombre, tipo, cantidad))

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
        cur.execute("""
            INSERT INTO "Consumibles" (Nombre, Precio_unidad, Categoria)
            VALUES (%s, %s, %s)
        """, (nombre, precio, categoria))

def registrarIngredientesUsados(id_venta, detalles):
    for id_cons, cantidad_vendida in detalles:
        cur.execute('SELECT Nombre FROM "Consumibles" WHERE Id_consumibles = %s', (id_cons,))
        res = cur.fetchone()
        if not res:
            continue
        nombre_consumible = res[0]
        if nombre_consumible not in ingredientes_por_consumible:
            continue
        ingredientes = ingredientes_por_consumible[nombre_consumible]
        for nombre_ingrediente, cant_por_unidad in ingredientes.items():
            cantidad_total = cant_por_unidad * cantidad_vendida
            cur.execute('SELECT Id_ingrediente FROM "Ingredientes" WHERE Nombre = %s', (nombre_ingrediente,))
            res_ing = cur.fetchone()
            if res_ing is None:
                continue
            id_ingrediente = res_ing[0]
            cur.execute('SELECT Id_cocinero FROM "Cocinero" ORDER BY RANDOM() LIMIT 1')
            id_cocinero = cur.fetchone()[0]
            cur.execute("""
                INSERT INTO "Hechos_Ingredientes_Usados"
                (FK_Id_consumible, FK_Id_ingrediente, Cantidad, Fecha_uso, FK_Id_cocinero)
                VALUES (%s, %s, %s, NOW(), %s)
            """, (id_cons, id_ingrediente, cantidad_total, id_cocinero))

def generarVentas(n):
    cur.execute('SELECT Id_mesero FROM "Mesero"')
    meseros = [row[0] for row in cur.fetchall()]
    cur.execute('SELECT Id_Medio_Pago FROM "Medio_Pago"')
    medios = [row[0] for row in cur.fetchall()]
    cur.execute('SELECT Id_consumibles, Precio_unidad FROM "Consumibles"')
    consumibles = cur.fetchall()
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
        cur.execute("""
            INSERT INTO "Hechos_Ventas" 
            (Cantidad_Productos, Cantidad_clientes, Monto_Total, Fecha_Venta, FK_Id_Mesero, Id_Mesa, FK_Id_Medio_Pago)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING Id_Venta
        """, (num_productos, cantidad_clientes, monto_total, fecha_venta, id_mesero, id_mesa, id_medio))
        id_venta = cur.fetchone()[0]
        for id_prod, cantidad in detalles:
            cur.execute("""
                INSERT INTO "Consumibles_Vendidos" (FK_Id_Venta, FK_Id_Consumible, Cantidad)
                VALUES (%s, %s, %s)
            """, (id_venta, id_prod, cantidad))
        registrarIngredientesUsados(id_venta, detalles)
    conn.commit()

if __name__ == "__main__":
    generarMedioPago()
    meseros = int(input("Cantidad de meseros: "))
    generarMeseros(meseros)
    cocineros = int(input("Cantidad de cocineros: "))
    generarCocineros(cocineros)
    generarIngredientes(5)
    generarConsumibles(5)
    print("pescó")

    ventas = int(input("Ventas a generar: "))
    generarVentas(ventas)

cur.close()
conn.close()
