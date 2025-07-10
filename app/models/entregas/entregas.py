# Este archivo debe contener las funciones que se comunican con la base de datos (modelos)
from flask import current_app

def consultar_entrega(id_ejercicio, id_usuario):
  connection = current_app.connection
    
  with connection.cursor() as cursor:
    cursor.execute("""
      SELECT * FROM entrega WHERE idEjercicio = %s AND idUsuario = %s
    """, (id_ejercicio, id_usuario))
        
    return cursor.fetchone()
  
def insertar_entrega(id_usuario, id_ejercicio, notaObtenida = 0):
  connection = current_app.connection
    
  with connection.cursor() as cursor:
    cursor.execute("""
      INSERT INTO entrega (idUsuario, idEjercicio, notaObtenida, estado, fechaEntrega)
      VALUES (%s, %s, %s, 0, '0000-00-00 00:00:00')
    """, (id_usuario, id_ejercicio, notaObtenida))
        
    cursor.lastrowid
        
    connection.commit()

  return True

def darNota(idUsuario, idEjercicio, nota):
  connection = current_app.connection
    
  with connection.cursor() as cursor:
    cursor.execute("""
      UPDATE entrega 
      SET notaObtenida = %s
      WHERE idUsuario = %s AND idEjercicio = %s
    """, (nota, idUsuario, idEjercicio))
        
    connection.commit()
