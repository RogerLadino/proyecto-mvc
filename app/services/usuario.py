from flask import session

def obtener_sesion_id_usuario():
  return int(session['id_usuario'])