
# Este archivo debe contener las siguientes rutas:

# GET /aulas -- Listar aulas
# POST /aulas/crear -- Crear aulas
# DELETE /aulas/eliminar/<id> -- Eliminar aula según id
# PUT /aulas/modificar/<id>  -- Modificar aula según id
from flask import Blueprint,render_template, request, redirect, url_for, session, flash
from config import Config
from app.models.aulas.aulas import es_profesor
from app.services.usuario import obtener_sesion_id_usuario
from app.models.aulas.aulas import (
    listar_aulas, insertar_aula, consultar_aula,
    modificar_aula, eliminar_aula
)

aulas_bp = Blueprint('aulas_bp', __name__)

@aulas_bp.route('/aulas')
def aulas():
    try:
        id_usuario = obtener_sesion_id_usuario()
        aulas = listar_aulas(id_usuario)
        print("Aulas devueltas:", aulas)

        return render_template('aulas/clases.html', aulas=aulas)
    except Exception as e:
        flash(f"Error al obtener aulas: {str(e)}", "danger")
        return render_template('aulas/clases.html', aulas=[])

@aulas_bp.route('/aulas/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        codigo = request.form.get('codigo')
        id_usuario = obtener_sesion_id_usuario()
        try:
            insertar_aula(nombre, codigo, id_usuario)
            flash("Aula creada exitosamente", "success")
            return redirect(url_for('aulas_bp.aulas'))
        except Exception as e:
            flash(f"Error al crear aula: {str(e)}", "danger")
        return render_template('aulas/crear-clase.html')

@aulas_bp.route('/aulas/modificar/<int:id_aula>', methods=['GET', 'POST'])
def modificar(id_aula):
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        codigo = request.form.get('codigo')
        try:
            modificar_aula(id_aula, nombre, codigo)
            flash("Aula modificada exitosamente", "success")
            return redirect(url_for('aulas_bp.aulas'))
        except Exception as e:
            flash(f"Error al modificar aula: {str(e)}", "danger")
    try:
        aula = consultar_aula(id_aula)
        return render_template('aulas/editar-clase.html', aula=aula)
    except Exception as e:
        flash(f"Error al cargar aula: {str(e)}", "danger")
        return redirect(url_for('aulas_bp.aulas'))

@aulas_bp.route('/aulas/eliminar/<int:id_aula>', methods=['POST'])
def eliminar(id_aula):
    try:
        eliminar_aula(id_aula)
        flash("Aula eliminada exitosamente", "success")
    except Exception as e:
        flash(f"Error al eliminar aula: {str(e)}", "danger")
    return redirect(url_for('aulas_bp.aulas'))


@aulas_bp.route('/aulas-redirigir')
def redirigir_aulas():
    id_usuario = obtener_sesion_id_usuario()
    if es_profesor(id_usuario):
        return redirect(url_for('aulas_bp.aulas'))
    else:
        return redirect(url_for('aulas_alumno_bp.aulas_alumno'))

@aulas_bp.route('/inicio')
def inicio_según_rol():
    id_usuario = obtener_sesion_id_usuario()
    if es_profesor(id_usuario):
        return redirect(url_for('aulas_bp.aulas'))  # Vista para profesores
    else:
        return redirect(url_for('aulas_alumno_bp.aulas_alumno'))  # Vista para alumnos
   






