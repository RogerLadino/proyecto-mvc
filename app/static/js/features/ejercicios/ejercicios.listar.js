import { obtenerListaEjerciciosPorAula } from "../../db/ejercicios.db.js";
import { actualizarNombreAula } from "../aulas/aula.handler.js";

const ejercicios = obtenerListaEjerciciosPorAula(localStorage.getItem("idAula"));
const listaEjercicios = document.getElementById('lista-ejercicios');

ejercicios.forEach(ejercicio => {
  listaEjercicios.innerHTML += `
      <div class="ejercicio">
        <i class="circulo icon-circle-empty icono-success"></i>
        <p>${ejercicio.nombre}</p>
        <p class="fecha">${ejercicio.fechaEntrega}</p>
        <a class="icon-code icono-codigo" onmousedown="seleccionarEjercicio(${ejercicio.idEjercicio}, 'codigo.html')"></a>
        <a class="icon-right" onmousedown="seleccionarEjercicio(${ejercicio.idEjercicio}, 'ejercicio.html')"></a>
      </div>
    `
});

const seleccionarEjercicio = (idEjercicio, href) => {
  localStorage.setItem("idEjercicio", idEjercicio);
  window.location.href = href;
}

actualizarNombreAula()

// Exportar la función para que esté disponible en el contexto global
window.seleccionarEjercicio = seleccionarEjercicio;