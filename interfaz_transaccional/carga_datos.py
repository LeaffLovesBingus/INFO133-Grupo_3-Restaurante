# carga_datos.py (tu blueprint)
from flask import Blueprint, render_template_string, request
from modelo_db.cargar_datos_masivos import generar_datos_masivos

carga_datos_bp = Blueprint("carga_datos_bp", __name__)

@carga_datos_bp.route("/cargar_datos_prueba", methods=["POST"])
def cargar_datos():
    resultado = generar_datos_masivos()
    
    if resultado.startswith("✅"):
        return render_template_string("""
        <div style='font-family: sans-serif; padding: 2rem;'>
            <h2 style='color: green;'>{{ resultado }}</h2>
            <br>
            <a href="/" style="color: blue; text-decoration: underline;">Volver al menú</a>
        </div>
        """, resultado=resultado)
    else:
        return render_template_string("""
        <div style='font-family: sans-serif; padding: 2rem;'>
            <h2 style='color: red;'>{{ resultado }}</h2>
            <br>
            <a href="/" style="color: blue; text-decoration: underline;">Volver al menú</a>
        </div>
        """, resultado=resultado)