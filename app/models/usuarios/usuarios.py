from flask import current_app

def consultar_usuario(id_usuario):
  connection = current_app.connection
    
  with connection.cursor() as cursor:
    cursor.execute("""
      SELECT * FROM usuario WHERE idUsuario = %s
   """, (id_usuario)) 
        
    return cursor.fetchone()