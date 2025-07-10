import { editor } from './codigo.editor.js';

export const iniciarCodigoSocket = (idUsuario, idEjercicio) => {
  const socket = io();

  // Unirse a la sala
  socket.emit('join', { idUsuario, idEjercicio });

  let bloqueandoCambio = false;
  let temporizador = null;

  // Se espera 250 ms antes de enviar el código al servidor
  // para evitar enviar demasiados cambios
  editor.session.on('change', () => {
    if (bloqueandoCambio) return;

    clearTimeout(temporizador);

    temporizador = setTimeout(() => {
      socket.emit('actualizar_codigo', {
        idUsuario: idUsuario,
        idEjercicio: idEjercicio,
        codigo: editor.getValue()
      });
    }, 250);
  });

  // Recibir cambios desde otros clientes
  socket.on('actualizar_codigo', (data) => {
    bloqueandoCambio = true;
    editor.setValue(data.codigo, -1);
    bloqueandoCambio = false;
  });
}