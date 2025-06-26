import psycopg2
import os
import json
from dotenv import load_dotenv
import psycopg2.extras


def transferir_datos():

    # Cargar las variables de entorno
    load_dotenv(dotenv_path="./credenciales.env")

    # Cargar las queries para transferir las tablas
    with open("./ETL/queries.json", 'r', encoding="utf-8") as f:
        queries = json.load(f)

    try:
        # Crear las conexiones a las bases de datos
        conn_transaccional = psycopg2.connect(
            host="localhost",
            database=os.getenv("CONEXION_TRANSACCIONAL"),
            user=os.getenv("USUARIO_TRANSACCIONAL"),
            password=os.getenv("CLAVE")
        )
        curr_transaccional = conn_transaccional.cursor()
        
        conn_estrella = psycopg2.connect(
            host="localhost",
            database=os.getenv("CONEXION_ESTRELLA"),
            user=os.getenv("USUARIO_ESTRELLA"),
            password=os.getenv("CLAVE")
        )
        curr_estrella = conn_estrella.cursor()

        # Transferir datos de la tabla de meseros
        curr_transaccional.execute(queries["tr_mesero"])
        meseros = curr_transaccional.fetchall()
        psycopg2.extras.execute_values(curr_estrella, queries["est_mesero"], meseros)
        conn_estrella.commit()
        del meseros

        # Transferir datos de la tabla de cocineros
        curr_transaccional.execute(queries["tr_cocinero"])
        cocineros = curr_transaccional.fetchall()
        psycopg2.extras.execute_values(curr_estrella, queries["est_cocinero"], cocineros)
        conn_estrella.commit()
        del cocineros

        # Transferir datos de la tabla de consumibles
        curr_transaccional.execute(queries["tr_consumibles"])
        consumibles = curr_transaccional.fetchall()
        psycopg2.extras.execute_values(curr_estrella, queries["est_consumibles"], consumibles)
        conn_estrella.commit()
        del consumibles

        # Transferir datos de la tabla de medios de pago
        curr_transaccional.execute(queries["tr_mediopago"])
        mediopago = curr_transaccional.fetchall()
        psycopg2.extras.execute_values(curr_estrella, queries["est_mediopago"], mediopago)
        conn_estrella.commit()
        del mediopago

        # Transferir datos de la tabla de ingredientes
        curr_transaccional.execute(queries["tr_ingredientes"])
        ingredientes = curr_transaccional.fetchall()
        psycopg2.extras.execute_values(curr_estrella, queries["est_ingredientes"], ingredientes)
        conn_estrella.commit()
        del ingredientes

        # Transferir datos de la tabla de ingredientes usados
        curr_transaccional.execute(queries["tr_ingredientesusados"])
        ingredientes_usados = curr_transaccional.fetchall()
        psycopg2.extras.execute_values(curr_estrella, queries["est_ingredientesusados"], ingredientes_usados)
        conn_estrella.commit()
        del ingredientes_usados
        
        # Transferir datos de la tabla de ventas
        curr_transaccional.execute(queries["tr_ventas"])
        ventas = curr_transaccional.fetchall()
        psycopg2.extras.execute_values(curr_estrella, queries["est_ventas"], ventas)
        conn_estrella.commit()
        del ventas

        # Transferir datos de la tabla de consumibles vendidos
        curr_transaccional.execute(queries["tr_consumiblesvendidos"])
        consumibles_vendidos = curr_transaccional.fetchall()
        psycopg2.extras.execute_values(curr_estrella, queries["est_consumiblesvendidos"], consumibles_vendidos)
        conn_estrella.commit()
        del consumibles_vendidos


        curr_transaccional.close()
        curr_estrella.close()
        conn_transaccional.close()
        conn_estrella.close()

    except Exception as e:
        print(f"ETL: Error en rellenar tablas\n> {e}")
        curr_transaccional.close()
        curr_estrella.close()
        conn_transaccional.close()
        conn_estrella.close()


def vaciar_tablas():
    load_dotenv(dotenv_path="./credenciales.env")

    try:
        conn_estrella = psycopg2.connect(
            host="localhost",
            database=os.getenv("CONEXION_ESTRELLA"),
            user=os.getenv("USUARIO_ESTRELLA"),
            password=os.getenv("CLAVE")
        )
        curr_estrella = conn_estrella.cursor()

        # Obtener los nombres de todas las tablas en la base de datos
        curr_estrella.execute(
        """
            SELECT tables.table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """)
        tablas = curr_estrella.fetchall()

        # Vaciar todas las tablas
        for tabla in tablas:
            nombre_tabla = tabla[0]
            try:
                curr_estrella.execute(f"TRUNCATE TABLE \"{nombre_tabla}\" CASCADE;")
            except Exception as e:
                print(f"ETL: No se pudo vaciar la tabla {nombre_tabla}\nDetalle: {e}")

        conn_estrella.commit()

        curr_estrella.close()
        conn_estrella.close()

    except Exception as e:
        print(f"ETL: Error en vaciar tablas\n> {e}")
        curr_estrella.close()
        conn_estrella.close()

# Testeo
def main():
    transferir_datos()
    vaciar_tablas()


if __name__ == "__main__":
    main()