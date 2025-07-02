# app/controllers/usuarios_controller.py

from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash, session
from flask_bcrypt import Bcrypt

from ..models.usuarios_model import get_usuario_by_correo, insert_usuario, get_usuario_for_login

usuario_bp = Blueprint('usuario_bp', __name__, url_prefix='/usuario', template_folder='../../templates')
bcrypt = Bcrypt()

@usuario_bp.route('/registrar', methods=['GET', 'POST'])
def registrar():
    # ... (código de registro sin cambios) ...
    connection = current_app.connection
    if request.method == 'POST':
        correo = request.form.get('email')
        if get_usuario_by_correo(connection, correo):
            flash('El correo electrónico ya está registrado.', 'danger')
            return redirect(url_for('usuario_bp.registrar'))
        hashed_password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
        insert_usuario(
            connection=connection,
            nombre1=request.form.get('nombre1'),
            nombre2=request.form.get('nombre2'),
            apellido1=request.form.get('apellido1'),
            apellido2=request.form.get('apellido2'),
            correo=correo,
            hashed_password=hashed_password
        )
        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('usuario_bp.iniciar_sesion'))
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
            session['user_id'] = user_data['idUsuario']
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