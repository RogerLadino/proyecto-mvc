from flask import Flask
from flask_socketio import SocketIO
import pymysql.cursors
from config import Config
from app.socket.codigo import codigo_sockets

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)

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

    return app
