import { obtenerUsuariosEnAula } from '../../db/aulas.db.js';
import { obtenerListaCodigosPorAula } from '../../db/codigo.db.js';
import { obtenerListaEjerciciosPorAula } from '../../db/ejercicios.db.js';

const crearFilaReporte = (usuario, codigos, ejercicios) => {
  const filasCodigos = ejercicios.map(ejercicio => {
    const codigo = codigos.find(c => c.idEjercicio === ejercicio.idEjercicio) || {};
    return `
      <td>
        <div class="statistic">
          <p class="nota">${codigo.notaObtenida || '0'}/100</p>
          <i class="icon-cancel checkmark icon-warning reporte-x-icon"></i>
          <p class="attempts">${codigo.intentosRealizados || 0}</p>
          <i class="icon-clock clock"></i>
        </div>
      </td>
    `;
  }).join('');

  return `
    <tr class="table-row">
      <td>
        <i class="icon-circle ${usuario.esProfesor ? 'icon-success' : 'icon-accent'}"></i>
        ${usuario.nombre1} ${usuario.apellido1}
      </td>
      ${filasCodigos}
    </tr>
  `;
};

const renderizarTitulosEjercicios = (ejercicios) => {
  const tableHeader = document.querySelector('.exercise-table thead .table-header');
  tableHeader.innerHTML = `
    <th>Nombre</th>
    ${ejercicios.map(ejercicio => `
      <th>
        <i class="icon-circle-empty icon-accent"></i>
        ${ejercicio.nombre}
      </th>
    `).join('')}
  `;
};

const renderizarTablaReportes = () => {
  const usuarios = obtenerUsuariosEnAula();
  const codigos = obtenerListaCodigosPorAula();
  const ejercicios = obtenerListaEjerciciosPorAula(); 

  renderizarTitulosEjercicios(ejercicios);

  const tableBody = document.querySelector('.exercise-table tbody');
  tableBody.innerHTML = usuarios.map(usuario => {
    const codigosUsuario = codigos.filter(codigo => codigo.idUsuario === usuario.idUsuario);
    return crearFilaReporte(usuario, codigosUsuario, ejercicios);
  }).join('');
};

// Función para inicializar la página de reportes
const inicializarReportes = () => {
  renderizarTablaReportes();
};

// Ejecutar la inicialización al cargar el script
document.addEventListener('DOMContentLoaded', inicializarReportes);