from flask import Flask, render_template, request, redirect, url_for
import psycopg2

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
        cur.execute('''SELECT * FROM "reservas"''')
        data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('reservas_mesas.html', data=data)
    except Exception as e:
        return f"Error al cargar reservas: {e}"

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
        id_mesa = request.form["id_mesa"]
        estado = request.form["estado_reserva"]
        fecha = request.form["fecha_reserva"]
        nombre = request.form["nombre_cliente"]
        telefono = request.form["telefono_cliente"]
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
    except Exception as e:
        return f"Error al crear reserva: {e}"

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
        id_reserva = request.form["id"]
        id_mesa = request.form["id_mesa"]
        estado = request.form["estado_reserva"]
        fecha = request.form["fecha_reserva"]
        nombre = request.form["nombre_cliente"]
        telefono = request.form["telefono_cliente"]
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
    except Exception as e:
        return f"Error al actualizar reserva: {e}"

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
        id_reserva = request.form["id"]
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
    except Exception as e:
        return f"Error al eliminar reserva: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
