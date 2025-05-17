import sys
import os
from pathlib import Path
from generador_gráficos.funciones_graficos import *


def main():
    if (len(sys.argv) != 2):
        print("Error, ejecute como: python analisis.py 'año'")

    año = sys.argv[1]
    carpeta_año = Path(f"gráficos/{año}")
    if (not os.path.exists(carpeta_año)):
        os.makedirs(carpeta_año)

    print(f"Generando estadísticas del año {año}")

    graficar_numero_ventas_por_mes(año)
    print("> (Barras) Número de ventas por mes generado con éxito")

    graficar_total_ventas_por_mes(año)
    print("> (Barras) Número total de ventas por mes generado con éxito")

    graficar_ventas_consumibles(año)
    print("> (Barras) Consumible más vendido por mes generado con éxito")

    #ventas_por_mesero_por_mes(año)
    print("> (Barras) Ventas por mesero por mes generado con éxito")
    
    #ventas_consumibles_por_mes(año)
    print("> (Barras) Número de ventas de cada consumible por mes generado con éxito")

    #ingrediende_mas_usado_por_mes(año)
    print("> (Barras) Ingrediente más usado por mes generado con éxito")

    #ingredientes_por_cocinero_por_mes(año)
    print("> (Barras) Cocineros que utilizan más ingredientes por mes generado con éxito")

    #numero_ingredientes_usados_por_mes(año)
    print("> (Barras) Número de ingredientes usados por mes generado con éxito")

    #ventas_mesero_por_año(año)
    print("> (Torta) Número de ventas por mesero en todo el año generado con éxito")

    #total_uso_ingredientes_por_cocinero(año)
    print("> (Torta) Cocineros que utilizan más ingredientes por mes generado con éxito")


if __name__ == "__main__":
    main()