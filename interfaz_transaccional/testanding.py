from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from medio_pago import create as create_medio_pago, update as update_medio_pago, delete as delete_medio_pago

app = Flask(__name__)

@app.route("/")

def index():
    return render_template(template_name_or_list='index.html')

@app.route('/medio_pago/<string:action>')

def medio_pago(action):

    # Connect to the database
    conn = psycopg2.connect(
        host="localhost",
        database="sistema_restaurante",
        user="usuario_restaurante",
        password="1234"
    )

    # create a cursor
    cur = conn.cursor()

    # Select all products from the table
    cur.execute('''SELECT * FROM "Medio_Pago"''')

    # Fetch the data
    data = cur.fetchall()

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template(template_name_or_list='medio_pago.html', data=data, action=action)

@app.route("/ventas/<string:accion>")

def ventas(accion):
    # Connect to the database
    conn = psycopg2.connect(
    host="localhost",
    database="sistema_restaurante",
    user="usuario_restaurante",
    password="1234"
    )

    # create a cursor
    cur = conn.cursor()

    # Select all products from the table
    cur.execute('''SELECT * FROM "Hechos_Ventas"''')

    # Fetch the data
    data = cur.fetchall()

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template('ventas_realizadas.html', data=data, action=accion)

@app.route("/ingredientes/<string:accion>")

def ingredientes(accion):
    # Connect to the database
    conn = psycopg2.connect(
    host="localhost",
    database="sistema_restaurante",
    user="usuario_restaurante",
    password="1234"
    )

    # create a cursor
    cur = conn.cursor()

    # Select all products from the table
    cur.execute('''SELECT * FROM "Hechos_Ingredientes_Usados"''')

    # Fetch the data
    data = cur.fetchall()

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template('ingredientes_usados.html', data=data, action=accion)


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
