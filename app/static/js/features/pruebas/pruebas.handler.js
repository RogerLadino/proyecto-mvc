import { parsearValorParametro, obtenerNombreDeTipoDeParametro } from "../../utils/parametros.js";
import { toggleDropdown } from "../../utils/dropdown.js";

const crearOpcionesSelect = (tipoSeleccionado) => {
  const tipos = ['int', 'string', 'float', 'boolean', 'json'];
  return tipos.map(tipo => `
    <option value="${tipo}" ${tipo === tipoSeleccionado ? 'selected' : ''}>${tipo.charAt(0).toUpperCase() + tipo.slice(1)}</option>
  `).join('');
};

const crearContenedorParametro = (tipoParametro, valorParametro) => `
  <div class="param-row parametro">
    <select class="param-select tipo-parametro">
      ${crearOpcionesSelect(tipoParametro)}
    </select>
    <div class="param-value-container">
      <input type="text" value="${valorParametro}" class="valor-parametro">
      <i class="icon-cancel" onmousedown="eliminarParametro(event)"></i>
    </div>
  </div>
`;

const crearSalidaHTML = (tipoParametro, valorRetorno) => `
  <div class="param-header">
    <span>Debe retornar</span>
  </div>
  <div class="param-grid">
    <div class="param-grid-header">
      <span>Tipo</span>
      <span>Valor</span>
    </div>
    <div class="param-row">
      <select class="param-select tipo-retorno">
        ${crearOpcionesSelect(tipoParametro)}
      </select>
      <div class="param-value-container">
        <input type="text" value="${valorRetorno}" class="valor-retorno">
      </div>
    </div>
  </div>
`;

export const obtenerParametrosDesdeHTML = (prueba) => {
  const parametros = Array.from(prueba.querySelectorAll('.parametro')).map(parametro => {
    const valorParametro = parametro.querySelector('.valor-parametro').value;
    const tipoParametro = parametro.querySelector('.tipo-parametro').value;
    return parsearValorParametro(tipoParametro, valorParametro);
  });
  return JSON.stringify(parametros);
};

export const obtenerSalidaDesdeHTML = (prueba) => {
  const valorRetorno = prueba.querySelector('.valor-retorno').value;
  const tipoParametro = prueba.querySelector('.tipo-retorno').value;
  return JSON.stringify(parsearValorParametro(tipoParametro, valorRetorno));
};

export const obtenerPruebas = () => {
  const pruebas = []

  document.querySelectorAll('.prueba').forEach(prueba => {

    const idPrueba = prueba.querySelector('.id-prueba') ? prueba.querySelector('.id-prueba').value : null;
    const nombreFuncion = prueba.querySelector('.nombre-funcion').value;
    const entrada = obtenerParametrosDesdeHTML(prueba);
    const salida = obtenerSalidaDesdeHTML(prueba);

    pruebas.push({ idPrueba, nombreFuncion, entrada, salida })
  });

  return pruebas
};

export const crearElementoPrueba = () => {
  const elemento = `
    <div class="test-accordion prueba">
      <div class="test-header">
        <div class="test-title">
          <span>Prueba</span>
        </div>
        <i class="icon-trash" onmousedown="eliminarElementoPrueba(event)"></i>
        <i class="icon-down-dir dropdown-toggle" onclick="toggleDropdown(event)"></i>
      </div>
      <div class="test-main-content">
        <div class="test-content">
          <div class="test-content">
            <div class="param-header">
              <span>Función</span>
            </div>
            <div class="param-grid">
              <div class="param-grid-header">
                <span>Nombre</span>
              </div>
              <div class="param-row">
                <input type="text" class="valor-parametro nombre-funcion" placeholder="Nombre de la función">
              </div>
            </div>
          </div>
        ${mostrarParametros('[]', '1')}
      </div>
    </div>
  `;
  document.querySelector('.pruebas').innerHTML += elemento;
};

export const mostrarParametros = (parametrosJSON, salidaJSON) => {
  const parametros = JSON.parse(parametrosJSON);
  const listaParametros = parametros.map(parametro => crearContenedorParametro(obtenerNombreDeTipoDeParametro(parametro), parametro)).join('');

  return `
    <div class="test-content">
      <div class="param-header">
        <span>Parámetros</span>
        <i class="icon-plus" onmousedown="crearElementoParametro(event)"></i>
      </div>
      <div class="param-grid parametros">
        <div class="param-grid-header">
          <span>Tipo</span>
          <span>Valor</span>
        </div>
        ${listaParametros}
      </div>
    </div>
    <div class="test-content">
      <div class="param-header">
        <span>Debe retornar</span>
      </div>
      <div class="param-grid">
        <div class="param-grid-header">
          <span>Tipo</span>
          <span>Valor</span>
        </div>
        <div class="param-row">
          <select class="param-select tipo-retorno">
            ${crearOpcionesSelect(obtenerNombreDeTipoDeParametro(JSON.parse(salidaJSON)))}
          </select>
          <div class="param-value-container">
            <input type="text" value="${JSON.parse(salidaJSON)}" class="valor-retorno valor-parametro ">
          </div>
        </div>
      </div>
    </div>
  `;
};

export const cargarPruebas = (pruebas) => {
  pruebas.forEach(prueba => {
    const elemento = `
      <div class="test-accordion prueba">
        <input name="idPrueba" type="hidden" class="id-prueba" style="display: none;" value="${prueba.idPrueba}">
        <div class="test-header">
          <div class="test-title">
            <span>Prueba</span>
          </div>
          <i class="icon-trash" onmousedown="eliminarElementoPrueba(event)"></i>
          <i class="icon-down-dir dropdown-toggle" onclick="toggleDropdown(event)"></i>
        </div>
        <div class="test-main-content">
          <div class="test-content">
            <div class="param-header">
              <span>Función</span>
            </div>
            <div class="param-grid">
              <div class="param-grid-header">
                <span>Nombre</span>
              </div>
              <div class="param-row">
                <input type="text" class="valor-parametro nombre-funcion" placeholder="Nombre de la función" value="${prueba.nombreFuncion}">
              </div>
            </div>
          </div>
          ${mostrarParametros(prueba.entrada, prueba.salida)}
        </div>
      </div>
    `;
    document.querySelector('.pruebas').innerHTML += elemento;
  });
};

export const eliminarElementoPrueba = (event) => {
  event.target.closest('.prueba').remove();
};

export const eliminarParametro = (event) => {
  event.target.closest('.parametro').remove();
}

export const crearElementoParametro = (event) => {
  const contenedor = event.target.closest('.test-content').querySelector('.parametros');
  contenedor.insertAdjacentHTML('beforeend', crearContenedorParametro('string', ''));
};

export const mostrarPruebas = () => {
  const pruebas = obtenerPruebasPorEjercicio(localStorage.getItem('idEjercicio'));
  const element = document.querySelector('.pruebas');

  pruebas.forEach(prueba => {
    const parametrosHTML = JSON.parse(prueba.entrada).map(parametro => `
      <div class="param-grid-header">
        <span>${obtenerNombreDeTipoDeParametro(parametro)}</span>
        <span>${parametro}</span>
      </div>
    `).join('');

    const salidaHTML = `
      <div class="param-header">
        <span>Debe retornar</span>
      </div>
      <div class="param-grid">
        <div class="param-grid-header">
          <span>Tipo</span>
          <span>Valor</span>
        </div>
        <div class="param-grid-header">
          <span>${obtenerNombreDeTipoDeParametro(JSON.parse(prueba.salida))}</span>
          <span>${JSON.parse(prueba.salida)}</span>
        </div>
      </div>
    `;

    const elemento = `
      <div class="test-accordion prueba">
        <div class="id-prueba" style="display: none;">${prueba.idPrueba}</div>
        <div class="test-header">
          <div class="test-title">
            <span>Prueba</span>
          </div>
          <i class="icon-down-dir dropdown-toggle" onclick="toggleDropdown(event)"></i>
        </div>
        <div class="test-main-content">
          <div class="test-content">
            <div class="param-header">
              <span>Función</span>
            </div>
            <div class="param-grid">
              <div class="param-grid-header">
                <span>Nombre</span>
              </div>
              <div class="param-grid-header">
                <span>${prueba.nombreFuncion}</span>
              </div>
            </div>
          </div>
          <div class="test-content">
            <div class="param-header">
              <span>Parámetros</span>
            </div>
            <div class="param-grid parametros">
              <div class="param-grid-header">
                <span>Tipo</span>
                <span>Valor</span>
              </div>
              ${parametrosHTML}
            </div>
          </div>
          <div class="test-content">
            ${salidaHTML}
          </div>
        </div>
      </div>
    `;
    element.innerHTML += elemento;
  });
};

window.toggleDropdown = toggleDropdown;
window.eliminarParametro = eliminarParametro