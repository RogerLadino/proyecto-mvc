# app/__init__.py
from flask import Flask, app
from flask_socketio import SocketIO
import pymysql.cursors
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
from config import Config
from app.socket.codigo import codigo_sockets

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # --- Inicialización de extensiones ---
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
    bcrypt = Bcrypt(app) # Se asigna a una variable por convención

    # --- Configuración de la base de datos ---
    connection = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )
    # Hacemos la conexión y socketio accesibles en la app
    app.connection = connection
    app.socketio = socketio

    # --- Registro de Sockets ---
    codigo_sockets(socketio)
    
    # --- Registro de Blueprints (organizado en un solo lugar) ---
    from app.controllers.main import main_bp
    from app.controllers.usuarios_controller import usuario_bp
    from app.controllers.ejercicios.ejercicios import ejercicios_bp
    from app.controllers.codigo.codigo import codigo_bp
    from app.controllers.reportes.reportes_controller import reportes_bp 
    
    app.register_blueprint(main_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(ejercicios_bp)
    app.register_blueprint(codigo_bp)
    app.register_blueprint(reportes_bp) 
    
    Bcrypt(app)

    with app.app_context():
        # Aquí registramos nuestro controlador
        from .controllers.usuarios_controller import usuario_bp
        app.register_blueprint(usuario_bp)

    return app
