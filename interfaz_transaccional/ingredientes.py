from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
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
        cur.execute('''SELECT * FROM "Ingredientes_Usados"''')
        data = cur.fetchall()
        data = [
            row[:4] + (datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S"),) + row[5:]
            if isinstance(row[4], str) else row
            for row in data
        ]
        cur.close()
        conn.close()
        return render_template('ingredientes.html', data=data)
    except Exception as e:
        return f"Error al cargar ingredientes usados: {e}"

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
        id_consumible = request.form["id_consumible"]
        id_ingrediente = request.form["id_ingrediente"]
        cantidad = request.form["cantidad"]
        fecha = request.form["fecha"]
        id_cocinero = request.form["id_cocinero"]
        cur.execute(
            '''      
            INSERT INTO "Ingredientes_Usados" ("FK_Id_consumible", "FK_Id_ingrediente", "Cantidad", "Fecha_uso", "FK_Id_cocinero")
            VALUES (%s, %s, %s, %s, %s)
            ''',
            (id_consumible, id_ingrediente, cantidad, fecha, id_cocinero)
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('ingredientes', accion='add'))
    except Exception as e:
        return f"Error al crear ingrediente usado: {e}"

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
        id_consumible = request.form["id_consumible"]
        id_ingrediente = request.form["id_ingrediente"]
        cantidad = request.form["cantidad"]
        fecha = request.form["fecha"]
        id_cocinero = request.form["id_cocinero"]
        id_ingrediente_usado = request.form["id"]
        cur.execute(
            '''
            UPDATE "Ingredientes_Usados"
            SET "FK_Id_consumible" = %s,
                "FK_Id_ingrediente" = %s,
                "Cantidad" = %s,
                "Fecha_uso" = %s,
                "FK_Id_cocinero" = %s
            WHERE "Id_Ingredientes_Usados" = %s
            ''',
            (id_consumible, id_ingrediente, cantidad, fecha, id_cocinero, id_ingrediente_usado)
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('ingredientes', accion='modificar'))
    except Exception as e:
        return f"Error al actualizar ingrediente usado: {e}"

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
        id_ingrediente_usado = request.form["id"]
        cur.execute(
            '''
            DELETE FROM "Ingredientes_Usados"
            WHERE "Id_Ingredientes_Usados" = %s
            ''',
            (id_ingrediente_usado,)
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('ingredientes', accion='eliminar'))
    except Exception as e:
        return f"Error al eliminar ingrediente usado: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
