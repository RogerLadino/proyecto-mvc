from flask import current_app

def consultar_aula(id_aula):
  connection = current_app.connection
  
  with connection.cursor() as cursor:
    cursor.execute("""
      SELECT * FROM aula WHERE idAula = %s
    """, (id_aula))
    
    return cursor.fetchone()

def es_profesor(id_usuario, id_aula):
  aula = consultar_aula(id_aula)
    
  if aula['idUsuario'] == id_usuario:
    return True
  return False