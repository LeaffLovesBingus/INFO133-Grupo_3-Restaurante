import schedule
import time
from transferir_datos import *
import subprocess
import sys
import os

def job():
    vaciar_tablas()
    transferir_datos()
    años = ["2022", "2023", "2024", "2025"]
    ruta_analisis = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'analisis.py'))
    for año in años:
        subprocess.run([sys.executable, ruta_analisis, año])

def scheduler():
    schedule.every(1).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
