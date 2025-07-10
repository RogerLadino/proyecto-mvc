from flask import current_app

def consultar_codigo(id_usuario, id_ejercicio):
  connection = current_app.connection
    
  with connection.cursor() as cursor:
    cursor.execute("""
      SELECT * FROM codigo WHERE idUsuario = %s AND idEjercicio = %s
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
      SELECT u.idUsuario, u.nombre1, u.apellido1, c.idCodigo
      FROM codigo c
      INNER JOIN usuario u ON c.idUsuario = u.idUsuario 
      WHERE idEjercicio = %s
    """, (id_ejercicio))
        
    return cursor.fetchall() 

def insertar_codigo(idUsuario, idEjercicio, notaObtenida):
  connection = current_app.connection
    
  with connection.cursor() as cursor:
    cursor.execute("""
      INSERT INTO codigo (idUsuario, idEjercicio, codigo, notaObtenida, resuelto, intentosRealizados, fechaEntrega, idTipoLenguaje)
      VALUES (%s, %s, '', %s, 0, 0, '0000-00-00 00:00:00', 'python')
    """, (idUsuario, idEjercicio, notaObtenida))
        
    connection.commit()
    
    return cursor.lastrowid 

def actualizar_codigo(idCodigo, nuevoCodigo):
  connection = current_app.connection
    
  with connection.cursor() as cursor:
    cursor.execute("""
      UPDATE codigo 
      SET codigo = %s
      WHERE idCodigo = %s
    """, (nuevoCodigo, idCodigo))
        
    connection.commit()
    
    return cursor.lastrowid 
