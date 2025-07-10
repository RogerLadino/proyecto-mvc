from flask import session

def obtener_sesion_id_usuario():
    if 'id-usuario' not in session:
        raise Exception("Sesión no iniciada. Falta 'id-usuario' en la sesión.")
    return int(session['id-usuario'])