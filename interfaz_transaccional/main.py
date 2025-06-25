from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import psycopg2
from reservas import create as create_reserva, update as update_reserva, delete as delete_reserva
from ventas import create as create_ventas, update as update_ventas, delete as delete_ventas
from ingredientes import create as create_ingredientes, update as update_ingredientes, delete as delete_ingredientes
from carga_datos import carga_datos_bp

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

    year = request.args.get('year')
    mes = request.args.get('mes')

    # Valores por defecto si no hay filtro
    if not year:
        year = "2025"
    if not mes:
        mes = "6"

    # create a cursor
    cur = conn.cursor()

    # Select all products from the table
    cur.execute(f'''SELECT * FROM "reservas" WHERE 
                EXTRACT(YEAR FROM "fecha_reserva") = {year} AND 
                EXTRACT(MONTH FROM "fecha_reserva") = {mes}
                ORDER BY "fecha_reserva" ASC''')

    # Fetch the data
    data = cur.fetchall()
    data = [
        row[:3] + (datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S"),) + row[4:]
        if isinstance(row[3], str) else row
        for row in data
    ]

    cur.execute('SELECT DISTINCT EXTRACT(YEAR FROM "fecha_reserva") FROM "reservas" ORDER BY 1 DESC')

    years = [str(int(row[0])) for row in cur.fetchall()]
    
    cur.execute(f'''
        SELECT DISTINCT EXTRACT(MONTH FROM "fecha_reserva") 
        FROM "reservas" 
        WHERE EXTRACT(YEAR FROM "fecha_reserva") = {year}
        ORDER BY 1
        ''')
    
    meses_raw = cur.fetchall()
    meses = [(str(int(row[0])), nombre_mes(int(row[0]))) for row in meses_raw]

    cur.execute('''SELECT * FROM "Mesas"''')
    mesas = cur.fetchall()

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template(
        template_name_or_list='reservas_mesas.html', 
        data=data, 
        action=action, 
        mesas=mesas,
        years=years,
        meses=meses,
        year_actual=year,
        mes_actual=mes)

@app.route("/ventas/<string:accion>")
def ventas(accion):
    # Connect to the database
    conn = psycopg2.connect(
        host="localhost",
        database="sistema_restaurante_transaccional",
        user="usuario_restaurante_transaccional",
        password="1234"
    )

    year = request.args.get('year')
    mes = request.args.get('mes')
    if not year:
        year = "2025"
    if not mes:
        mes = "6"
    cur = conn.cursor()
    cur.execute(f'''SELECT * FROM "Ventas" WHERE 
                EXTRACT(YEAR FROM "Fecha_Venta") = {year} AND 
                EXTRACT(MONTH FROM "Fecha_Venta") = {mes}
                ORDER BY "Fecha_Venta" ASC''')
    data = cur.fetchall()
    data = [
        row[:3] + (datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S"),) + row[4:]
        if isinstance(row[3], str) else row
        for row in data
    ]
    cur.execute('SELECT DISTINCT EXTRACT(YEAR FROM "Fecha_Venta") FROM "Ventas" ORDER BY 1 DESC')
    years = [str(int(row[0])) for row in cur.fetchall()]
    cur.execute(f'''
        SELECT DISTINCT EXTRACT(MONTH FROM "Fecha_Venta") 
        FROM "Ventas" 
        WHERE EXTRACT(YEAR FROM "Fecha_Venta") = {year}
        ORDER BY 1
        ''')
    meses_raw = cur.fetchall()
    meses = [(str(int(row[0])), nombre_mes(int(row[0]))) for row in meses_raw]

    # Obtener los medios de pago, mesas y meseros

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

    return render_template(
        'ventas_realizadas.html',
        data=data,
        action=accion,
        medios_pago=medios_pago,
        meseros=meseros,
        mesas=mesas,
        years=years,
        meses=meses,
        year_actual=year,
        mes_actual=mes
    )
@app.route("/ingredientes/<string:accion>")

def ingredientes(accion):
    # Connect to the database
    conn = psycopg2.connect(
        host="localhost",
        database="sistema_restaurante_transaccional",
        user="usuario_restaurante_transaccional",
        password="1234"
    )

    year = request.args.get('year')
    mes = request.args.get('mes')
    if not year:
        year = "2025"
    if not mes:
        mes = "6"
    cur = conn.cursor()
    cur.execute(f'''SELECT * FROM "Ingredientes_Usados" WHERE 
                EXTRACT(YEAR FROM "Fecha_uso") = {year} AND 
                EXTRACT(MONTH FROM "Fecha_uso") = {mes}
                ORDER BY "Fecha_uso" ASC''')
    data = cur.fetchall()
    data = [
        row[:4] + (datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S"),) + row[5:]
        if isinstance(row[4], str) else row
        for row in data
    ]
    cur.execute('SELECT DISTINCT EXTRACT(YEAR FROM "Fecha_uso") FROM "Ingredientes_Usados" ORDER BY 1 DESC')
    years = [str(int(row[0])) for row in cur.fetchall()]
    cur.execute(f'''
        SELECT DISTINCT EXTRACT(MONTH FROM "Fecha_uso") 
        FROM "Ingredientes_Usados" 
        WHERE EXTRACT(YEAR FROM "Fecha_uso") = {year}
        ORDER BY 1
        ''')
    meses_raw = cur.fetchall()
    meses = [(str(int(row[0])), nombre_mes(int(row[0]))) for row in meses_raw]

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

    return render_template(
        'ingredientes_usados.html', 
        data=data, 
        action=accion, 
        ingredientes=ingredientes,
        consumibles=consumibles, 
        cocineros=cocineros,
        years=years,
        meses=meses,
        year_actual=year,
        mes_actual=mes
        )

# Limpiar Tablas
@app.route('/limpiar_tablas', methods=['POST'])

def limpiar_tablas():
    conn = psycopg2.connect(
        host="localhost",
        database="sistema_restaurante_transaccional",
        user="usuario_restaurante_transaccional",
        password="1234"
    )
    cur = conn.cursor()
    # Borra primero las tablas hijas (las que tienen FK)
    cur.execute('DELETE FROM "Consumibles_Vendidos"')
    cur.execute('DELETE FROM "Ingredientes_Usados"')
    cur.execute('DELETE FROM "reservas"')
    cur.execute('DELETE FROM "Ventas"')
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

# Reservas
@app.route('/reserva/create', methods=['POST'])
def create_reserva_route():
    return create_reserva()

@app.route('/reserva/update', methods=['POST'])
def update_reserva_route():
    return update_reserva()

@app.route('/reserva/delete', methods=['POST'])
def delete_reserva_route():
    return delete_reserva()

# Ventas
@app.route('/ventas/create', methods=['POST'])
def create_ventas_route():
    return create_ventas()

@app.route('/ventas/update', methods=['POST'])
def update_ventas_route():
    return update_ventas()

@app.route('/ventas/delete', methods=['POST'])
def delete_ventas_route():
    return delete_ventas()

# Ingredientes
@app.route('/ingredientes/create', methods=['POST'])
def create_ingredientes_route():
    return create_ingredientes()

@app.route('/ingredientes/update', methods=['POST'])
def update_ingredientes_route():
    return update_ingredientes()

@app.route('/ingredientes/delete', methods=['POST'])
def delete_ingredientes_route():
    return delete_ingredientes()

app.register_blueprint(carga_datos_bp)

def nombre_mes(numero):
    nombres = [
        '', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ]
    return nombres[int(numero)]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
