# modelo_db/cargar_datos_masivos.py
import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from tqdm import tqdm

def generar_datos_masivos():
    # Conexión
    conn = psycopg2.connect(
        host="localhost",
        database="sistema_restaurante_transaccional",
        user="usuario_restaurante_transaccional",
        password="1234"
    )
    cur = conn.cursor()
    fake = Faker('es_CL')

    def obtener_ids(tabla, campo):
        cur.execute(f'SELECT "{campo}" FROM "{tabla}"')
        return [row[0] for row in cur.fetchall()]

    ingredientes_por_consumible = {
        'Completo italiano': {'Pan': 1, 'Salchicha': 1, 'Palta': 1, 'Mayonesa': 1},
        'Hamburguesa doble': {'Pan': 2, 'Hamburguesa': 2, 'Queso': 1, 'Ketchup': 1},
        'Puré con carne': {'Puré': 1, 'Carne de vacuno': 1},
        'Arroz con pollo': {'Arroz': 1, 'Pollo': 1},
        'Pan con queso': {'Pan': 1, 'Queso': 1}
    }

    def generar_ventas(fecha_inicio, fecha_fin, cantidad):
        meseros = obtener_ids("Mesero", "Id_mesero")
        mesas = obtener_ids("Mesas", "Id_Mesa")
        medios_pago = obtener_ids("Medio_Pago", "Id_Medio_Pago")
        cocineros = obtener_ids("Cocinero", "Id_cocinero")

        cur.execute('SELECT "Id_consumibles", "Nombre", "Precio_unidad" FROM "Consumibles"')
        consumibles = {row[0]: {'nombre': row[1], 'precio': row[2]} for row in cur.fetchall()}

        cur.execute('SELECT "Id_ingrediente", "Nombre" FROM "Ingredientes"')
        ingredientes_map = {row[1]: row[0] for row in cur.fetchall()}

        for _ in range(cantidad):
            fecha_venta = fake.date_time_between_dates(datetime_start=fecha_inicio, datetime_end=fecha_fin)
            id_mesero = random.choice(meseros)
            id_mesa = random.choice(mesas)
            id_medio = random.choice(medios_pago)

            productos_vendidos = random.sample(list(consumibles.items()), k=random.randint(1, 3))
            cantidad_total = 0
            total_monto = 0

            for _, info in productos_vendidos:
                cantidad = random.randint(1, 3)
                cantidad_total += cantidad
                total_monto += info['precio'] * cantidad

            cur.execute("""
                INSERT INTO "Ventas" (
                    "Cantidad_Productos", "Monto_Total", "Fecha_Venta", "FK_Id_Mesero", "FK_Id_Mesa", "FK_Id_Medio_Pago"
                ) VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING "Id_Venta"
            """, (cantidad_total, total_monto, fecha_venta, id_mesero, id_mesa, id_medio))
            id_venta = cur.fetchone()[0]

            for id, info in productos_vendidos:
                cantidad = random.randint(1, 3)
                cur.execute("""
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
                            cur.execute("""
                                INSERT INTO "Ingredientes_Usados" 
                                ("FK_Id_consumible", "FK_Id_ingrediente", "Cantidad", "Fecha_uso", "FK_Id_cocinero")
                                VALUES (%s, %s, %s, %s, %s)
                            """, (id, id_ing, total_ingrediente, fecha_venta, id_cocinero))

    def generar_reservas(fecha_inicio, fecha_fin, cantidad):
        mesas = obtener_ids("Mesas", "Id_Mesa")
        estados = ["confirmada", "pendiente", "cancelada"]
        for _ in range(cantidad):
            fecha = fake.date_time_between_dates(datetime_start=fecha_inicio, datetime_end=fecha_fin)
            fecha = fecha.replace(microsecond=0)
            cur.execute("""
                INSERT INTO "reservas" 
                ("FK_id_mesas", "estado_reserva", "fecha_reserva", "nombre_cliente", "telefono_cliente")
                VALUES (%s, %s, %s, %s, %s)
            """, (
                random.choice(mesas),
                random.choice(estados),
                fecha,
                fake.name(),
                fake.phone_number()
            ))

    try:
        hoy = datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        rangos = [(hoy - relativedelta(months=i), hoy - relativedelta(months=i) + relativedelta(months=1) - timedelta(seconds=1)) for i in range(36)]

        for inicio, fin in tqdm(rangos[::-1], desc="Cargando datos por mes"):
            generar_ventas(inicio, fin, 500)
            generar_reservas(inicio, fin, 500)
            conn.commit()

        return "✅ Datos generados correctamente para 36 meses x 3 tablas."
    except Exception as e:
        conn.rollback()
        return f"❌ Error al generar datos: {str(e)}"
    finally:
        cur.close()
        conn.close()

# Esto permite que el script siga funcionando cuando se ejecuta directamente
if __name__ == "__main__":
    print(generar_datos_masivos())