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

    graficar_total_ventas_por_mes(año)

    graficar_ventas_consumibles(año)

    graficar_uso_ingredientes(año)

    grafico_porcentaje_ventas_realizadas_meseros(año)

    grafico_porcentaje_total_ventas_meseros(año)

    print(f"> Gráficos para el {año} generados con éxito")


if __name__ == "__main__":
    main()