import psycopg2
from flask import Flask, render_template, request, redirect, url_for

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
    return redirect(url_for('medio_pago', action='add'))

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
    return redirect(url_for('medio_pago', action='modificar'))

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

    return redirect(url_for('medio_pago', action='eliminar'))