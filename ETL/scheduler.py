import schedule
import time
from datetime import datetime
from transferir_datos import *
import subprocess
import sys
import os

def job():
    print("Iniciando ETL...")
    vaciar_tablas()
    transferir_datos()
    años = ["2022", "2023", "2024", "2025"]
    ruta_analisis = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'analisis.py'))
    for año in años:
        subprocess.run([sys.executable, ruta_analisis, año])
    with open("/tmp/etl_last_run.txt", "w") as f:
        f.write(datetime.now().isoformat())
    print("ETL completado.")

def scheduler():
    schedule.every(1).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
