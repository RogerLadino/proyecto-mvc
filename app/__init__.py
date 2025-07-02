# app/__init__.py
from flask import Flask
from flask_socketio import SocketIO
import pymysql.cursors
from flask import Flask
from config import Config
from flask_bcrypt import Bcrypt
from app.socket.codigo import codigo_sockets

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

    codigo_sockets(socketio)
    
    connection = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )
    app.connection = connection
    app.socketio = socketio

    from app.controllers.ejercicios.ejercicios import ejercicios_bp
    from app.controllers.codigo.codigo import codigo_bp
    
    app.register_blueprint(ejercicios_bp)
    app.register_blueprint(codigo_bp)

    Bcrypt(app)

    # Registrar Blueprints
    with app.app_context():
        from .controllers.main import main_bp
        app.register_blueprint(main_bp)

    with app.app_context():
        # Aquí registramos nuestro controlador
        from .controllers.usuarios_controller import usuario_bp
        app.register_blueprint(usuario_bp)

    # Registrar Blueprints
        with app.app_context():
            from .controllers.main import main_bp
            app.register_blueprint(main_bp)
        
    return app