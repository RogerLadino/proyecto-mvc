from flask import Blueprint, render_template, session
from app.services.usuario import obtener_sesion_id_usuario
from app.models.aulas.aulas import listar_aulas_alumno

aulas_alumno_bp = Blueprint('aulas_alumno_bp', __name__)

@aulas_alumno_bp.route('/aulas-alumno')
def aulas_alumno():
    id_usuario = obtener_sesion_id_usuario()
    aulas = listar_aulas_alumno(id_usuario)
    return render_template('aulas/aulas-alumno.html', aulas=aulas)
