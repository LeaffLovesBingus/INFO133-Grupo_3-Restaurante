import sys
import os
from pathlib import Path
from generador_gráficos.funciones_graficos import *


def main():
    if (len(sys.argv) != 2):
        print("Error, ejecute como: python analisis.py 'año'")
        sys.exit(1)

    año = sys.argv[1]
    carpeta_año = Path(f"gráficos/{año}")
    if (not os.path.exists(carpeta_año)):
        os.makedirs(carpeta_año)

    print(f"Generando estadísticas del año {año}")

    graficar_numero_ventas_por_mes(año)
    print("> (Barras) Número de ventas por mes generado con éxito")

    graficar_total_ventas_por_mes(año)
    print("> (Barras) Total ventas por mes generado con éxito")

    graficar_ventas_consumibles(año)
    print("> (Lineas) Ventas por consumibles generado con éxito")

    graficar_uso_ingredientes(año)
    print("> (Lineas) Uso de ingredientes generado con éxito")

    grafico_porcentaje_ventas_realizadas_meseros(año)
    print("> (Torta) Ventas realizadas por mesero generado con éxito")

    grafico_porcentaje_total_ventas_meseros(año)
    print("> (Torta) Montos totales de las ventas realizadas por los meseros generado con éxito")


if __name__ == "__main__":
    main()