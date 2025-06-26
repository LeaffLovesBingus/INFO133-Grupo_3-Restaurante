from flask import Flask, render_template, send_from_directory, request
import os

app = Flask(__name__)

# Ruta absoluta a la carpeta de gráficos
GRAFICOS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'gráficos'))

@app.route('/graficos/<path:filename>')
def graficos_static(filename):
    return send_from_directory(GRAFICOS_DIR, filename)

@app.route('/analisis')
def mostrar_graficos():
    year = request.args.get('year')
    graficos = []
    for root, dirs, files in os.walk(GRAFICOS_DIR):
        # Si se selecciona un año, solo busca en esa subcarpeta
        if year and os.path.basename(root) != year:
            continue
        for file in files:
            if file.lower().endswith('.png'):
                rel_dir = os.path.relpath(root, GRAFICOS_DIR)
                rel_file = os.path.join(rel_dir, file) if rel_dir != '.' else file
                graficos.append(rel_file.replace("\\", "/"))
    # Obtén lista de años disponibles (subcarpetas)
    years = sorted([d for d in os.listdir(GRAFICOS_DIR) if os.path.isdir(os.path.join(GRAFICOS_DIR, d))])
    return render_template('analisis.html', graficos=graficos, years=years, year_actual=year)