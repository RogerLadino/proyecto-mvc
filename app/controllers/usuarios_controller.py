# app/controllers/usuarios_controller.py

from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash, session
from flask_bcrypt import Bcrypt

from ..models.usuarios_model import get_usuario_by_correo, insert_usuario, get_usuario_for_login

usuario_bp = Blueprint('usuario_bp', __name__, url_prefix='/usuario', template_folder='../../templates')
bcrypt = Bcrypt()

@usuario_bp.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        # --- Obtener la conexión a la base de datos ---
        connection = current_app.connection

        # --- Obtener datos del formulario ---
        nombre1 = request.form.get('nombre1')
        nombre2 = request.form.get('nombre2')
        apellido1 = request.form.get('apellido1')
        apellido2 = request.form.get('apellido2')
        correo = request.form.get('email')
        password = request.form.get('password')
        
        # --- OBTENER EL ROL SELECCIONADO ---
        rol = request.form.get('rol')

        # --- Validaciones ---
        # Se añade 'rol' a la validación para asegurar que se seleccione uno.
        if not all([nombre1, apellido1, correo, password, rol]):
            flash('Todos los campos son obligatorios, incluyendo el rol.', 'danger')
            return redirect(url_for('usuario_bp.registrar'))

        # Verificar si el correo ya existe usando tu función
        if get_usuario_by_correo(connection, correo):
            flash('El correo electrónico ya está registrado.', 'danger')
            return redirect(url_for('usuario_bp.registrar'))

        # Hashear la contraseña
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # --- Llamar a tu función para insertar el usuario, AHORA CON EL ROL ---
        try:
            # ¡IMPORTANTE! Debes asegurarte de que tu función 'insert_usuario'
            # ahora acepte el parámetro 'idRol'.
            insert_usuario(
                connection=connection,
                nombre1=nombre1,
                nombre2=nombre2,
                apellido1=apellido1,
                apellido2=apellido2,
                correo=correo,
                hashed_password=hashed_password,
                idRol=rol  # <-- Aquí pasamos el nuevo dato
            )
            flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('usuario_bp.iniciar_sesion'))
        except Exception as e:
            # Es una buena práctica registrar el error real
            print(f"Error en la inserción: {e}")
            flash('Ocurrió un error al intentar registrar el usuario.', 'danger')
            return redirect(url_for('usuario_bp.registrar'))

    return render_template('register.html')

@usuario_bp.route('/iniciar-sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        correo = request.form.get('email')
        password = request.form.get('password')
        connection = current_app.connection

        user_data = get_usuario_for_login(connection, correo)

        if user_data and bcrypt.check_password_hash(user_data['contraseña'], password):
            session.clear()
            session['id_usuario'] = user_data['idUsuario']
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('usuario_bp.dashboard'))
        else:
            flash('Correo o contraseña incorrectos.', 'danger')
            return redirect(url_for('usuario_bp.iniciar_sesion'))

    return render_template('login.html')

@usuario_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para ver esta página.', 'warning')
        return redirect(url_for('usuario_bp.iniciar_sesion'))
    
    return f"<h1>Bienvenido al Dashboard! Tu ID de usuario en la sesión es: {session['user_id']}</h1>"