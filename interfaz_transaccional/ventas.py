from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import psycopg2
import json

app = Flask(__name__)

@app.route("/")
def index():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="sistema_restaurante_transaccional",
            user="usuario_restaurante_transaccional",
            password="1234"
        )
        cur = conn.cursor()
        cur.execute('''SELECT * FROM "Ventas"''')
        data = cur.fetchall()
        cur.execute('''SELECT * FROM "Medio_Pago"''')
        medios_pago = cur.fetchall()
        data = [
            row[:4] + (datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S"),) + row[5:]
            if isinstance(row[4], str) else row
            for row in data
        ]
        cur.close()
        conn.close()
        return render_template('ventas_realizadas.html', data=data, medios_pago=medios_pago)
    except Exception as e:
        return f"Error al cargar ventas: {e}"

@app.route('/create', methods=['POST'])
def create():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="sistema_restaurante_transaccional",
            user="usuario_restaurante_transaccional",
            password="1234"
        )
        cur = conn.cursor()
        cantidad_productos = request.form["cantidad_productos"]
        monto_total = request.form["monto_total"]
        fecha_venta = request.form["fecha_venta"]
        id_mesero = request.form["id_mesero"]
        id_mesa = request.form["id_mesa"]
        id_medio_pago = request.form["id_medio_pago"]
        cur.execute(
            '''
            INSERT INTO "Ventas" ("Cantidad_Productos", "Monto_Total", "Fecha_Venta", "FK_Id_Mesero", "FK_Id_Mesa", "FK_Id_Medio_Pago")
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING "Id_Venta"
            ''',
            (cantidad_productos, monto_total, fecha_venta, id_mesero, id_mesa, id_medio_pago)
        )
        id_venta = cur.fetchone()[0]
        conn.commit()
        boleta_json = request.form.get("boleta_json")
        boleta = json.loads(boleta_json) if boleta_json else []
        print("Boleta recibida:", boleta)
        for item in boleta:
            cur.execute('''INSERT INTO "Consumibles_Vendidos" 
                        ("FK_Id_Venta", 
                        "FK_Id_Consumible", 
                        "Cantidad")
                        VALUES (%s, %s, %s)''',
                        (id_venta, item['id'], item['cantidad']))
            conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('ventas', accion='add'))
    except Exception as e:
        return f"Error al crear venta: {e}"

@app.route('/update', methods=['POST'])
def update():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="sistema_restaurante_transaccional",
            user="usuario_restaurante_transaccional",
            password="1234"
        )
        cur = conn.cursor()
        cantidad_productos = request.form["cantidad_productos"]
        monto_total = request.form["monto_total"]
        fecha_venta = request.form["fecha_venta"]
        id_mesero = request.form["id_mesero"]
        id_mesa = request.form["id_mesa"]
        id_medio_pago = request.form["id_medio_pago"]
        id_venta = request.form["id"]
        cur.execute(
            '''
            UPDATE "Ventas" 
            SET "Cantidad_Productos" = %s,
                "Monto_Total" = %s, 
                "Fecha_Venta" = %s, 
                "FK_Id_Mesero" = %s, 
                "FK_Id_Mesa" = %s, 
                "FK_Id_Medio_Pago" = %s
            WHERE "Id_Venta" = %s
            ''',
            (cantidad_productos, monto_total, fecha_venta, id_mesero, id_mesa, id_medio_pago, id_venta)
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('ventas', accion='modificar'))
    except Exception as e:
        return f"Error al actualizar venta: {e}"

@app.route('/delete', methods=['POST'])
def delete():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="sistema_restaurante_transaccional",
            user="usuario_restaurante_transaccional",
            password="1234"
        )
        cur = conn.cursor()
        id_venta = request.form["id"]
        
        cur.execute(
            '''
            DELETE FROM "Consumibles_Vendidos"
            WHERE "FK_Id_Venta" = %s
            ''',
            (id_venta,)
        )

        cur.execute(
            '''
            DELETE FROM "Ventas"
            WHERE "Id_Venta" = %s
            ''',
            (id_venta,)
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('ventas', accion='eliminar'))
    except Exception as e:
        return f"Error al eliminar venta: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
