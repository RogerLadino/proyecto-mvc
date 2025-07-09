# app/models/usuarios_model.py

def get_usuario_by_correo(connection, correo):
    """Busca si un correo ya existe en la base de datos."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT idUsuario FROM usuario WHERE correo = %s", (correo,))
        return cursor.fetchone()

def insert_usuario(connection, nombre1, nombre2, apellido1, apellido2, correo, hashed_password, idRol):
    """Inserta un nuevo usuario en la tabla 'usuario', incluyendo su rol."""
    with connection.cursor() as cursor:
        # Se añade la columna 'idRol' a la consulta
        sql = """INSERT INTO usuario (nombre1, nombre2, apellido1, apellido2, correo, contraseña, idRol)
                 VALUES (%s, %s, %s, %s, %s, %s, %s)""" # Se añade un placeholder '%s'
        
        # Se pasa el nuevo valor 'idRol' en la tupla de ejecución
        cursor.execute(sql, (nombre1, nombre2, apellido1, apellido2, correo, hashed_password, idRol))
    connection.commit()

def get_usuario_for_login(connection, correo):
    """Obtiene el id, la contraseña y el ROL de un usuario para el login."""
    with connection.cursor() as cursor:
        # Ahora también seleccionamos el 'idRol'
        sql = "SELECT idUsuario, contraseña, idRol FROM usuario WHERE correo = %s"
        cursor.execute(sql, (correo,))
        return cursor.fetchone()