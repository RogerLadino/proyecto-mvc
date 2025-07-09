from flask import current_app

def consultar_codigo(id_usuario, id_ejercicio):
  connection = current_app.connection
    
  with connection.cursor() as cursor:
    cursor.execute("""
      SELECT c.*, u.nombre1, u.apellido1
      FROM codigo c
      INNER JOIN usuario u ON c.idUsuario = u.idUsuario
      WHERE c.idUsuario = %s AND c.idEjercicio = %s
    """, (id_usuario, id_ejercicio))
        

    return cursor.fetchone()

def consultar_usuario_con_codigo(id_codigo):
  connection = current_app.connection
    
  with connection.cursor() as cursor:
    cursor.execute("""
      SELECT u.idUsuario, u.nombre1, u.apellido1
      FROM codigo c
      INNER JOIN usuario u ON u.idUsuario = c.idUsuario
      WHERE c.idCodigo = %s
    """, (id_codigo))
        
    return cursor.fetchone()

def consultar_codigo_por_id(id_codigo):
  connection = current_app.connection
    
  with connection.cursor() as cursor:
    cursor.execute("""
      SELECT * FROM codigo WHERE idCodigo = %s
    """, (id_codigo))
        
    return cursor.fetchone()
  
def consultar_usuarios_con_codigo(id_ejercicio):
  connection = current_app.connection
    
  with connection.cursor() as cursor:
    cursor.execute("""
      SELECT u.idUsuario, u.nombre1, u.apellido1
      FROM codigo c
      INNER JOIN usuario u ON c.idUsuario = u.idUsuario 
      WHERE idEjercicio = %s
    """, (id_ejercicio))
        
    return cursor.fetchall() 

def insertar_codigo(idUsuario, idEjercicio):
  connection = current_app.connection
    
  with connection.cursor() as cursor:
    cursor.execute("""
      INSERT INTO codigo (idUsuario, idEjercicio, codigo, intentosRealizados, idTipoLenguaje)
      VALUES (%s, %s, '', 0, 1)
    """, (idUsuario, idEjercicio))
        
    connection.commit()
    
    return cursor.lastrowid 

def actualizar_codigo(idUsuario, idEjercicio, nuevoCodigo):
  connection = current_app.connection
    
  with connection.cursor() as cursor:
    cursor.execute("""
      UPDATE codigo 
      SET codigo = %s
      WHERE idUsuario = %s AND idEjercicio = %s
    """, (nuevoCodigo, idUsuario, idEjercicio))
        
    connection.commit()
    
    return cursor.lastrowid 
