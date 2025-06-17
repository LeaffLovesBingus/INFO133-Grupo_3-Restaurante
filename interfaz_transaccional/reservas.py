from flask import Flask, render_template, request, redirect, url_for
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
    cur.execute('''SELECT * FROM "reservas"''')

    # Fetch the data
    data = cur.fetchall()

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template('reservas_mesas.html', data=data)

@app.route('/create', methods=['POST'])

def create():
    conn = psycopg2.connect(
        host="localhost",
        database="sistema_restaurante_transaccional",
        user="usuario_restaurante_transaccional",
        password="1234"
    )
    cur = conn.cursor()

    # Llamar a los inputs del html
    id_mesa = request.form["id_mesa"]
    estado = request.form["estado_reserva"]
    fecha = request.form["fecha_reserva"]
    nombre = request.form["nombre_cliente"]
    telefono = request.form["telefono_cliente"]
    
    # Crear en la base de datos
    cur.execute(
        '''
        INSERT INTO "reservas" ("FK_id_mesas", "estado_reserva", "fecha_reserva", "nombre_cliente", "telefono_cliente") 
        VALUES (%s, %s, %s, %s, %s)
        ''',
        (id_mesa, estado, fecha, nombre, telefono)
    )

    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('reservas', action='add'))

@app.route('/update', methods=['POST'])

def update():
    conn = psycopg2.connect(
        host="localhost",
        database="sistema_restaurante_transaccional",
        user="usuario_restaurante_transaccional",
        password="1234"
    )
    cur = conn.cursor()
    
    # Llamar a los inputs del html
    id_reserva = request.form["id"]
    id_mesa = request.form["id_mesa"]
    estado = request.form["estado_reserva"]
    fecha = request.form["fecha_reserva"]
    nombre = request.form["nombre_cliente"]
    telefono = request.form["telefono_cliente"]

    # Actualizar la base de datos
    cur.execute(
        '''
        UPDATE "reservas"
        SET "FK_id_mesas" = %s,
            "estado_reserva" = %s,
            "fecha_reserva" = %s,
            "nombre_cliente" = %s,
            "telefono_cliente" = %s
        WHERE "PK_id_reservas" = %s
        ''',
        (id_mesa, estado, fecha, nombre, telefono, id_reserva)
    )

    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('reservas', action='modificar'))

@app.route('/delete', methods=['POST'])

def delete():
    conn = psycopg2.connect(
    host="localhost",
    database="sistema_restaurante_transaccional",
    user="usuario_restaurante_transaccional",
    password="1234"
    )

    cur = conn.cursor()

    # Llamar a los inputs del html
    id_reserva = request.form["id"]

    # Ejecutar el delete
    cur.execute(
        '''
        DELETE FROM "reservas" 
        WHERE "PK_id_reservas" = %s
        ''',
        (id_reserva,)
    )

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('reservas', action='eliminar'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
