import { obtenerIdAula } from "../../db/aulas.db.js";
import { obtenerListaEjerciciosPorAula } from "../../db/ejercicios.db.js";
import { actualizarCodigoAula, actualizarNombreAula } from "../aulas/aula.handler.js";

const listaEjercicios = document.getElementById('lista-ejercicios-profesor');

const ejercicios = obtenerListaEjerciciosPorAula(obtenerIdAula());

for (let ejercicio of ejercicios) {
  listaEjercicios.innerHTML += `
        <div class="ejercicio">
          <i class="circulo icon-circle-empty icono-accent"></i>
          <p>${ejercicio.nombre}</p>
          <a class="icon-code icono-codigo icono-codigo-profesor" onmousedown="seleccionarEjercicio(${ejercicio.idEjercicio}, 'codigo-profesor.html')"></a>
          <a class="icon-right" onmousedown="seleccionarEjercicio(${ejercicio.idEjercicio}, 'ejercicio-profesor.html')"></a>
        </div>
      `
}

export const seleccionarEjercicio = (idEjercicio, href) => {
  localStorage.setItem("idEjercicio", idEjercicio);
  window.location.href = href;
}

actualizarCodigoAula()
actualizarNombreAula()

// Exportar la función para que esté disponible en el contexto global
window.seleccionarEjercicio = seleccionarEjercicio;