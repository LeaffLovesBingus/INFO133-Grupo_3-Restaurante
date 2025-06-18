from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import psycopg2

app = Flask(__name__)

@app.route("/")

def index():
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

    data = cur.fetchall()

    cur.execute('''SELECT * FROM "Medio_Pago"''')

    medios_pago = cur.fetchall()
    
    data = [
        row[:4] + (datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S"),) + row[5:]
        if isinstance(row[4], str) else row
        for row in data
    ]
    
    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template('ventas_realizadas.html', data=data, medios_pago=medios_pago)

@app.route('/create', methods=['POST'])

def create():
    conn = psycopg2.connect(
        host="localhost",
        database="sistema_restaurante_transaccional",
        user="usuario_restaurante_transaccional",
        password="1234"
    )
    cur = conn.cursor()
    
    # Extraer los datos de la interfaz
    cantidad_productos = request.form["cantidad_productos"]
    monto_total = request.form["monto_total"]
    fecha_venta = request.form["fecha_venta"]
    id_mesero = request.form["id_mesero"]
    id_mesa = request.form["id_mesa"]
    id_medio_pago = request.form["id_medio_pago"]

    # Sentencia SQL para actualizar la tabla de ventas
    cur.execute(
        '''
        INSERT INTO "Ventas" ("Cantidad_Productos", "Monto_Total", "Fecha_Venta", "FK_Id_Mesero", "FK_Id_Mesa", "FK_Id_Medio_Pago")
        VALUES (%s, %s, %s, %s, %s, %s)
        ''',
        (cantidad_productos, monto_total, fecha_venta, id_mesero, id_mesa, id_medio_pago)
    )

    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('ventas', accion='add'))

@app.route('/update', methods=['POST'])

def update():
    conn = psycopg2.connect(
        host="localhost",
        database="sistema_restaurante_transaccional",
        user="usuario_restaurante_transaccional",
        password="1234"
    )
    cur = conn.cursor()
    
    # Extraer los datos de la interfaz
    cantidad_productos = request.form["cantidad_productos"]
    monto_total = request.form["monto_total"]
    fecha_venta = request.form["fecha_venta"]
    id_mesero = request.form["id_mesero"]
    id_mesa = request.form["id_mesa"]
    id_medio_pago = request.form["id_medio_pago"]
    id_venta = request.form["id"]

    # Sentencia SQL para actualizar la tabla ventas
    cur.execute(
        '''
        UPDATE "Ventas" 
        SET "Cantidad_Productos" = %s,
            "Monto_Total" = %s, 
            "Fecha_Venta" = %s, 
            "FK_Id_Mesero" = %s, 
            "FK_Id_Mesa" = %s, 
            "FK_Id_Medio_Pago" = %s
        WHERE Id_Venta = %s
        ''',
        (cantidad_productos, monto_total, fecha_venta, id_mesero, id_mesa, id_medio_pago, id_venta)
    )

    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('ventas', accion='modificar'))

@app.route('/delete', methods=['POST'])

def delete():
    conn = psycopg2.connect(
    host="localhost",
    database="sistema_restaurante_transaccional",
    user="usuario_restaurante_transaccional",
    password="1234"
    )

    cur = conn.cursor()

    # Eliminar elemento por ID
    id_venta = request.form["id"]
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
