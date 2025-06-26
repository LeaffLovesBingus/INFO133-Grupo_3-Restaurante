import psycopg2
from getpass import getpass
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./credenciales.env")

def crear_sistema_restaurantes():
    '''
    Crea la base de datos 'sistema_restaurante' y luego a su usuario 'usuario_restaurante' 
    junto con sus permisos.
    '''
    try:
        conn.set_session(autocommit=True)

        # Crear la base de datos
        cur.execute("CREATE DATABASE sistema_restaurante;")

        # Crear el usuario para la base de datos
        cur.execute("CREATE USER usuario_restaurante WITH PASSWORD %s;", (os.getenv("CLAVE"),))
        cur.execute("GRANT CONNECT ON DATABASE sistema_restaurante TO usuario_restaurante;")

        print("> Base de datos sistema_restaurante creada")
        print("> Usuario creado exitosamente")

        conn.set_session(autocommit=False)

        # Conectarse a la nueva base de datos
        conn_sr = psycopg2.connect(
            database="sistema_restaurante",
            user="postgres",
            password=clave,
            host="localhost"
        )
        cur_sr = conn_sr.cursor()

        # Otorgar permisos a usuario_restaurante
        cur_sr.execute("GRANT USAGE ON SCHEMA public TO usuario_restaurante;")
        cur_sr.execute("GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA public TO usuario_restaurante;")
        cur_sr.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON TABLES TO usuario_restaurante;")
        conn_sr.commit()
        print("> Permisos para usuario_restaurante concedidos con éxito")

        # Cerrar conexión de postgres a sistema_restaurante
        cur_sr.close()
        conn_sr.close()

    except Exception as e:
        conn.rollback()
        print(f"# Error con la creación de sistema_restaurantes\nDetalle -> {e}")


def crear_esquema_bd():
    '''
    Crea el esquema de la base de datos de análisis del sistema de restaurantes\n
    Tener el archivo RestaurantDB.sql en la misma carpeta que este script python pls\n
    Link dbdiagram: https://dbdiagram.io/d/RestaurantDB-V2-0-6818e8e31ca52373f588d4c4
    '''
    script = True

    try:
        conn_sr = psycopg2.connect(
            database="sistema_restaurante",
            user="postgres",
            password=clave,
            host="localhost"
        )
        cur_sr = conn_sr.cursor()
        print("> postgres conectado con éxito a sistema_restaurante")
    except Exception as e:
        script = False
        print(f"# Error al conectar a sistema_restaurante\nDetalle -> {e}")
    
    if script:
        try:
            with open("ETL/db_estrella/db_estrella.sql", 'r', encoding="utf-8") as f:
                script_modelo = f.read()
            
            for statement in script_modelo.split(';'):
                stmt = statement.strip()
                if stmt:
                    cur_sr.execute(stmt + ';')

            conn_sr.commit()
            print("> Modelo de base de datos creado con éxito")

        except Exception as e:
            conn_sr.rollback()
            print(f"# Error con la creación del esquema\nDetalle -> {e}")
        
        cur_sr.close()
        conn_sr.close()



if __name__ == "__main__":
    # Conexión a postgres en ámbito global
    clave = getpass("Ingrese su contraseña del usuario postgres: ")
    try: 
        conn = psycopg2.connect(
            database="postgres",
            user="postgres",
            password=clave,
            host="localhost"
        )
        cur = conn.cursor()
        
        crear_sistema_restaurantes()
        crear_esquema_bd()
        
        cur.close()
        conn.close()

    except Exception as e:
        print(f"# Fallo de conexión\nDetalle: {e}")