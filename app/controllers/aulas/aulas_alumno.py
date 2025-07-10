from flask import Blueprint, render_template, session, request, redirect, url_for, flash, current_app
from app.services.usuario import obtener_sesion_id_usuario
from app.models.aulas.aulas import listar_aulas_alumno, obtener_aulas_sidebar

aulas_alumno_bp = Blueprint('aulas_alumno_bp', __name__)

@aulas_alumno_bp.route('/aulas-alumno')
def aulas_alumno():
    id_usuario = obtener_sesion_id_usuario()
    aulas = listar_aulas_alumno(id_usuario)
    aulas_sidebar = obtener_aulas_sidebar(id_usuario)
    return render_template('aulas/aulas-alumno.html', aulas=aulas, sidebar=aulas_sidebar)

@aulas_alumno_bp.route('/aulas-alumno/unirse', methods=['POST'])
def unirse():
    codigo = request.form.get('codigo')
    id_usuario = obtener_sesion_id_usuario()

    connection = current_app.connection
    try:
        with connection.cursor() as cursor:
            # Verificar si existe un aula con ese código
            cursor.execute("SELECT idAula FROM aula WHERE codigo = %s", (codigo,))
            aula = cursor.fetchone()

            if not aula:
                flash("El código ingresado no corresponde a ninguna clase.", "danger")
                return redirect(url_for('aulas_alumno_bp.aulas_alumno'))

            id_aula = aula['idAula']

            # Verificar si ya está inscrito
            cursor.execute("SELECT * FROM usuario_aula WHERE idUsuario = %s AND idAula = %s", (id_usuario, id_aula))
            existe = cursor.fetchone()

            if existe:
                flash("Ya estás inscrito en esta clase.", "info")
            else:
                # Insertar en usuario_aula con rol de alumno (idRol = 2)
                cursor.execute("""
                    INSERT INTO usuario_aula (idUsuario, idAula, idRol)
                    VALUES (%s, %s, 2)
                """, (id_usuario, id_aula))
                connection.commit()
                flash("Te has unido exitosamente al aula.", "success")

    except Exception as e:
        connection.rollback()
        flash(f"Ocurrió un error: {str(e)}", "danger")

    return redirect(url_for('aulas_alumno_bp.aulas_alumno'))
