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
    cur.execute('''SELECT * FROM "Ingredientes_Usados"''')

    # Fetch the data
    data = cur.fetchall()

    data = [
        row[:4] + (datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S"),) + row[5:]
        if isinstance(row[4], str) else row
        for row in data
    ]

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template('ingredientes.html', data=data)

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
    id_consumible = request.form["id_consumible"]
    id_ingrediente = request.form["id_ingrediente"]
    cantidad = request.form["cantidad"]
    fecha = request.form["fecha"]
    id_cocinero = request.form["id_cocinero"]

    # Sentencia SQL
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
    id_consumible = request.form["id_consumible"]
    id_ingrediente = request.form["id_ingrediente"]
    cantidad = request.form["cantidad"]
    fecha = request.form["fecha"]
    id_cocinero = request.form["id_cocinero"]
    id_ingrediente_usado = request.form["id"]

    # Sentencia SQL
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

@app.route('/delete', methods=['POST'])

def delete():
    conn = psycopg2.connect(
    host="localhost",
    database="sistema_restaurante_transaccional",
    user="usuario_restaurante_transaccional",
    password="1234"
    )

    cur = conn.cursor()

    # Eliminar por id
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
