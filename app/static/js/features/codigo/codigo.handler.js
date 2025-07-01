import { editor } from "./codigo.editor.js";

const configurarTabs = () => {
  const tabs = document.querySelectorAll(".tab-container .editor-title-item");
  const tabContents = document.querySelectorAll(".tab-content > div");

  if (tabs.length === 0 || tabContents.length === 0) return;

  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => {
      activarTab(tabs, tabContents, index);
    });
  });

  activarTab(tabs, tabContents, 0);
};

const activarTab = (tabs, tabContents, index) => {
  tabs.forEach(t => {
    t.classList.remove("active-tab");
    const icon = t.querySelector("i");
    if (icon) icon.className = "icon-circle-empty icon-accent";
  });

  tabContents.forEach(content => content.style.display = "none");

  const tab = tabs[index];
  tab.classList.add("active-tab");
  const icon = tab.querySelector("i");
  if (icon) icon.className = "icon-circle icon-accent";

  tabContents[index].style.display = "flex";
};

export const mostrarResultadoConsola = (respuesta) => {
  const contenedor = document.querySelector('.console-info');
  if (!contenedor) return;

  let html = '';

  // Mostrar la salida general de consola si existe
  if (respuesta.print_codigo) {
    html += `
      <div class="test-accordion resultado-consola">
        <div class="test-header">
          <div class="test-title">
            <span>Consola global</span>
          </div>
          <i class="icon-down-dir dropdown-toggle" onclick="toggleDropdown(event)"></i>
        </div>
        <div class="test-main-content">
          <div class="test-content">
            <div class="param-header">
              <span>Salida de consola</span>
            </div>
            <div class="param-row">
              <pre>${respuesta.print_codigo}</pre>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  // Helper para mostrar valor y tipo
  const mostrarValorYTipo = (valor, tipo) => {
    // Si es array, mostrar como [ ... ]
    if (Array.isArray(valor)) {
      return `[ ${valor.join(', ')} ]  <span class="tipo-parametro">${tipo}</span>`;
    }
    return `
      <span class="valor-parametro">${tipo}</span>
      <span class="valor-parametro">${valor}</span>  
    `;
  };

  // Mostrar cada prueba como tarjeta tipo acordeón
  if (respuesta.detalles && Array.isArray(respuesta.detalles)) {
    respuesta.detalles.forEach(prueba => {
      const tipoEsperado = Array.isArray(prueba.salida_esperada) ? 'Array' : typeof prueba.salida_esperada;
      const tipoObtenido = Array.isArray(prueba.salida_obtenida) ? 'Array' : typeof prueba.salida_obtenida;

      html += `
        <div class="test-accordion resultado-prueba">
          <div class="test-header">
            <div class="test-title">
              <span>${prueba.nombre}</span>
            </div>
            <span class="test-status" style="margin-left:auto;${prueba.paso ? 'color:var(--success);' : 'color:var(--accent);'}">
              ${prueba.paso ? 'Pasada' : 'Fallida'}
            </span>
            <i class="icon-down-dir dropdown-toggle" onclick="toggleDropdown(event)"></i>
          </div>
          <div class="test-main-content">
            ${prueba.consola ? `
            <div class="test-content">
              <div class="param-header">
                <span>Consola</span>
              </div>
              <div class="param-row">
                <pre>${prueba.consola}</pre>
              </div>
            </div>` : ''}
            <div class="test-content">
              <div class="param-header">
                <span>Salida esperada</span>
              </div>
              <div class="param-grid">
              <div class="param-grid-header">
                <span>Tipo</span>
                <span>Valor</span>
              </div>
                <div class="param-row">
                  ${mostrarValorYTipo(prueba.salida_esperada, tipoEsperado)}
                </div>
              </div>
            </div>
            <div class="test-content">
              <div class="param-header">
                <span>Salida obtenida</span>
              </div>
              <div class="param-grid">
                <div class="param-grid-header">
                  <span>Tipo</span>
                  <span>Valor</span>
                </div>
                <div class="param-row">
                  ${mostrarValorYTipo(prueba.salida_obtenida, tipoObtenido)}
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
    });
  }

  contenedor.innerHTML = html;
};

export const configurarEjecutarCodigo = (path) => {
  document.getElementById("correr-codigo").addEventListener("click", async () => {
    try {
      const respuesta = await fetch(path, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          codigo: editor.getValue()
        })
      });

      const resultado = await respuesta.json();

      if (resultado.status == 'error') {
        alert(resultado.error)
      }
      else {
        mostrarResultadoConsola(resultado)
      }
    } catch (e) {
      alert(e)
    }
  });
}

export const mostrarInterfaz = () => {
  configurarTabs();
};