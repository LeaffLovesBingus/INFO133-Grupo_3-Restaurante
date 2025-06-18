import psycopg2
from faker import Faker
import random
from datetime import datetime

def generarDatosCRUD():
    global conn_dr
    global cur_dr
    
    conn_dr = psycopg2.connect(
        host="localhost",
        database="sistema_restaurante_transaccional",
        user="usuario_restaurante_transaccional",
        password="1234"
    )
    cur_dr = conn_dr.cursor()



    conn_dr.commit()
    cur_dr.close()
    conn_dr.close()


fake = Faker('es_CL')



def obtener_ids(tabla, campo): #chatgpt me corrigio esto, funcionaba sin eso pero asi se ve mas claro
    cur_dr.execute(f'SELECT "{campo}" FROM "{tabla}"')
    return [row[0] for row in cur_dr.fetchall()]


ingredientes_por_consumible = {
    'Completo italiano': {'Pan': 1, 'Salchicha': 1, 'Palta': 1, 'Mayonesa': 1},
    'Hamburguesa doble': {'Pan': 2, 'Hamburguesa': 2, 'Queso': 1, 'Ketchup': 1},
    'Puré con carne': {'Puré': 1, 'Carne de vacuno': 1},
    'Arroz con pollo': {'Arroz': 1, 'Pollo': 1},
    'Pan con queso': {'Pan': 1, 'Queso': 1}
}

def generarVentas(n): #incluye ingredientes usados
    meseros = obtener_ids("Mesero", "Id_mesero")
    mesas = obtener_ids("Mesas", "Id_Mesa")
    medios_pago = obtener_ids("Medio_Pago", "Id_Medio_Pago")
    consumibles = {}
    cur_dr.execute('SELECT "Id_consumibles", "Nombre", "Precio_unidad" FROM "Consumibles"')
    for row in cur_dr.fetchall():
        consumibles[row[0]] = {'nombre': row[1], 'precio': row[2]}
    cocineros = obtener_ids("Cocinero", "Id_cocinero")
    ingredientes_map = {}
    cur_dr.execute('SELECT "Id_ingrediente", "Nombre" FROM "Ingredientes"')
    for row in cur_dr.fetchall():
        ingredientes_map[row[1]] = row[0]

    for _ in range(n):
        id_mesero = random.choice(meseros)
        id_mesa = random.choice(mesas)
        id_medio = random.choice(medios_pago)
        fecha_venta = fake.date_time_between(start_date='-1y', end_date='now')
        productos_vendidos = random.sample(list(consumibles.items()), k=random.randint(1, 3))

        cantidad_total = 0
        total_monto = 0
        for _, info in productos_vendidos:
            cantidad = random.randint(1, 3)
            cantidad_total += cantidad
            total_monto += info['precio'] * cantidad

        cur_dr.execute("""
            INSERT INTO "Ventas" (
                "Cantidad_Productos", "Monto_Total", "Fecha_Venta", "FK_Id_Mesero", "FK_Id_Mesa", "FK_Id_Medio_Pago"
            ) VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING "Id_Venta"
        """, (cantidad_total, total_monto, fecha_venta, id_mesero, id_mesa, id_medio))
        id_venta = cur_dr.fetchone()[0]

        for id, info in productos_vendidos:
            cantidad = random.randint(1, 3)
            cur_dr.execute("""
                INSERT INTO "Consumibles_Vendidos" ("FK_Id_Venta", "FK_Id_Consumible", "Cantidad")
                VALUES (%s, %s, %s)
            """, (id_venta, id, cantidad))


            nombre = info['nombre']
            if nombre in ingredientes_por_consumible:
                for ing_nombre, cant_unidad in ingredientes_por_consumible[nombre].items():
                    if ing_nombre in ingredientes_map:
                        id_ing = ingredientes_map[ing_nombre]
                        id_cocinero = random.choice(cocineros)
                        total_ingrediente = cant_unidad * cantidad
                        cur_dr.execute("""
                            INSERT INTO "Ingredientes_Usados" 
                            ("FK_Id_consumible", "FK_Id_ingrediente", "Cantidad", "Fecha_uso", "FK_Id_cocinero")
                            VALUES (%s, %s, %s, %s, %s)
                        """, (id, id_ing, total_ingrediente, fecha_venta, id_cocinero))

def generarReservas(n):
    mesas = obtener_ids("Mesas", "Id_Mesa")
    estados = ["confirmada","pendiente", "cancelada"]
    for _ in range(n):
        id_mesa = random.choice(mesas)
        fecha_reserva = fake.date_time_between(start_date='-1y', end_date='+30d')
        fecha_reserva = fecha_reserva.replace(microsecond=0) #por alguna razon solo en reservas se generaban las fechas con microsegundos, en teoria esto los saca
        nombre = fake.name()
        telefono = fake.phone_number()
        estado = random.choice(estados)
        cur_dr.execute("""
            INSERT INTO "reservas" 
            ("FK_id_mesas", "estado_reserva", "fecha_reserva", "nombre_cliente", "telefono_cliente")
            VALUES (%s, %s, %s, %s, %s)
        """, (id_mesa, estado, fecha_reserva, nombre, telefono))




