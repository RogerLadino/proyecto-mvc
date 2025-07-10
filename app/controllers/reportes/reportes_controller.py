# app/controllers/reportes.py

from flask import Blueprint, render_template, abort
from app.models.reportes.reportes_model import obtener_datos_reporte
from app.services.usuario import obtener_sesion_id_usuario
from app.models.aulas.aulas import obtener_aulas_sidebar

# Se crea el Blueprint con un prefijo de URL para todas las rutas de este archivo
reportes_bp = Blueprint('reportes', __name__, url_prefix='/reportes')

@reportes_bp.route('/<int:id_aula>')
def ver_reporte(id_aula):
    """
    Ruta para mostrar la página de reportes de un aula.
    Llama al modelo, procesa los datos y renderiza la vista.
    """
    # 1. Llama al modelo para obtener los datos (la llamada ahora es más simple)
    resultados_db = obtener_datos_reporte(id_aula)

    # Si el aula no existe o no tiene alumnos, devuelve un error 404
    if not resultados_db:
        abort(404, f"No se encontraron datos para el aula con ID {id_aula}.")

    # 2. Procesa los resultados de la base de datos para estructurarlos
    aula_info = {
        "nombre": resultados_db[0]['nombre_aula'],
        "id": resultados_db[0]['idAula']
    }
    
    ejercicios_header = []
    estudiantes_dict = {}

    for fila in resultados_db:
        # Agrupa los datos por estudiante para evitar duplicados
        if fila['idUsuario'] not in estudiantes_dict:
            estudiantes_dict[fila['idUsuario']] = {
                "nombre_completo": f"{fila['nombre1']} {fila['apellido1']}",
                "status_class": "dot-red" if fila['idUsuario'] % 2 == 0 else "dot-danger-red", # Lógica de ejemplo para el color del punto
                "ejercicios": []
            }
        
        # Añade la información de cada ejercicio al estudiante correspondiente
        if fila['idEjercicio']:
            estudiantes_dict[fila['idUsuario']]['ejercicios'].append({
                "score": fila['notaObtenida'] or 0,
                "intentos": fila['intentosRealizados'] or 0,
            })
            
            # Crea la cabecera de la tabla con los nombres de los ejercicios (sin duplicados)
            if not any(e['id'] == fila['idEjercicio'] for e in ejercicios_header):
                ejercicios_header.append({
                    "id": fila['idEjercicio'],
                    "nombre": fila['nombre_ejercicio'],
                    "dot_class": "dot-border-orange" if len(ejercicios_header) % 2 == 0 else "dot-border-green"
                })

    # Convierte el diccionario de estudiantes a una lista para el renderizado
    lista_estudiantes = list(estudiantes_dict.values())

    # Sidebar para navegación
    id_usuario = obtener_sesion_id_usuario()
    aulas_sidebar = obtener_aulas_sidebar(id_usuario)

    # 3. Pasa los datos procesados a la plantilla HTML
    return render_template(
        'reportes.html',
        aula=aula_info,
        ejercicios=ejercicios_header,
        estudiantes=lista_estudiantes,
        sidebar=aulas_sidebar
    )
