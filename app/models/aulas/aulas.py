from flask import current_app

def consultar_aula(id_aula):
  connection = current_app.connection
  
  with connection.cursor() as cursor:
    cursor.execute("""
      SELECT * FROM aula WHERE idAula = %s
    """, (id_aula))
    
    return cursor.fetchone()

def es_profesor(id_usuario, id_aula):
  connection = current_app.connection
  
  with connection.cursor() as cursor:
    cursor.execute("""
      SELECT * FROM usuario_aula WHERE idAula = %s AND idRol = 1
    """, (id_aula))
    
    usuarioAula = cursor.fetchone()
    
  if usuarioAula['idUsuario'] == id_usuario:
    return True
  return False

def obtener_profesor(id_aula):
  connection = current_app.connection
  
  with connection.cursor() as cursor:
    cursor.execute("""
      SELECT idUsuario FROM usuario_aula WHERE idAula = %s AND idRol = 1
    """, (id_aula))
    
    return cursor.fetchone()
    

def obtener_aulas_sidebar(id_usuario, id_rol):
  connection = current_app.connection
  
  with connection.cursor() as cursor:
    cursor.execute("""
      SELECT * 
      FROM usuario_aula ua 
      JOIN aulas a ON a.idUsuario = ua.idUsuario
      WHERE a.idUsuario = %s AND idRol = %s
    """, (id_usuario, id_rol))
    
    return cursor.fetchall()

  return []

def actualizar_codigo_aula(id_aula, codigo):
  connection = current_app.connection
  
  with connection.cursor() as cursor:
    cursor.execute("""
      UPDATE aula
      SET codigo = %s
      WHERE idAula = %s
    """, (codigo, id_aula))
    
    connection.commit()
  return True