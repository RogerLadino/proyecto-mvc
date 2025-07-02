# app/__init__.py
import pymysql.cursors
from flask import Flask
from config import Config
from flask_bcrypt import Bcrypt

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    connection = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )
    app.connection = connection

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