# app/models/usuarios_model.py

def get_usuario_by_correo(connection, correo):
    """Busca si un correo ya existe en la base de datos."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT idUsuario FROM usuario WHERE correo = %s", (correo,))
        return cursor.fetchone()

def insert_usuario(connection, nombre1, nombre2, apellido1, apellido2, correo, hashed_password):
    """Inserta un nuevo usuario en la tabla 'usuario'."""
    with connection.cursor() as cursor:
        sql = """INSERT INTO usuario (nombre1, nombre2, apellido1, apellido2, correo, contraseña)
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (nombre1, nombre2, apellido1, apellido2, correo, hashed_password))
    connection.commit()

def get_usuario_for_login(connection, correo):
    """Obtiene el id y la contraseña hasheada de un usuario para el login."""
    with connection.cursor() as cursor:
        # Seleccionamos el id y la contraseña para la verificación
        cursor.execute("SELECT idUsuario, contraseña FROM usuario WHERE correo = %s", (correo,))
        return cursor.fetchone()