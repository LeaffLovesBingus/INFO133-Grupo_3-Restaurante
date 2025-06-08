from flask import request, redirect, url_for
import psycopg2

def create():
    conn = psycopg2.connect(
    host="localhost",
    database="sistema_restaurante",
    user="usuario_restaurante",
    password="1234"
    )

    cur = conn.cursor()

    # Get the data from the form
    name = request.form['name']

    # Insert the data into the table
    cur.execute(
        '''INSERT INTO "Medio_Pago""" \
        (name) VALUES (%s)''',
        (name))

    # commit the changes
    conn.commit()

    # close the cursor and connection
    cur.close()
    conn.close()

    return redirect(url_for('index'))

def update():
    conn = psycopg2.connect(
    host="localhost",
    database="sistema_restaurante",
    user="usuario_restaurante",
    password="1234"
    )

    cur = conn.cursor()

    # Get the data from the form
    name = request.form['name']
    id = request.form['id']

    # Update the data in the table
    cur.execute(
        '''UPDATE ""Medio_Pago"" SET name=%s,\
        WHERE id=%s''', (name, id))

    # commit the changes
    conn.commit()
    return redirect(url_for('index'))

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
    cur.execute('''DELETE FROM "Medio_Pago" WHERE id=%s''', (id,))

    # commit the changes
    conn.commit()

    # close the cursor and connection
    cur.close()
    conn.close()

    return redirect(url_for('index'))