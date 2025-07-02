import { obtenerPruebas, cargarPruebas, crearElementoPrueba, crearElementoParametro, eliminarElementoPrueba } from "../pruebas/pruebas.handler.js";

const formulario = document.getElementById('form')

formulario.addEventListener('submit', (e) => {
  // Se crea un elemento oculto que tiene el valor las pruebas por formato JSON
  // El servidor recibe la lista de pruebas "pruebas" en formato JSON.

  const campo = document.createElement('input');
  campo.setAttribute('type', 'hidden');
  campo.setAttribute('name', 'pruebas');
  campo.setAttribute('value', JSON.stringify(obtenerPruebas()));

  formulario.appendChild(campo);
})

// Se usa window para que la función sea accesible desde el HTML
window.crearElementoPrueba = crearElementoPrueba
window.crearElementoParametro = crearElementoParametro
window.eliminarElementoPrueba = eliminarElementoPrueba
window.cargarPruebas = cargarPruebas