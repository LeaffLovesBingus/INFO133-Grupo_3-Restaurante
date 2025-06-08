from flask import Flask, render_template
import psycopg2
from consultas import *

app = Flask(__name__)

@app.route("/")
@app.route('/create', methods=['POST'])
@app.route('/update', methods=['POST'])
@app.route('/delete', methods=['POST'])

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
    cur.execute('''SELECT * FROM "Medio_Pago"''')

    # Fetch the data
    data = cur.fetchall()

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template('index.html', data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
