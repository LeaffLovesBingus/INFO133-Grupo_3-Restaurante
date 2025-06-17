from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import psycopg2

app = Flask(__name__)

@app.route("/")

def index():
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

    return render_template('ventas.html', data=data, medios_pago=medios_pago)

@app.route('/create', methods=['POST'])

def create():
    conn = psycopg2.connect(
        host="localhost",
        database="sistema_restaurante",
        user="usuario_restaurante",
        password="1234"
    )
    cur = conn.cursor()
    
    ...

    cur.close()
    conn.close()
    return redirect(url_for('ventas'))

@app.route('/update', methods=['POST'])

def update():
    conn = psycopg2.connect(
        host="localhost",
        database="sistema_restaurante",
        user="usuario_restaurante",
        password="1234"
    )
    cur = conn.cursor()
    
    ...

    cur.close()
    conn.close()
    return redirect(url_for('ventas'))

@app.route('/delete', methods=['POST'])

def delete():
    conn = psycopg2.connect(
    host="localhost",
    database="sistema_restaurante",
    user="usuario_restaurante",
    password="1234"
    )

    cur = conn.cursor()

    ...

    cur.close()
    conn.close()

    return redirect(url_for('ventas'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
