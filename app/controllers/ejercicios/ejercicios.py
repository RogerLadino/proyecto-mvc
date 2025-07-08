from flask import Blueprint, render_template, request, redirect, url_for, session
import json

from app.utils.generar_codigo import generar_codigo
from app.models.ejercicios.ejercicios import (insertar_ejercicio, consultar_ejercicio, editar_ejercicio, eliminar_ejercicio, consultar_estadisticas_ejercicio, consultar_ejercicios_por_aula)
from app.models.pruebas.pruebas import (insertar_prueba, consultar_pruebas, editar_prueba)
from app.models.codigo.codigo import (consultar_codigo, darNota, insertar_codigo)
from app.services.usuario import (obtener_sesion_id_usuario)
from app.models.aulas.aulas import (es_profesor, consultar_aula, actualizar_codigo_aula)

ejercicios_bp = Blueprint('ejercicios_bp', __name__)

@ejercicios_bp.route('/aulas/<id_aula>/ejercicios', methods=['GET'])
def ejercicios(id_aula):
  idUsuario = obtener_sesion_id_usuario()

  ejercicios = consultar_ejercicios_por_aula(id_aula)

  aula = consultar_aula(id_aula)
  
  if es_profesor(idUsuario, id_aula):
    return render_template('ejercicios/lista-ejercicios-profesor.html', id_aula=id_aula, ejercicios=ejercicios, aula=aula)

  return render_template('ejercicios/lista-ejercicios.html', id_aula=id_aula, ejercicios=ejercicios, aula=aula)

@ejercicios_bp.route('/aulas/<id_aula>/ejercicios/<id_ejercicio>', methods=['GET'])
def ejercicio(id_aula, id_ejercicio):
  idUsuario = obtener_sesion_id_usuario()

  ejercicio = consultar_ejercicio(id_ejercicio)

  if es_profesor(idUsuario, id_aula):
    estadisticas = consultar_estadisticas_ejercicio(id_ejercicio, id_aula) 
    
    return render_template('ejercicios/ejercicio-profesor.html', id_aula=id_aula, id_ejercicio=id_ejercicio, estadisticas=estadisticas, ejercicio=ejercicio)

  codigo = consultar_codigo(idUsuario, id_ejercicio)
  
  return render_template('ejercicios/ejercicio.html', ejercicio=ejercicio, codigo=codigo, id_aula=id_aula, id_ejercicio=id_ejercicio)

@ejercicios_bp.route('/aulas/<id_aula>/ejercicios/crear', methods=['GET', 'POST'])
def crear(id_aula):
  if request.method == 'POST':
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    codigoInicial = request.form['codigo']
    fechaEntrega = request.form['fecha']
    pruebasJson = request.form.get('pruebas', None)

    try:
      idEjercicio = insertar_ejercicio(id_aula, nombre, descripcion, codigoInicial, fechaEntrega)
    
      if pruebasJson is not None:
        pruebas = json.loads(pruebasJson)
        
        for prueba in pruebas:
          insertar_prueba(idEjercicio, prueba['nombreFuncion'], prueba['entrada'], prueba['salida'])
    except Exception as e:
      print('An error has ocurried ', str(e))
    
    return redirect(url_for('ejercicios_bp.ejercicio', id_aula=id_aula, id_ejercicio=idEjercicio))

  return render_template('ejercicios/crear-ejercicio.html', id_aula=id_aula)

@ejercicios_bp.route('/aulas/<id_aula>/ejercicios/<id_ejercicio>/editar', methods=['GET', 'POST'])
def editar(id_aula, id_ejercicio):
  if request.method == 'POST':
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    codigoInicial = request.form['codigo']
    fechaEntrega = request.form['fecha']
    pruebasJson = request.form.get('pruebas', None)

    try:
      editar_ejercicio(id_ejercicio, nombre, descripcion, codigoInicial, fechaEntrega)
      
      if pruebasJson is not None:
        pruebas = json.loads(pruebasJson)
        
        for prueba in pruebas:
          if 'idPrueba' in prueba and prueba['idPrueba'] != '':
            editar_prueba(prueba['idPrueba'], prueba['nombreFuncion'], prueba['entrada'], prueba['salida'])
          else:
            insertar_prueba(id_ejercicio, prueba['nombreFuncion'], prueba['entrada'], prueba['salida'])
    except Exception as e:
      print('An error has ocurried ', str(e))

    return redirect(url_for('ejercicios_bp.ejercicio', id_aula=id_aula, id_ejercicio=id_ejercicio))
  
  ejercicio = consultar_ejercicio(id_ejercicio)

  pruebas = consultar_pruebas(id_ejercicio) 
  
  return render_template('ejercicios/editar-ejercicio.html', ejercicio=ejercicio, pruebas=pruebas, id_aula=id_aula, id_ejercicio=id_ejercicio)

@ejercicios_bp.route('/aulas/<id_aula>/ejercicios/<id_ejercicio>/guardar-notas', methods=['POST'])
def guardar_notas(id_aula, id_ejercicio):
  usuarios = request.form.getlist('id_usuario')
  
  for idUsuario in usuarios:
    nota = request.form.get(f'nota-{idUsuario}', 0)

    codigo = consultar_codigo(idUsuario, id_ejercicio)
    
    # Si el idCodigo es vacío, significa que no hay código asociado al usuario
    if codigo is None:
      try:
        # Insertar un nuevo código para el usuario
        insertar_codigo(idUsuario, id_ejercicio, nota)
      except Exception as e:
        print('An error has ocurried ', str(e))
    else:
      try:
        darNota(idUsuario, id_ejercicio,nota)
      except Exception as e:
        print('An error has ocurried ', str(e))

  return redirect(url_for('ejercicios_bp.ejercicio', id_aula=id_aula, id_ejercicio=id_ejercicio))

@ejercicios_bp.route('/aulas/<id_aula>/ejercicios/<id_ejercicio>/eliminar', methods=['GET', 'POST'])
def eliminar(id_aula, id_ejercicio):
  try:
    eliminar_ejercicio(id_ejercicio)
  except Exception as e:
    print('An error has ocurried ', str(e))

  return redirect(url_for('ejercicios_bp.ejercicios', id_aula=id_aula))

@ejercicios_bp.route('/aulas/<id_aula>/actualizar-codigo', methods=['GET'])
def actualizar_codigo(id_aula):
  codigo = generar_codigo(6)
  
  actualizar_codigo_aula(id_aula, codigo)

  return redirect(url_for('ejercicios_bp.ejercicios', id_aula=id_aula))