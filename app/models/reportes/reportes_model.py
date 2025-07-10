# app/models/reporte_model.py

from flask import current_app, abort 

def obtener_datos_reporte(id_aula):
    """
    Función del modelo que usa la conexión a la base de datos existente en la app
    para consultar los datos de un reporte.
    """
    try:
        conn = current_app.connection
        with conn.cursor() as cursor:
            query = """
                SELECT
                    a.idAula, a.nombre AS nombre_aula,
                    u.idUsuario, u.nombre1, u.apellido1,
                    e.idEjercicio, e.nombre AS nombre_ejercicio,
                    ent.notaObtenida, ent.estado AS estado_entrega,
                    c.intentosRealizados
                FROM aula a
                JOIN usuario_aula ua ON a.idAula = ua.idAula
                JOIN usuario u ON ua.idUsuario = u.idUsuario AND ua.idRol = u.idRol
                LEFT JOIN ejercicio e ON a.idAula = e.idAula
                LEFT JOIN entrega ent ON u.idUsuario = ent.idUsuario AND e.idEjercicio = ent.idEjercicio
                LEFT JOIN codigo c ON ent.idUsuario = c.idUsuario AND ent.idEjercicio = c.idEjercicio
                WHERE a.idAula = %s AND u.idRol = 2
                ORDER BY u.apellido1, u.nombre1, e.idEjercicio;
            """
            cursor.execute(query, (id_aula,))
            return cursor.fetchall()
    except Exception as e:
        print(f"Error en el modelo de reportes: {e}")
        # Es importante manejar errores, podrías abortar o devolver None/vacío
        abort(500, description="Error al consultar los datos del reporte.")