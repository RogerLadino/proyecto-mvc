# app/controllers/main.py

from flask import Blueprint, render_template

# Creamos un nuevo Blueprint para las rutas principales
main_bp = Blueprint('main_bp', __name__, template_folder='../../templates')

@main_bp.route('/')
def index():
    """Muestra la página de inicio (index.html)."""
    return render_template('index.html')