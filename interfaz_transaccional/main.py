from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from math import ceil
import psycopg2
from reservas import create as create_reserva, update as update_reserva, delete as delete_reserva
from ventas import create as create_ventas, update as update_ventas, delete as delete_ventas
from ingredientes import create as create_ingredientes, update as update_ingredientes, delete as delete_ingredientes
from carga_datos import carga_datos_bp
from cargar_analisis import mostrar_graficos, graficos_static

app = Flask(__name__)

@app.route("/")
def index():
    return render_template(template_name_or_list='index.html')

@app.route('/reservas/<string:action>')
def reservas(action):
    try:
        page = int(request.args.get('page', 1))
        per_page = 25
        offset = (page - 1) * per_page

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
        cur.execute(f'''SELECT COUNT(*) FROM "reservas"
                    WHERE EXTRACT(YEAR FROM "fecha_reserva") = {year} 
                    AND EXTRACT(MONTH FROM "fecha_reserva") = {mes}''')
        total = cur.fetchone()[0]
        total_pages = ceil(total / per_page)

        cur.execute(f'''SELECT * FROM "reservas" WHERE 
                    EXTRACT(YEAR FROM "fecha_reserva") = {year} AND 
                    EXTRACT(MONTH FROM "fecha_reserva") = {mes}
                    ORDER BY "fecha_reserva" ASC
                    LIMIT {per_page} OFFSET {offset}''')
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

        cur.close()
        conn.close()

        return render_template(
            template_name_or_list='reservas_mesas.html', 
            data=data, 
            page=page,
            total_pages=total_pages,
            action=action, 
            mesas=mesas,
            years=years,
            meses=meses,
            year_actual=year,
            mes_actual=mes)
    except Exception as e:
        return f"Error en reservas: {e}"

@app.route("/ventas/<string:accion>")
def ventas(accion):
    try:
        page = int(request.args.get('page', 1))
        per_page = 25
        offset = (page - 1) * per_page

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

        cur.execute(f'''SELECT COUNT(*) FROM "Ventas"
                    WHERE EXTRACT(YEAR FROM "Fecha_Venta") = {year} 
                    AND EXTRACT(MONTH FROM "Fecha_Venta") = {mes}''')
        total = cur.fetchone()[0]
        total_pages = ceil(total / per_page)

        cur.execute(f'''SELECT * FROM "Ventas" WHERE 
                    EXTRACT(YEAR FROM "Fecha_Venta") = {year} AND 
                    EXTRACT(MONTH FROM "Fecha_Venta") = {mes}
                    ORDER BY "Fecha_Venta" ASC
                    LIMIT {per_page} OFFSET {offset}''')
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

        cur.execute('''SELECT * FROM "Medio_Pago"''')
        medios_pago = cur.fetchall()

        cur.execute('''SELECT * FROM "Mesas"''')
        mesas = cur.fetchall()

        cur.execute('''SELECT m."Id_mesero", e."Nombre" FROM "Mesero" m
                    JOIN "Empleados" e ON m."Id_mesero" = e."Id_empleado"''')
        meseros = cur.fetchall()

        cur.execute('''SELECT * FROM "Consumibles"''')
        consumibles = cur.fetchall()

        cur.close()
        conn.close()

        meseros_dict = {mesero[0]: mesero[1] for mesero in meseros}
        medios_pago_dict = {medio[0]: medio[1] for medio in medios_pago}
        mesas_dict = {mesa[0]: mesa[1] for mesa in mesas}

        return render_template(
            'ventas_realizadas.html',
            data=data,
            page=page,
            total_pages=total_pages,
            action=accion,
            medios_pago=medios_pago,
            medios_pago_dict=medios_pago_dict,
            meseros=meseros,
            meseros_dict=meseros_dict,
            mesas=mesas,
            mesas_dict=mesas_dict,
            consumibles=consumibles,
            years=years,
            meses=meses,
            year_actual=year,
            mes_actual=mes
        )
    except Exception as e:
        return f"Error en ventas: {e}"

@app.route("/ingredientes/<string:accion>")
def ingredientes(accion):
    try:
        page = int(request.args.get('page', 1))
        per_page = 25
        offset = (page - 1) * per_page

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
        cur.execute(f'''SELECT COUNT(*) FROM "Ingredientes_Usados"
                    WHERE EXTRACT(YEAR FROM "Fecha_uso") = {year} 
                    AND EXTRACT(MONTH FROM "Fecha_uso") = {mes}''')
        total = cur.fetchone()[0]
        total_pages = ceil(total / per_page)

        cur.execute(f'''SELECT * FROM "Ingredientes_Usados" WHERE 
                    EXTRACT(YEAR FROM "Fecha_uso") = {year} AND 
                    EXTRACT(MONTH FROM "Fecha_uso") = {mes}
                    ORDER BY "Fecha_uso" ASC
                    LIMIT {per_page} OFFSET {offset}''')
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

        cur.close()
        conn.close()

        consumibles_dict = {consumible[0]: consumible[1] for consumible in consumibles}
        ingredientes_dict = {ingrediente[0]: ingrediente[1] for ingrediente in ingredientes}
        cocineros_dict = {cocinero[0]: cocinero[1] for cocinero in cocineros}

        return render_template(
            'ingredientes_usados.html', 
            data=data, 
            page=page,
            total_pages=total_pages,
            action=accion, 
            ingredientes=ingredientes,
            ingredientes_dict=ingredientes_dict,
            consumibles=consumibles, 
            consumibles_dict=consumibles_dict,
            cocineros=cocineros,
            cocineros_dict=cocineros_dict,
            years=years,
            meses=meses,
            year_actual=year,
            mes_actual=mes
            )
    except Exception as e:
        return f"Error en ingredientes: {e}"

@app.route('/limpiar_tablas', methods=['POST'])
def limpiar_tablas():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="sistema_restaurante_transaccional",
            user="usuario_restaurante_transaccional",
            password="1234"
        )
        cur = conn.cursor()
        cur.execute('DELETE FROM "Consumibles_Vendidos"')
        cur.execute('DELETE FROM "Ingredientes_Usados"')
        cur.execute('DELETE FROM "reservas"')
        cur.execute('DELETE FROM "Ventas"')
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error al limpiar tablas: {e}"

# Reservas
@app.route('/reserva/create', methods=['POST'])
def create_reserva_route():
    try:
        return create_reserva()
    except Exception as e:
        return f"Error al crear reserva: {e}"

@app.route('/reserva/update', methods=['POST'])
def update_reserva_route():
    try:
        return update_reserva()
    except Exception as e:
        return f"Error al actualizar reserva: {e}"

@app.route('/reserva/delete', methods=['POST'])
def delete_reserva_route():
    try:
        return delete_reserva()
    except Exception as e:
        return f"Error al eliminar reserva: {e}"

# Ventas
@app.route('/ventas/create', methods=['POST'])
def create_ventas_route():
    try:
        return create_ventas()
    except Exception as e:
        return f"Error al crear venta: {e}"

@app.route('/ventas/update', methods=['POST'])
def update_ventas_route():
    try:
        return update_ventas()
    except Exception as e:
        return f"Error al actualizar venta: {e}"

@app.route('/ventas/delete', methods=['POST'])
def delete_ventas_route():
    try:
        return delete_ventas()
    except Exception as e:
        return f"Error al eliminar venta: {e}"

# Ingredientes
@app.route('/ingredientes/create', methods=['POST'])
def create_ingredientes_route():
    try:
        return create_ingredientes()
    except Exception as e:
        return f"Error al crear ingrediente: {e}"

@app.route('/ingredientes/update', methods=['POST'])
def update_ingredientes_route():
    try:
        return update_ingredientes()
    except Exception as e:
        return f"Error al actualizar ingrediente: {e}"

@app.route('/ingredientes/delete', methods=['POST'])
def delete_ingredientes_route():
    try:
        return delete_ingredientes()
    except Exception as e:
        return f"Error al eliminar ingrediente: {e}"
    

@app.route('/graficos/<path:filename>')
def graficos_estaticos(filename):
    try:
        return graficos_static(filename)
    except Exception as e:
        return f"Error al eliminar ingrediente: {e}"

@app.route('/analisis')
def analisis():
    try:
        return mostrar_graficos()
    except Exception as e:
        return f"Error al mostrar análisis: {e}"

app.register_blueprint(carga_datos_bp)

def nombre_mes(numero):
    nombres = [
        '', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ]
    return nombres[int(numero)]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
