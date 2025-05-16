from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt

def clasificar_mes(mes:int) -> str:
    # Clasifica el mes

    meses = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre"
    }

    return meses.get(mes, "Mes no válido")

def graficar_numero_ventas_por_mes(año:int) -> None:
    #Genera un gráfico de barras con el número de ventas por mes

    try:
        # Conexión a la base de datos
        engine = create_engine('postgresql+psycopg2://usuario_restaurante:1234@localhost/sistema_restaurante')
        
        # Consulta SQL para obtener el número de ventas por mes
        query = f"""
        SELECT EXTRACT(MONTH FROM "Fecha_Venta") AS mes, COUNT(*) AS numero_ventas
        FROM "Hechos_Ventas"
        WHERE EXTRACT(YEAR FROM "Fecha_Venta") = {año}
        GROUP BY mes
        ORDER BY mes;
        """
        
        # Leer los datos en un DataFrame de pandas
        engine = create_engine('postgresql+psycopg2://usuario_restaurante:1234@localhost/sistema_restaurante')
        df = pd.read_sql_query(query, engine)
        df['mes'] = df['mes'].apply(clasificar_mes)  # Clasificar los meses
        
        # Graficar los datos
        plt.figure(figsize=(10, 6))
        plt.bar(df['mes'], df['numero_ventas'], color='skyblue')
        plt.title(f'Análisis Número de Ventas Año {año}')
        plt.xlabel('Mes')
        plt.ylabel('Número de Ventas')
        plt.xticks(df['mes'], rotation=45)
        plt.tight_layout()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Guardar el gráfico
        plt.savefig(f'gráficos/grafico_numero_ventas_{año}_por_mes.png')
        plt.close()
        
    except Exception as e:
        print(f"# Error al graficar número de ventas por mes\nDetalle -> {e}")
    

def graficar_ventas_por_año(año:int) -> None:
    #Genera un gráfico de barras con las ventas por año

    try:
        # Conexión a la base de datos
        engine = create_engine('postgresql+psycopg2://usuario_restaurante:1234@localhost/sistema_restaurante')

        # Consulta SQL para obtener las ventas por año
        query = f"""
        SELECT EXTRACT(MONTH FROM "Fecha_Venta") AS mes, SUM("Monto_Total") AS total_ventas
        FROM "Hechos_Ventas"
        WHERE EXTRACT(YEAR FROM "Fecha_Venta") = {año}
        GROUP BY mes
        ORDER BY mes;
        """
        
        # Leer los datos en un DataFrame de pandas
        df = pd.read_sql_query(query, engine)
        df['mes'] = df['mes'].apply(clasificar_mes)  # Clasificar los meses
        
        # Graficar los datos
        plt.figure(figsize=(10, 6))
        plt.bar(df['mes'], df['total_ventas'], color='skyblue')
        plt.title(f'Análisis Monto Total Ventas Año {año}')
        plt.xlabel('Mes')
        plt.ylabel('Total Ventas')
        plt.xticks(df['mes'], rotation=45)
        plt.tight_layout()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Guardar el gráfico
        plt.savefig(f'gráficos/grafico_total_ventas_{año}_por_mes.png')
        plt.close()
        
    except Exception as e:
        print(f"# Error al graficar ventas por año\nDetalle -> {e}")


def graficar_consumible_mas_vendido_por_mes(año:int) -> None:
    # Genera un gráfico de barras con el consumible más vendido por mes

    try:
        # Conexión a la base de datos
        engine = create_engine('postgresql+psycopg2://usuario_restaurante:1234@localhost/sistema_restaurante')

        # Consulta SQL: para cada mes, el consumible más vendido
        query = f"""
        SELECT mes, nombre_consumible, total_vendido FROM (
            SELECT 
                EXTRACT(MONTH FROM hv."Fecha_Venta") AS mes, 
                c."Nombre" AS nombre_consumible, 
                SUM(cv."Cantidad") AS total_vendido,
                ROW_NUMBER() OVER (PARTITION BY EXTRACT(MONTH FROM hv."Fecha_Venta") ORDER BY SUM(cv."Cantidad") DESC) as rn
            FROM "Hechos_Ventas" hv
            JOIN "Consumibles_Vendidos" cv ON hv."Id_Venta" = cv."FK_Id_Venta"
            JOIN "Consumibles" c ON cv."FK_Id_Consumible" = c."Id_consumibles"
            WHERE EXTRACT(YEAR FROM hv."Fecha_Venta") = {año}
            GROUP BY mes, c."Nombre"
        ) t
        WHERE rn = 1
        ORDER BY mes;
        """

        df = pd.read_sql_query(query, engine)
        df['mes_nombre'] = df['mes'].apply(clasificar_mes)

        # Graficar
        plt.figure(figsize=(10, 6))
        plt.bar(df['mes_nombre'], df['total_vendido'], color='skyblue')
        for idx, row in df.iterrows():
            plt.text(idx, row['total_vendido'], row['nombre_consumible'], ha='center', va='bottom', fontsize=9, rotation=0)
        plt.title(f'Análisis Consumible Más Vendido por Mes, Año {año}')
        plt.xlabel('Mes')
        plt.ylabel('Cantidad Vendida')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'gráficos/grafico_consumible_mas_vendido_{año}_por_mes.png')
        plt.close()

    except Exception as e:
        print(f"# Error al graficar consumible más vendido por mes\nDetalle -> {e}")

def main():

    graficar_numero_ventas_por_mes(2024)
    graficar_ventas_por_año(2024)
    graficar_consumible_mas_vendido_por_mes(2024)

    print("> Gráficos generados con éxito")

if __name__ == "__main__":
    main()