from flask_socketio import join_room, emit
from app.models.codigo.codigo import actualizar_codigo

def codigo_sockets(socketio):
  @socketio.on('join')
  def manejar_join(data):
    room = data['idCodigo']

    join_room(room)
  
  @socketio.on('actualizar_codigo')
  def manejar_actualizar_codigo(data):
    idCodigo = data['idCodigo']

    codigo = data['codigo']

    actualizar_codigo(idCodigo, codigo)

    emit('actualizar_codigo', {'codigo': codigo}, room=idCodigo, include_self=False)