import { obtenerIdUsuario } from "../../db/usuarios.db.js";
import { obtenerEjercicio, obtenerIdEjercicio } from "../../db/ejercicios.db.js";
import { obtenerCodigoUsuario } from "../../db/codigo.db.js";

const ejercicio = obtenerEjercicio(obtenerIdEjercicio());

document.querySelector(".ejercicio-titulo").innerHTML = ejercicio.nombre;
document.querySelector(".descripcion-ejercicio").innerHTML = ejercicio.descripcion;
document.querySelector(".date-info").innerHTML = (ejercicio.fechaEntrega) ? `Fecha de entrega: ${ejercicio.fechaEntrega}` : "";

const codigo = obtenerCodigoUsuario(obtenerIdUsuario())

if (codigo != undefined) {
  document.querySelector(".score").innerHTML = `${codigo.notaObtenida}/100`;
}