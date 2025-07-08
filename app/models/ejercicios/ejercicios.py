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
      SELECT u.idUsuario, u.nombre1, u.apellido1, c.notaObtenida, c.resuelto, c.intentosRealizados, c.fechaEntrega
      FROM codigo c
      RIGHT JOIN usuario_aula ua ON c.idUsuario = ua.idUsuario AND c.idEjercicio = %s 
      LEFT JOIN usuario u ON ua.idUsuario = u.idUsuario AND ua.idAula = %s
      WHERE ua.idRol = 2
    """, (id_ejercicio, id_aula))
        
    return cursor.fetchall()

def insertar_ejercicio(idAula, nombre, descripcion, codigoInicial, fechaEntrega, idTipoLenguaje = 'python'):
  connection = current_app.connection
    
  with connection.cursor() as cursor:
    cursor.execute("""
      INSERT INTO ejercicio (nombre, descripcion, codigoInicial, fechaEntrega, idAula, idTipoLenguaje)
      VALUES (%s, %s, %s, %s, %s, %s)
    """, (nombre, descripcion, codigoInicial, fechaEntrega, idAula, idTipoLenguaje))
        
    idEjercicio = cursor.lastrowid
        
    connection.commit()

    return idEjercicio
  
def editar_ejercicio(idEjercicio, nombre, descripcion, codigoInicial, fechaEntrega, idTipoLenguaje = 'python'):
  connection = current_app.connection
    
  with connection.cursor() as cursor:
    cursor.execute("""
      UPDATE ejercicio
      SET nombre = %s, descripcion = %s, codigoInicial = %s, fechaEntrega = %s, idTipoLenguaje = %s
      WHERE idEjercicio = %s
    """, (nombre, descripcion, codigoInicial, fechaEntrega, idTipoLenguaje, idEjercicio))
        
    connection.commit()

def eliminar_ejercicio(idEjercicio):
  connection = current_app.connection
    
  with connection.cursor() as cursor:
    cursor.execute("""
      DELETE FROM ejercicio WHERE idEjercicio = %s
    """, (idEjercicio))
        
    connection.commit()