from flask import Flask, render_template, request, redirect, url_for
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

    # Fetch the data
    data = cur.fetchall()

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template('index.html', data=data)

@app.route("/ventas", methods=["GET", "POST"])

def ventas():
    if request.method == "POST":
        producto = request.form["producto"]
        cantidad = request.form["cantidad"]
        precio = request.form["precio"]

        # Aquí podrías agregar la lógica para guardar la venta en la base de datos
        # Por ejemplo, usando psycopg2 para conectarte a PostgreSQL

        return redirect(url_for("index"))

    return render_template("ventas.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)