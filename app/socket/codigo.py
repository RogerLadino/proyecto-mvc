from flask_socketio import join_room, emit
from app.models.codigo.codigo import actualizar_codigo

def codigo_sockets(socketio):
  @socketio.on('join')
  def manejar_join(data):
    idUsuario = data['idUsuario']
    idEjercicio = data['idEjercicio']

    room = f'codigo_{idEjercicio}_{idUsuario}'

    join_room(room)
  
  @socketio.on('actualizar_codigo')
  def manejar_actualizar_codigo(data):
    idUsuario = data['idUsuario']
    idEjercicio = data['idEjercicio']

    room = f'codigo_{idEjercicio}_{idUsuario}'
    
    codigo = data['codigo']

    actualizar_codigo(idUsuario, idEjercicio, codigo)

    emit('actualizar_codigo', {'codigo': codigo}, room=room, include_self=False)