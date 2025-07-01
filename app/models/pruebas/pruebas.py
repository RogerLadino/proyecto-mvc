from flask import current_app

def consultar_pruebas(id_ejercicio):
  connection = current_app.connection
    
  with connection.cursor() as cursor:
    cursor.execute("""
      SELECT * FROM prueba WHERE idEjercicio = %s ORDER BY idPrueba
   """, (id_ejercicio)) 
        
    return cursor.fetchall()

def insertar_prueba(idEjercicio, nombreFuncion, entrada, salida):
    connection = current_app.connection
    
    with connection.cursor() as cursor:
      cursor.execute("""
        INSERT INTO prueba (nombreFuncion, entrada, salida, idEjercicio)
        VALUES (%s, %s, %s, %s)
      """, (nombreFuncion, entrada, salida, idEjercicio))
        
      idPrueba = cursor.lastrowid
        
      connection.commit()

      return idPrueba 

def eliminar_prueba(idPrueba):
    connection = current_app.connection
    
    with connection.cursor() as cursor:
      cursor.execute("""
        DELETE FROM prueba WHERE idPrueba = %s
      """, (idPrueba))
        
      connection.commit()
      
def editar_prueba(idPrueba, nombreFuncion, entrada, salida):
    connection = current_app.connection
    
    with connection.cursor() as cursor:
      cursor.execute("""
        UPDATE prueba
        SET nombreFuncion = %s, entrada = %s, salida = %s
        WHERE idPrueba = %s
      """, (nombreFuncion, entrada, salida, idPrueba))
        
      connection.commit()