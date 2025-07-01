  // Esta función toma el tipo de parámetro y el valor del parámetro y lo convierte al tipo correspondiente
  // Si el tipo de parámetro es int, lo convierte a un número entero
export const parsearValorParametro = (tipoParametro, valorParametro) => {
  switch (tipoParametro) {
    case 'int':
      return parseInt(valorParametro);

    case 'float':
      return parseFloat(valorParametro);

    case 'string':
      return String(valorParametro);

    case 'boolean':
      return valorParametro === 'true' || valorParametro === true || valorParametro === 1 || valorParametro === '1';

    case 'json':
      return typeof valorParametro === 'string' ? JSON.parse(valorParametro) : valorParametro;
  }
}


// Esta función toma el valor del parámetro y devuelve el tipo de parámetro correspondiente
// Si el valor es un número entero, devuelve 'int'
export const obtenerNombreDeTipoDeParametro = (valor) => {

  if (typeof valor === 'string') {
    return 'string';
  }

  if (typeof valor === 'number') {
    if (Number.isInteger(valor)) {
      return 'int';
    } else {
      return 'float';
    }
  }

  if (typeof valor === 'object' && valor !== null && !Array.isArray(valor)) {
    return 'json';
  }

  if (typeof valor === 'boolean') {
    return 'boolean';
  }
}