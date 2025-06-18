import psycopg2
from getpass import getpass
from datos_random_transaccional import generar_datos
from generar_datos_crud import generarDatosCRUD


def crear_sistema_restaurantes():
    '''
    Crea la base de datos 'sistema_restaurante_transaccional' y luego a su usuario 'usuario_restaurante_transaccional' 
    junto con sus permisos.
    '''
    try:
        conn.set_session(autocommit=True)

        # Crear la base de datos
        cur.execute("CREATE DATABASE sistema_restaurante_transaccional;")

        # Crear el usuario para la base de datos
        cur.execute("CREATE USER usuario_restaurante_transaccional WITH PASSWORD '1234';")
        cur.execute("GRANT CONNECT ON DATABASE sistema_restaurante_transaccional TO usuario_restaurante_transaccional;")

        print("> Base de datos sistema_restaurante_transaccional creada")
        print("> Usuario creado exitosamente\nNombre: usuario_restaurante_transaccional\nContraseña: 1234")

        conn.set_session(autocommit=False)

        # Conectarse a la nueva base de datos
        conn_sr = psycopg2.connect(
            database="sistema_restaurante_transaccional",
            user="postgres",
            password=f"{clave}",
            host="localhost"
        )
        cur_sr = conn_sr.cursor()

        # Otorgar permisos a usuario_restaurante_transaccional
        cur_sr.execute("GRANT USAGE ON SCHEMA public TO usuario_restaurante_transaccional;")
        cur_sr.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO usuario_restaurante_transaccional;")
        cur_sr.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO usuario_restaurante_transaccional;")
        conn_sr.commit()
        print("> Permisos para usuario_restaurante_transaccional concedidos con éxito")

        # Cerrar conexión de postgres a sistema_restaurante_transaccional
        cur_sr.close()
        conn_sr.close()

    except Exception as e:
        conn.rollback()
        print(f"# Error con la creación de sistema_restaurantes\nDetalle -> {e}")


def crear_esquema_bd():
    '''
    Crea el esquema de la base de datos transaccional del sistema de restaurantes\n
    Tener el archivo modelo_transaccional.sql en la misma carpeta que este script python pls\n
    Link dbdiagram: https://dbdiagram.io/d/RestaurantDB-V3-0-684312615a9a94714e3f2843
    '''
    script = True

    try:
        conn_sr = psycopg2.connect(
            database="sistema_restaurante_transaccional",
            user="postgres",
            password=f"{clave}",
            host="localhost"
        )
        cur_sr = conn_sr.cursor()
        print("> postgres conectado con éxito a sistema_restaurante_transaccional")
    except Exception as e:
        script = False
        print(f"# Error al conectar a sistema_restaurante_transaccional\nDetalle -> {e}")
    
    if script:
        try:
            with open("interfaz_transaccional/modelo_db/modelo_transaccional.sql", 'r', encoding="utf-8") as f:
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
            password=f"{clave}",
            host="localhost"
        )
        cur = conn.cursor()
        print(f"> Conexión exitosa\nUser: {conn.info.user}\nBase de datos: {conn.info.dbname}")
        crear_sistema_restaurantes()
        crear_esquema_bd()
        
        cur.close()
        conn.close()

    except Exception as e:
        print(f"# Fallo de conexión\nDetalle: {e}")

    generar_datos()
    generarDatosCRUD()