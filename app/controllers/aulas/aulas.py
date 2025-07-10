from flask import Blueprint,render_template, request, redirect, url_for, session, flash
from config import Config
from app.models.aulas.aulas import es_profesor
from app.services.usuario import obtener_sesion_id_usuario
from app.models.aulas.aulas import (
    listar_aulas, insertar_aula, consultar_aula,
    modificar_aula, eliminar_aula, listar_aulas_por_profesor,
    obtener_aulas_sidebar
)
from app.utils.generar_codigo import generar_codigo

aulas_bp = Blueprint('aulas_bp', __name__)


@aulas_bp.route('/aulas')
def aulas():
    aulas_sidebar = obtener_aulas_sidebar(obtener_sesion_id_usuario())

    try:
        id_usuario = obtener_sesion_id_usuario()
        aulas = listar_aulas_por_profesor(id_usuario)
        print("Aulas devueltas:", aulas)

        return render_template('aulas/clases.html', aulas=aulas, sidebar=aulas_sidebar)
    except Exception as e:
        flash(f"Error al obtener aulas: {str(e)}", "danger")
        return render_template('aulas/clases.html', aulas=[], sidebar=aulas_sidebar)

@aulas_bp.route('/aulas/crear', methods=['GET', 'POST'])
def crear():
    aulas_sidebar = obtener_aulas_sidebar(obtener_sesion_id_usuario())

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        codigo = generar_codigo(6)
        id_usuario = obtener_sesion_id_usuario()
        try:
            insertar_aula(nombre, codigo, id_usuario)
            flash("Aula creada exitosamente", "success")
            return redirect(url_for('aulas_bp.aulas'))
        except Exception as e:
            flash(f"Error al crear aula: {str(e)}", "danger")
    return render_template('aulas/crear-clase.html', sidebar=aulas_sidebar)

@aulas_bp.route('/aulas/modificar/<int:id_aula>', methods=['GET', 'POST'])
def modificar(id_aula):
    aulas_sidebar = obtener_aulas_sidebar(obtener_sesion_id_usuario())

    if request.method == 'POST':
        nombre = request.form.get('nombre')

        try:
            modificar_aula(id_aula, nombre)
            flash("Aula modificada exitosamente", "success")
            return redirect(url_for('aulas_bp.aulas'))
        except Exception as e:
            print('hi', str(e))
            flash(f"Error al modificar aula: {str(e)}", "danger")
    try:
        aula = consultar_aula(id_aula)
        return render_template('aulas/editar-clase.html', aula=aula, sidebar=aulas_sidebar)
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
def inicio_segun_rol():
    id_usuario = obtener_sesion_id_usuario()

    print(id_usuario)
    if es_profesor(id_usuario):
        return redirect(url_for('aulas_bp.aulas'))  # Vista para profesores
    else:
        return redirect(url_for('aulas_alumno_bp.aulas_alumno'))  # Vista para alumnos







