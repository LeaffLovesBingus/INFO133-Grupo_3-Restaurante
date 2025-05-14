import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

def graficar_ventas_por_mes():
    '''
    Genera un gráfico de barras con las ventas por mes
    '''
    try:
        # Conexión a la base de datos
        conn = psycopg2.connect(
            database="sistema_restaurante",
            user="usuario_restaurante",
            password="1234",
            host="localhost"
        )
        print("> postgres conectado con éxito")
        
        # Consulta SQL para obtener las ventas por mes
        query = """
        SELECT EXTRACT(MONTH FROM "Fecha_Venta") AS mes, SUM("Monto_Total") AS total_ventas
        FROM "Hechos_Ventas"
        GROUP BY mes
        ORDER BY mes;
        """
        
        # Leer los datos en un DataFrame de pandas
        df = pd.read_sql_query(query, conn)
        
        # Graficar los datos
        plt.figure(figsize=(10, 6))
        plt.bar(df['mes'], df['total_ventas'], color='skyblue')
        plt.title('Ventas por Mes')
        plt.xlabel('Mes')
        plt.ylabel('Total Ventas')
        plt.xticks(df['mes'])
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Mostrar el gráfico
        plt.show()
        
    except Exception as e:
        print(f"# Error al graficar ventas por mes\nDetalle -> {e}")
    
    finally:
        if conn:
            conn.close()
            print("> Conexión cerrada")

def graficar_ventas_por_año(año:int):

    '''
    Genera un gráfico de barras con las ventas por año
    '''
    try:
        # Conexión a la base de datos
        conn = psycopg2.connect(
            database="sistema_restaurante",
            user="usuario_restaurante",
            password="1234",
            host="localhost"
        )
        print("> postgres conectado con éxito")
        
        # Consulta SQL para obtener las ventas por año
        query = f"""
        SELECT EXTRACT(YEAR FROM "Fecha_Venta") AS año, SUM("Monto_Total") AS total_ventas
        FROM "Hechos_Ventas"
        WHERE EXTRACT(YEAR FROM "Fecha_Venta") = {año}
        GROUP BY año;
        """
        
        # Leer los datos en un DataFrame de pandas
        df = pd.read_sql_query(query, conn)
        
        # Graficar los datos
        plt.figure(figsize=(10, 6))
        plt.bar(df['año'], df['total_ventas'], color='skyblue')
        plt.title(f'Ventas por Año: {año}')
        plt.xlabel('Año')
        plt.ylabel('Total Ventas')
        plt.xticks(df['año'])
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Mostrar el gráfico
        plt.show()
        
    except Exception as e:
        print(f"# Error al graficar ventas por año\nDetalle -> {e}")
    
    finally:
        if conn:
            conn.close()
            print("> Conexión cerrada")
    

if __name__ == "__main__":

    try: 
        conn = psycopg2.connect(
            database="sistema_restaurante",
            user="usuario_restaurante",
            password="1234",
            host="localhost"
        )
        print("> postgres conectado con éxito")
    except Exception as e:
        print(f"# Error al conectar a postgres\nDetalle -> {e}")
        conn.close()
        exit()
