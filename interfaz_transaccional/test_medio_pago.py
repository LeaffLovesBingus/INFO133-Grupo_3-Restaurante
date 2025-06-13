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
    cur.execute('''SELECT * FROM "Medio_Pago"''')

    # Fetch the data
    data = cur.fetchall()

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template('index.html', data=data)

@app.route('/create', methods=['POST'])

def create():
    conn = psycopg2.connect(
        host="localhost",
        database="sistema_restaurante",
        user="usuario_restaurante",
        password="1234"
    )
    cur = conn.cursor()
    name = request.form['name']
    cur.execute(
        '''INSERT INTO "Medio_Pago" ("Medio_Pago") VALUES (%s)''',
        (name,)
    )
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])

def update():
    conn = psycopg2.connect(
        host="localhost",
        database="sistema_restaurante",
        user="usuario_restaurante",
        password="1234"
    )
    cur = conn.cursor()
    name = request.form['name']
    id = request.form['id']
    cur.execute(
        '''UPDATE "Medio_Pago" SET "Medio_Pago"=%s WHERE "Id_Medio_Pago"=%s''',
        (name, id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])

def delete():
    conn = psycopg2.connect(
    host="localhost",
    database="sistema_restaurante",
    user="usuario_restaurante",
    password="1234"
    )

    cur = conn.cursor()

    # Get the data from the form
    id = request.form['id']

    # Delete the data from the table
    cur.execute('''DELETE FROM "Medio_Pago" WHERE "Id_Medio_Pago"=%s''', (id,))

    # commit the changes
    conn.commit()

    # close the cursor and connection
    cur.close()
    conn.close()

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
