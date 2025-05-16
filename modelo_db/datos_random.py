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

fake = Faker('es_CL') # datos basados en chile

    #este va a crear los datos varios de las tablas 'primarias', las que dependen de ellas se generan despues de estas

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
    conn.commit()

def generarMedioPago(n):
    medios = ['Efectivo', 'Tarjeta Crédito', 'Tarjeta Débito', 'Transferencia', 'Cheque']
    for medio in medios:
        cur.execute("""
            INSERT INTO "Medio_Pago" (Medio_Pago)
            VALUES (%s)
        """, (medio,))
    conn.commit()

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
    conn.commit()

def generarIngredientes(n):
    tipos = {
        'Verdura': ['Tomate', 'Lechuga', 'Palta'],
        'Carne': ['Hamburguesa', 'Salchicha'],
        'Aderezo': ['Mayonesa', 'Mostaza', 'Ketchup'],
        'Misc': ['Puré', 'Arroz'],
        'Lácteo': ['Queso'],
        'Masas': ['Pan']
    }

    todos_ingredientes = [ing for sublist in tipos.values() for ing in sublist] # esta deja el diccionario como una lista para acceder mas fácil a los ingredientes
    ingredientes_seleccionados = random.sample(todos_ingredientes, min(n, len(todos_ingredientes)))

    for nombre in ingredientes_seleccionados:
        tipo = next((key for key, lista in tipos.items() if nombre in lista), 'Misc')
        cantidad = random.randint(3, 5)
        cur.execute("""
            INSERT INTO "Ingredientes" (Nombre, Tipo, Cantidad)
            VALUES (%s, %s, %s)
        """, (nombre, tipo, cantidad))
    conn.commit()


def generarConsumibles(n):
    categorias = ['Bebida', 'Entrada', 'Plato', 'Postre']
    nombre_menu = [] #añadir nombres para el menu
    for _ in range(n):
        nombre = random.choice(nombre_menu)
        precio = random.randint(1000, 10000)
        categoria = random.choice(categorias)
        cur.execute("""
            INSERT INTO "Consumibles" (Nombre, Precio_unidad, Categoria)
            VALUES (%s, %s, %s)
        """, (nombre, precio, categoria))
    conn.commit()

if __name__ == "__main__":

    # no ejecutar aun hay que ver con que numeros en concreto se va a hacer y añadir datos del menu
    generarMedioPago();
    meseros = int(input("Cantidad de meseros: "));
    generarMeseros(meseros);
    cocineros = int(input("Cantidad de cocineros "));
    generarCocineros(cocineros)

    generarIngredientes(5)
    generarConsumibles(5)
    print("pesco")

cur.close()
conn.close()
