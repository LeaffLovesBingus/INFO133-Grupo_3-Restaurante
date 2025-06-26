from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def clasificar_mes(mes:int) -> str:
    meses = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    return meses.get(mes, "Mes no válido")

def graficar_numero_ventas_por_mes(año:int) -> None:
    """Gráfico de barras: Número de ventas por mes"""
    try:
        engine = create_engine('postgresql+psycopg2://usuario_restaurante:1234@localhost/sistema_restaurante')
        query = f"""
        SELECT EXTRACT(MONTH FROM "Fecha_Venta") AS mes, COUNT(*) AS numero_ventas
        FROM "Hechos_Ventas"
        WHERE EXTRACT(YEAR FROM "Fecha_Venta") = {año}
        GROUP BY mes
        ORDER BY mes;
        """
        df = pd.read_sql_query(query, engine)
        df['mes'] = df['mes'].apply(clasificar_mes)
        plt.figure(figsize=(12, 8))
        plt.bar(df['mes'], df['numero_ventas'], color='skyblue')
        plt.title(f'Número de Ventas por Mes - {año}', fontsize=22)
        plt.xlabel('Mes', fontsize=22)
        plt.ylabel('Número de Ventas', fontsize=22)
        plt.xticks(df['mes'], rotation=45, fontsize=18)
        plt.yticks(fontsize=18)
        plt.tight_layout()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        os.makedirs(f'gráficos/{año}', exist_ok=True)
        plt.savefig(f'gráficos/{año}/grafico_numero_ventas_{año}_por_mes.png')
        plt.close()
    except Exception as e:
        print(f"# Error al graficar número de ventas por mes\nDetalle -> {e}")

def graficar_total_ventas_por_mes(año:int) -> None:
    """Gráfico de barras: Monto total de ventas por mes"""
    try:
        engine = create_engine('postgresql+psycopg2://usuario_restaurante:1234@localhost/sistema_restaurante')
        query = f"""
        SELECT EXTRACT(MONTH FROM "Fecha_Venta") AS mes, SUM("Monto_Total") AS total_ventas
        FROM "Hechos_Ventas"
        WHERE EXTRACT(YEAR FROM "Fecha_Venta") = {año}
        GROUP BY mes
        ORDER BY mes;
        """
        df = pd.read_sql_query(query, engine)
        df['mes'] = df['mes'].apply(clasificar_mes)
        plt.figure(figsize=(12, 8))
        plt.bar(df['mes'], df['total_ventas'], color='skyblue')
        plt.title(f'Monto Total de Ventas por Mes - {año}', fontsize=22)
        plt.xlabel('Mes', fontsize=22)
        plt.ylabel('Total Ventas', fontsize=22)
        plt.xticks(df['mes'], rotation=45, fontsize=16)
        plt.yticks(fontsize=16)
        plt.tight_layout()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        os.makedirs(f'gráficos/{año}', exist_ok=True)
        plt.savefig(f'gráficos/{año}/grafico_total_ventas_{año}_por_mes.png')
        plt.close()
    except Exception as e:
        print(f"# Error al graficar ventas por año\nDetalle -> {e}")

def graficar_ventas_consumibles(año:int) -> None:
    """Gráfico de líneas: Ventas de cada consumible por mes"""
    try:
        engine = create_engine('postgresql+psycopg2://usuario_restaurante:1234@localhost/sistema_restaurante')
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
        df = pd.read_sql_query(query, engine)
        df['mes'] = df['mes'].astype(int)
        df['mes_nombre'] = df['mes'].apply(clasificar_mes)
        df = df.sort_values('mes')
        df_pivot = df.pivot(index='mes_nombre', columns='nombre_consumible', values='total_vendido').fillna(0)
        meses_orden = [clasificar_mes(i) for i in range(1, 13)]
        df_pivot = df_pivot.reindex(meses_orden).fillna(0)
        marcadores = ['o', 's', '^', 'D', 'v', '*', 'P', 'X', 'h', '+', 'x', '1', '2', '3', '4', '|', '_']
        consumibles = list(df_pivot.columns)
        plt.figure(figsize=(10, 7))
        for idx, consumible in enumerate(consumibles):
            marcador = marcadores[idx % len(marcadores)]
            plt.plot(df_pivot.index, df_pivot[consumible], marker=marcador, markersize=8, label=consumible)
        plt.title(f'Ventas de Consumibles por Mes - {año}', fontsize=22)
        plt.xlabel('Mes', fontsize=22)
        plt.ylabel('Cantidad Vendida', fontsize=22)
        plt.xticks(rotation=45, fontsize=16)
        plt.yticks(fontsize=16)
        plt.legend(title='Consumible', fontsize=16, title_fontsize=18)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        os.makedirs(f'gráficos/{año}', exist_ok=True)
        plt.savefig(f'gráficos/{año}/grafico_ventas_consumibles_{año}.png')
        plt.close()
    except Exception as e:
        print(f"# Error al graficar ventas de todos los consumibles por mes\nDetalle -> {e}")

def graficar_uso_ingredientes(año:int) -> None:
    """Gráfico de líneas: Uso de ingredientes por mes"""
    try:
        engine = create_engine('postgresql+psycopg2://usuario_restaurante:1234@localhost/sistema_restaurante')
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
        df_pivot = df.pivot(index='mes_nombre', columns='nombre_ingrediente', values='total_usado').fillna(0)
        meses_orden = [clasificar_mes(i) for i in range(1, 13)]
        df_pivot = df_pivot.reindex(meses_orden).fillna(0)
        marcadores = ['o', 's', '^', 'D', 'v', '*', 'P', 'X', 'h', '+', 'x', '1', '2', '3', '4', '|', '_']
        ingredientes = list(df_pivot.columns)
        plt.figure(figsize=(10, 7))
        for idx, ingrediente in enumerate(ingredientes):
            marcador = marcadores[idx % len(marcadores)]
            plt.plot(df_pivot.index, df_pivot[ingrediente], marker=marcador, markersize=8, label=ingrediente)
        plt.title(f'Uso de Ingredientes por Mes - {año}', fontsize=22)
        plt.xlabel('Mes', fontsize=22)
        plt.ylabel('Cantidad Usada', fontsize=22)
        plt.xticks(rotation=45, fontsize=16)
        plt.yticks(fontsize=16)
        plt.legend(title='Ingrediente', fontsize=16, title_fontsize=18)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        os.makedirs(f'gráficos/{año}', exist_ok=True)
        plt.savefig(f'gráficos/{año}/grafico_uso_ingredientes_{año}.png')
        plt.close()
    except Exception as e:
        print(f"# Error al graficar uso de ingredientes\nDetalle -> {e}")

def grafico_porcentaje_ventas_realizadas_meseros(año: int):
    """Gráfico de torta: Porcentaje de ventas realizadas por cada mesero (cantidad de ventas)"""
    try:
        engine = create_engine('postgresql+psycopg2://usuario_restaurante:1234@localhost/sistema_restaurante')
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
        plt.pie(df['total_ventas'], labels=df['nombre_mesero'], autopct='%1.0f%%', textprops={'fontsize': 14})
        plt.title(f"Porcentaje de Ventas Realizadas por Mesero - {año}", fontsize=20)
        plt.tight_layout()
        os.makedirs(f'gráficos/{año}', exist_ok=True)
        plt.savefig(f'gráficos/{año}/grafico_porcentaje_ventas_realizadas_meseros_{año}.png')
        plt.close()
    except Exception as e:
        print(f'# Error al graficar porcentaje ventas por mesero\nDetalle -> {e}')

def grafico_porcentaje_total_ventas_meseros(año: int):
    """Gráfico de torta: Porcentaje del monto total vendido por cada mesero"""
    try:
        engine = create_engine('postgresql+psycopg2://usuario_restaurante:1234@localhost/sistema_restaurante')
        query = f"""
        SELECT m."Nombre" || ' ' || m."Apellido" as nombre_mesero,
        SUM(hv."Monto_Total") as total_ventas
        FROM "Hechos_Ventas" hv
        JOIN "Mesero" m ON hv."FK_Id_Mesero" = m."Id_mesero"
        WHERE EXTRACT(YEAR FROM hv."Fecha_Venta") = {año}
        GROUP BY nombre_mesero
        ORDER BY total_ventas DESC;
        """
        df = pd.read_sql_query(query, engine)
        plt.figure(figsize=(8, 8))
        plt.pie(df['total_ventas'], labels=df['nombre_mesero'], autopct='%1.0f%%', textprops={'fontsize': 14})
        plt.title(f"Porcentaje del Monto Total Vendido por Mesero - {año}", fontsize=20)
        plt.tight_layout()
        os.makedirs(f'gráficos/{año}', exist_ok=True)
        plt.savefig(f'gráficos/{año}/grafico_porcentaje_total_ventas_meseros_{año}.png')
        plt.close()
    except Exception as e:
        print(f'# Error al graficar porcentaje total ventas por mesero\nDetalle -> {e}')

def main():
    año = 2024
    graficar_numero_ventas_por_mes(año)
    graficar_total_ventas_por_mes(año)
    graficar_ventas_consumibles(año)
    graficar_uso_ingredientes(año)
    grafico_porcentaje_ventas_realizadas_meseros(año)
    grafico_porcentaje_total_ventas_meseros(año)
    print("> Gráficos generados con éxito")

if __name__ == "__main__":
    main()