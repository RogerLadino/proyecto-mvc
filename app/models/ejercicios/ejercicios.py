# Este archivo debe contener las funciones que se comunican con la base de datos (modelos)
from flask import current_app

def consultar_ejercicio(id_ejercicio):
  connection = current_app.connection
    
  with connection.cursor() as cursor:
    cursor.execute("""
      SELECT * FROM ejercicio WHERE idEjercicio = %s
    """, (id_ejercicio))
        
    return cursor.fetchone()

def consultar_ejercicios_por_aula(id_aula):
  connection = current_app.connection
    
  with connection.cursor() as cursor:
    cursor.execute("""
      SELECT * FROM ejercicio WHERE idAula = %s
    """, (id_aula))
        
    return cursor.fetchall()
  return []

def consultar_estadisticas_ejercicio(id_ejercicio, id_aula):
  connection = current_app.connection
    
  with connection.cursor() as cursor:
    cursor.execute("""
      SELECT u.idUsuario, u.nombre1, u.apellido1, e.notaObtenida, e.estado, c.intentosRealizados, e.fechaEntrega
      FROM entrega e
      LEFT JOIN codigo c ON e.idUsuario = c.idUsuario AND e.idEjercicio = c.idEjercicio
      RIGHT JOIN usuario_aula ua ON e.idUsuario = ua.idUsuario AND e.idEjercicio = %s 
      INNER JOIN usuario u ON ua.idUsuario = u.idUsuario AND ua.idAula = %s
      WHERE ua.idRol = 2
    """, (id_ejercicio, id_aula))
        
    res = cursor.fetchall()
    return res

def insertar_ejercicio(idAula, nombre, descripcion, fechaEntrega = '0000-00-00 00:00:00'):
  connection = current_app.connection
    
  with connection.cursor() as cursor:
    cursor.execute("""
      INSERT INTO ejercicio (nombre, descripcion, fechaEntrega, idAula)
      VALUES (%s, %s, %s, %s)
    """, (nombre, descripcion, fechaEntrega, idAula))
        
    idEjercicio = cursor.lastrowid
        
    connection.commit()

    return idEjercicio
  
def editar_ejercicio(idEjercicio, nombre, descripcion, fechaEntrega = '0000-00-00 00:00:00'):
  connection = current_app.connection
    
  with connection.cursor() as cursor:
    cursor.execute("""
      UPDATE ejercicio
      SET nombre = %s, descripcion = %s, fechaEntrega = %s
      WHERE idEjercicio = %s
    """, (nombre, descripcion, fechaEntrega, idEjercicio))
        
    connection.commit()

def eliminar_ejercicio(idEjercicio):
  connection = current_app.connection
    
  with connection.cursor() as cursor:
    cursor.execute("""
      DELETE FROM ejercicio WHERE idEjercicio = %s
    """, (idEjercicio))
        
    connection.commit()

  return True