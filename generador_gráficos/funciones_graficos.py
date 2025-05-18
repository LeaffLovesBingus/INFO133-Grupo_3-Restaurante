from sqlalchemy import create_engine
import pandas as pd
import numpy as np
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
        plt.savefig(f'gráficos/{año}/grafico_numero_ventas_{año}_por_mes.png')
        plt.close()
        
    except Exception as e:
        print(f"# Error al graficar número de ventas por mes\nDetalle -> {e}")
    

def graficar_total_ventas_por_mes(año:int) -> None:
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
        plt.savefig(f'gráficos/{año}/grafico_total_ventas_{año}_por_mes.png')
        plt.close()
        
    except Exception as e:
        print(f"# Error al graficar ventas por año\nDetalle -> {e}")


def graficar_ventas_consumibles(año:int) -> None:
    # Genera un gráfico de barras con el consumible más vendido por mes

    try:
        # Conexión a la base de datos
        engine = create_engine('postgresql+psycopg2://usuario_restaurante:1234@localhost/sistema_restaurante')

        # Consulta SQL: para cada mes, el consumible más vendido
        query = f"""
        SELECT 
            EXTRACT(MONTH FROM hv."Fecha_Venta") AS mes, 
            c."Nombre" AS nombre_consumible, 
            SUM(cv."Cantidad") AS total_vendido
        FROM "Hechos_Ventas" hv
        JOIN "Consumibles_Vendidos" cv ON hv."Id_Venta" = cv."FK_Id_Venta"
        JOIN "Consumibles" c ON cv."FK_Id_Consumible" = c."Id_consumibles"
        WHERE EXTRACT(YEAR FROM hv."Fecha_Venta") = {año}
        GROUP BY mes, c."Nombre"
        ORDER BY mes, c."Nombre";
        """
        # Transformar query a dataframe, clasificando mes y ordenando
        df = pd.read_sql_query(query, engine)
        df['mes'] = df['mes'].astype(int)
        df['mes_nombre'] = df['mes'].apply(clasificar_mes)
        df = df.sort_values('mes')

        # Pivotear el DataFrame: filas=mes, Columnas=consumible, valores=total_vendido
        df_pivot = df.pivot(index='mes_nombre', 
                            columns='nombre_consumible', 
                            values='total_vendido').fillna(0)
        
        meses_orden = [clasificar_mes(i) for i in range(1, 13)]
        df_pivot = df_pivot.reindex(meses_orden).fillna(0)

        # Graficar
        # Graficar
        plt.figure(figsize=(12, 7))
        for consumible in df_pivot.columns:
            plt.plot(df_pivot.index, df_pivot[consumible], marker='o', label=consumible)
        plt.title(f'Análisis Ventas Consumibles, Año {año}')
        plt.xlabel('Mes')
        plt.ylabel('Cantidad Vendida')
        plt.xticks(rotation=45)
        plt.legend(title='Consumible')
        plt.yticks(np.arange(0, df_pivot.values.max() + 1, 1))
        plt.tight_layout()
        plt.savefig(f'gráficos/{año}/grafico_ventas_consumibles_{año}.png')
        plt.close()

    except Exception as e:
        print(f"# Error al graficar consumible más vendido por mes\nDetalle -> {e}")

# Graficar ventas por mesero por mes por año
def ventas_por_mesero_por_mes(año: int):
    ...  

# Graficar que ingrediente se usa más por mes
def ingrediende_mas_usado_por_mes(año: int):
    ...

# Graficar que cocinero usa más ingredientes por mes
def ingredientes_por_cocinero_por_mes(año: int):
    ...

# Graficar que numero de ingredientes usados por mes
def numero_ingredientes_usados_por_mes(año: int):
    ...

def ventas_realizadas_mesero_por_año(año: int):
# Genera un gráfico de torta con los porcentajes de las ventas realizadas por los meseros
    try:
        # Conexión a la base de datos
        engine = create_engine('postgresql+psycopg2://usuario_restaurante:1234@localhost/sistema_restaurante')

        # Consulta SQL obtener ventas por mesero
        query = f"""
        SELECT m."Nombre" || ' ' || m."Apellido" as nombre_mesero,
        COUNT(*) as total_ventas
        FROM "Hechos_Ventas" hv
        JOIN "Mesero" m ON hv."FK_Id_Mesero" = m."Id_mesero"
        WHERE EXTRACT(YEAR FROM hv."Fecha_Venta") = {año}
        GROUP BY nombre_mesero
        ORDER BY total_ventas DESC;
        """

        df = pd.read_sql_query(query, engine)

        plt.figure(figsize=(8, 8))
        plt.pie(df['total_ventas'], labels=df['nombre_mesero'], autopct='%1.0f%%')
        plt.title(f"Porcentaje Ventas por Mesero, Año {año}")
        plt.tight_layout()
        plt.savefig(f'gráficos/{año}/grafico_porcentaje_ventas_realizadas_meseros_{año}.png')
        plt.close()
    except Exception as e:
        print(f'# Error al graficar porcentaje ventas por mesero\nDetalle -> {e}')


def total_ventas_mesero_por_año(año: int):
# Genera un gráfico de torta con los porcentajes de los montos totales de las ventas realizadas por los meseros
    try:
        # Conexión a la base de datos
        engine = create_engine('postgresql+psycopg2://usuario_restaurante:1234@localhost/sistema_restaurante')

        # Consulta SQL obtener ventas por mesero
        query = f"""
        SELECT m."Nombre" || ' ' || m."Apellido" as nombre_mesero,
        SUM (hv."Monto_Total") as total_ventas
        FROM "Hechos_Ventas" hv
        JOIN "Mesero" m ON hv."FK_Id_Mesero" = m."Id_mesero"
        WHERE EXTRACT(YEAR FROM hv."Fecha_Venta") = {año}
        GROUP BY nombre_mesero
        ORDER BY total_ventas DESC;
        """

        df = pd.read_sql_query(query, engine)

        plt.figure(figsize=(8, 8))
        plt.pie(df['total_ventas'], labels=df['nombre_mesero'], autopct='%1.0f%%')
        plt.title(f"Porcentaje Ventas por Mesero, Año {año}")
        plt.tight_layout()
        plt.savefig(f'gráficos/{año}/grafico_porcentaje_total_ventas_meseros_{año}.png')
        plt.close()
    except Exception as e:
        print(f'# Error al graficar porcentaje ventas por mesero\nDetalle -> {e}')


def graficar_uso_ingredientes(año:int) -> None:
    # Genera un gráfico de barras con el consumible más vendido por mes

    try:
        # Conexión a la base de datos
        engine = create_engine('postgresql+psycopg2://usuario_restaurante:1234@localhost/sistema_restaurante')

        # Consulta SQL: para cada mes, el consumible más vendido
        query = f"""
        SELECT 
            EXTRACT(MONTH FROM hi."Fecha_uso") AS mes, 
            i."Nombre" AS nombre_ingrediente, 
            SUM(hi."Cantidad") AS total_usado
        FROM "Hechos_Ingredientes_Usados" hi
        JOIN "Ingredientes" i ON hi."FK_Id_ingrediente" = i."Id_ingrediente"
        WHERE EXTRACT(YEAR FROM hi."Fecha_uso") = {año}
        GROUP BY mes, i."Nombre"
        ORDER BY mes, i."Nombre";
        """

        df = pd.read_sql_query(query, engine)
        df['mes'] = df['mes'].astype(int)
        df['mes_nombre'] = df['mes'].apply(clasificar_mes)
        df = df.sort_values('mes')

        # Pivotear el DataFrame: filas=mes, columnas=ingredientes, valores=total_vendido
        df_pivot = df.pivot(index='mes_nombre', 
                            columns='nombre_ingrediente', 
                            values='total_usado').fillna(0)
        
        # Aseguro orden de los meses y pivoteo denuevo
        meses_orden = [clasificar_mes(i) for i in range(1, 13)]
        df_pivot = df_pivot.reindex(meses_orden).fillna(0)

        # Graficar
        plt.figure(figsize=(12, 7))
        for consumible in df_pivot.columns:
            plt.plot(df_pivot.index, df_pivot[consumible], marker='o', label=consumible)
        plt.title(f'Uso Ingredientes por Mes, Año {año}')
        plt.xlabel('Mes')
        plt.ylabel('Cantidad Usado')
        plt.xticks(rotation=45)
        plt.legend(title='Ingrediente')

        plt.yticks(np.arange(0, df_pivot.values.max() + 1, 1))

        plt.tight_layout()
        plt.savefig(f'gráficos/{año}/grafico_uso_ingredientes_{año}.png')
        plt.close()

    except Exception as e:
        print(f"# Error al graficar ventas de todos los consumibles por mes\nDetalle -> {e}")


# Graficar que cocinero usa más ingredientes por año (torta)
def total_uso_ingredientes_por_cocinero(año: int):
    ...


def main():
    año = 2024

    graficar_numero_ventas_por_mes(año)
    graficar_total_ventas_por_mes(año)
    graficar_ventas_consumibles(año)

    print("> Gráficos generados con éxito")

if __name__ == "__main__":
    main()