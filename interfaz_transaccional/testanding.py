from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import psycopg2
from medio_pago import create as create_medio_pago, update as update_medio_pago, delete as delete_medio_pago

app = Flask(__name__)

@app.route("/")

def index():
    return render_template(template_name_or_list='index.html')

@app.route('/reservas/<string:action>')

def reservas(action):

    # Connect to the database
    conn = psycopg2.connect(
        host="localhost",
        database="sistema_restaurante_transaccional",
        user="usuario_restaurante_transaccional",
        password="1234"
    )

    # create a cursor
    cur = conn.cursor()

    # Select all products from the table
    cur.execute('''SELECT * FROM "reservas"''')

    # Fetch the data
    data = cur.fetchall()
    data = [
        row[:3] + (datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S"),) + row[4:]
        if isinstance(row[3], str) else row
        for row in data
    ]

    cur.execute('''SELECT * FROM "Mesas"''')
    mesas = cur.fetchall()

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template(template_name_or_list='reservas_mesas.html', data=data, 
                           action=action, mesas=mesas)

@app.route("/ventas/<string:accion>")

def ventas(accion):
    # Connect to the database
    conn = psycopg2.connect(
        host="localhost",
        database="sistema_restaurante_transaccional",
        user="usuario_restaurante_transaccional",
        password="1234"
    )

    # create a cursor
    cur = conn.cursor()

    # Select all products from the table
    cur.execute('''SELECT * FROM "Ventas"''')

    # Fetch the data
    data = cur.fetchall()

    data = [
        row[:3] + (datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S"),) + row[4:]
        if isinstance(row[3], str) else row
        for row in data
    ]

    cur.execute('''SELECT * FROM "Medio_Pago"''')
    medios_pago = cur.fetchall()

    cur.execute('''SELECT * FROM "Mesas"''')
    mesas = cur.fetchall()

    cur.execute('''SELECT m."Id_mesero", e."Nombre" FROM "Mesero" m
                 JOIN "Empleados" e ON m."Id_mesero" = e."Id_empleado"''')
    meseros = cur.fetchall()

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template('ventas_realizadas.html', data=data,
                            action=accion, medios_pago=medios_pago,
                            meseros=meseros, mesas=mesas)

@app.route("/ingredientes/<string:accion>")

def ingredientes(accion):
    # Connect to the database
    conn = psycopg2.connect(
        host="localhost",
        database="sistema_restaurante_transaccional",
        user="usuario_restaurante_transaccional",
        password="1234"
    )

    # create a cursor
    cur = conn.cursor()

    # Select all products from the table
    cur.execute('''SELECT * FROM "Ingredientes_Usados"''')

    # Fetch the data
    data = cur.fetchall()

    data = [
        row[:4] + (datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S"),) + row[5:]
        if isinstance(row[4], str) else row
        for row in data
    ]

    cur.execute('''SELECT * FROM "Ingredientes"''')
    ingredientes = cur.fetchall()

    cur.execute('''SELECT * FROM "Consumibles"''')
    consumibles = cur.fetchall()

    cur.execute('''SELECT c."Id_cocinero", e."Nombre" FROM "Cocinero" c
                 JOIN "Empleados" e ON c."Id_cocinero" = e."Id_empleado"''')
    cocineros = cur.fetchall()

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template('ingredientes_usados.html', data=data, 
                           action=accion, ingredientes=ingredientes,
                           consumibles=consumibles, cocineros=cocineros)

@app.route('/medio_pago/<string:action>')

def medio_pago(action):

    # Connect to the database
    conn = psycopg2.connect(
        host="localhost",
        database="sistema_restaurante_transaccional",
        user="usuario_restaurante_transaccional",
        password="1234"
    )

    # create a cursor
    cur = conn.cursor()

    cur.execute('''SELECT * FROM "Medio_Pago"''')

    data = cur.fetchall()

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template(template_name_or_list='medio_pago.html', data=data, action=action)


@app.route('/medio_pago/create', methods=['POST'])
def create_medio_pago_route():
    return create_medio_pago()

@app.route('/medio_pago/update', methods=['POST'])
def update_medio_pago_route():
    return update_medio_pago()

@app.route('/medio_pago/delete', methods=['POST'])
def delete_medio_pago_route():
    return delete_medio_pago()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
