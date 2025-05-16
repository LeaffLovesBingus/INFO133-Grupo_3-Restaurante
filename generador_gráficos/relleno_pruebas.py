import psycopg2
import random
from datetime import datetime, timedelta

conn = psycopg2.connect(
    dbname="sistema_restaurante",
    user="usuario_restaurante",
    password="1234",
    host="localhost"
)
cur = conn.cursor()

cur.execute("""
INSERT INTO "Medio_Pago" ("Medio_Pago") VALUES
('Efectivo'), ('Tarjeta'), ('Transferencia');
""")

cur.execute("""
INSERT INTO "Cocinero" ("Nombre", "Apellido", "Correo", "Sueldo") VALUES
('Juan', 'Pérez', 'juan.perez@email.com', 800000),
('Ana', 'Gómez', 'ana.gomez@email.com', 850000);
""")

cur.execute("""
INSERT INTO "Mesero" ("Nombre", "Apellido", "Correo", "Sueldo") VALUES
('Luis', 'Martínez', 'luis.martinez@email.com', 500000),
('Sofía', 'López', 'sofia.lopez@email.com', 520000);
""")

cur.execute("""
INSERT INTO "Ingredientes" ("Nombre", "Tipo", "Cantidad") VALUES
('Tomate', 'Verdura', 100),
('Queso', 'Lácteo', 50),
('Pan', 'Cereal', 80);
""")

cur.execute("""
INSERT INTO "Consumibles" ("Nombre", "Precio_unidad", "Categoria") VALUES
('Hamburguesa', 3500, 'Comida'),
('Pizza', 5000, 'Comida'),
('Jugo', 1500, 'Bebida');
""")


# Parámetros base
meseros = [1, 2]
cocineros = [1, 2]
consumibles = [1, 2, 3]
ingredientes = [1, 2, 3]
medios_pago = [1, 2, 3]
mesas = [1, 2, 3, 4, 5]

# Generar ventas y consumibles vendidos
ventas = []
consumibles_vendidos = []
hechos_ingredientes = []

fecha_inicio = datetime.now() - timedelta(days=3*365)
for i in range(1, 51):  # 50 ventas
    fecha_venta = fecha_inicio + timedelta(days=random.randint(0, 3*365), hours=random.randint(10, 22))
    cantidad_productos = random.randint(1, 5)
    monto_total = cantidad_productos * random.choice([3500, 5000, 1500])
    mesero = random.choice(meseros)
    mesa = random.choice(mesas)
    medio_pago = random.choice(medios_pago)
    ventas.append((cantidad_productos, monto_total, fecha_venta, mesero, mesa, medio_pago))

# Insertar ventas
for v in ventas:
    cur.execute("""
        INSERT INTO "Hechos_Ventas" ("Cantidad_Productos", "Monto_Total", "Fecha_Venta", "FK_Id_Mesero", "Id_Mesa", "FK_Id_Medio_Pago")
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING "Id_Venta";
    """, v)
    id_venta = cur.fetchone()[0]
    # Consumibles vendidos por venta
    usados = random.sample(consumibles, random.randint(1, 3))
    for c in usados:
        cantidad = random.randint(1, 3)
        consumibles_vendidos.append((id_venta, c, cantidad))
        # Ingredientes usados por consumible
        usados_ing = random.sample(ingredientes, random.randint(1, 3))
        for ing in usados_ing:
            cantidad_ing = random.randint(1, 5)
            fecha_uso = v[2] - timedelta(hours=random.randint(1, 3))
            cocinero = random.choice(cocineros)
            hechos_ingredientes.append((c, ing, cantidad_ing, fecha_uso, cocinero))

# Insertar consumibles vendidos
for cv in consumibles_vendidos:
    cur.execute("""
        INSERT INTO "Consumibles_Vendidos" ("FK_Id_Venta", "FK_Id_Consumible", "Cantidad")
        VALUES (%s, %s, %s);
    """, cv)

# Insertar hechos ingredientes usados
for hi in hechos_ingredientes:
    cur.execute("""
        INSERT INTO "Hechos_Ingredientes_Usados" ("FK_Id_consumible", "FK_Id_ingrediente", "Cantidad", "Fecha_uso", "FK_Id_cocinero")
        VALUES (%s, %s, %s, %s, %s);
    """, hi)

conn.commit()
cur.close()
conn.close()
print("Datos de prueba insertados correctamente.")