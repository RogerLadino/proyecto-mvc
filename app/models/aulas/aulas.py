from flask import current_app

# Listar aulas creadas por un profesor
def listar_aulas(id_usuario):
    connection = current_app.connection
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT a.*
            FROM aula a
            JOIN usuario_aula ua ON a.idAula = ua.idAula
            WHERE ua.idUsuario = %s AND ua.idRol = 1
        """, (id_usuario,))
        return cursor.fetchall()

# Insertar aula y asociar con el profesor
def insertar_aula(nombre, codigo, id_usuario):
    connection = current_app.connection
    with connection.cursor() as cursor:
        # Insertar aula
        cursor.execute(
            "INSERT INTO aula (nombre, codigo) VALUES (%s, %s)",
            (nombre, codigo)
        )
        id_aula = cursor.lastrowid

        # Asociar aula con el profesor (rol 1)
        cursor.execute(
            "INSERT INTO usuario_aula (idAula, idUsuario, idRol) VALUES (%s, %s, %s)",
            (id_aula, id_usuario, 1)
        )

        connection.commit()

# Consultar aula por ID
def consultar_aula(id_aula):
    connection = current_app.connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM aula WHERE idAula = %s", (id_aula,))
        return cursor.fetchone()

# Modificar aula
def modificar_aula(id_aula, nombre):
    connection = current_app.connection
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE aula SET nombre = %s WHERE idAula = %s",
            (nombre, id_aula)
        )
        connection.commit()

# Eliminar aula
def eliminar_aula(id_aula):
    connection = current_app.connection
    with connection.cursor() as cursor:
        # Eliminar primero de la tabla usuario_aula (por integridad referencial)
        cursor.execute("DELETE FROM usuario_aula WHERE idAula = %s", (id_aula,))
        # Luego eliminar el aula
        cursor.execute("DELETE FROM aula WHERE idAula = %s", (id_aula,))
        connection.commit()

# Verificar si un usuario es profesor
def es_profesor(id_usuario):
    connection = current_app.connection
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM usuario 
            WHERE idUsuario = %s AND idRol = 1
        """, (id_usuario))
        return cursor.fetchone() is not None

# Verificar si un usuario es profesor de un aula
def es_profesor_de_aula(id_usuario, id_aula):
    connection = current_app.connection
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM usuario_aula
            WHERE idUsuario = %s AND idAula = %s AND idRol = 1
        """, (id_usuario, id_aula))
        return cursor.fetchone() is not None

def listar_aulas_por_profesor(id_usuario):
    connection = current_app.connection
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT a.*
            FROM aula a
            JOIN usuario_aula ua ON a.idAula = ua.idAula
            WHERE ua.idUsuario = %s AND ua.idRol = 1
        """, (id_usuario,))
        return cursor.fetchall()
    

# Listar aulas a las que un alumno está inscrito
def listar_aulas_alumno(id_usuario):
    connection = current_app.connection
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT a.*
            FROM aula a
            JOIN usuario_aula ua ON a.idAula = ua.idAula
            WHERE ua.idUsuario = %s AND ua.idRol = 2
        """, (id_usuario,))
        return cursor.fetchall()

def obtener_profesor(id_aula):
  connection = current_app.connection
  
  with connection.cursor() as cursor:
    cursor.execute("""
      SELECT idUsuario FROM usuario_aula WHERE idAula = %s AND idRol = 1
    """, (id_aula))
    
    return cursor.fetchone()
    

def obtener_aulas_sidebar(id_usuario):
  connection = current_app.connection
  
  with connection.cursor() as cursor:
    cursor.execute("""
      SELECT * 
      FROM usuario_aula ua 
      JOIN aula a ON a.idAula = ua.idAula
      WHERE ua.idUsuario = %s
    """, (id_usuario))
    
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