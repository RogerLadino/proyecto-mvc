from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
import json

from app.models.ejercicios.ejercicios import (consultar_ejercicio)
from app.models.pruebas.pruebas import (consultar_pruebas)
from app.models.codigo.codigo import (consultar_usuarios_con_codigo, consultar_codigo, insertar_codigo, consultar_usuario_con_codigo, consultar_codigo_por_id)
from app.services.codigo import (ejecutar_codigo_usuario, ejecutar_pruebas)
from app.models.aulas.aulas import (es_profesor, consultar_aula)
from app.services.usuario import (obtener_sesion_id_usuario)

codigo_bp = Blueprint('codigo_bp', __name__)

@codigo_bp.route('/aulas/<id_aula>/ejercicios/<id_ejercicio>/codigo/<id_codigo>', methods=['GET'])
def codigo(id_aula, id_ejercicio, id_codigo):
  id_usuario = obtener_sesion_id_usuario()
  
  ejercicio = consultar_ejercicio(id_ejercicio)
  
  pruebas = consultar_pruebas(id_ejercicio)

  usuarios = consultar_usuarios_con_codigo(id_ejercicio)

  usuario = consultar_usuario_con_codigo(id_codigo)

  codigo = consultar_codigo_por_id(id_codigo)

  # Si no tiene un registro de 'codigo' se crea.
  codigoUsuario = consultar_codigo(id_usuario, id_ejercicio)

  if not codigoUsuario:
    insertar_codigo(id_usuario, id_ejercicio)
  
  # Los usuarios que podrá ver el profesor son todos
  esProfesor = es_profesor(id_usuario, id_aula)
  if esProfesor:
    return render_template('codigo/codigo-profesor.html', ejercicio=ejercicio, pruebas=pruebas, usuarios=usuarios, codigo=codigo, usuario=usuario, id_aula=id_aula, id_ejercicio=id_ejercicio, id_codigo=id_codigo)

  # Los usuarios que podrá ver el alumno será sólo él mismo y el profesor (si tienen registros)
  aula = consultar_aula(id_aula)
  
  usuarios_filtrados = [u for u in usuarios if u['idUsuario'] == aula['idUsuario'] or id_usuario == u['idUsuario']]
  
  return render_template('codigo/codigo.html', ejercicio=ejercicio, pruebas=pruebas, codigo=codigo, usuarios=usuarios_filtrados, usuario=usuario, id_aula=id_aula, id_ejercicio=id_ejercicio, id_codigo=id_codigo)

@codigo_bp.route("/aulas/<id_aula>/ejercicios/<id_ejercicio>/codigo/<id_codigo>/ejecutar", methods=["POST"])
def ejecutar_codigo(id_aula, id_codigo, id_ejercicio):
  datos = request.get_json()
  codigo = datos.get("codigo", "")
  
  pruebas_db = consultar_pruebas(id_ejercicio)

  pruebas = []

  for prueba in pruebas_db:
    pruebas.append({
      "nombreFuncion": prueba["nombreFuncion"],
      "entrada": json.loads(prueba["entrada"]),
      "salida": json.loads(prueba["salida"])
    })

  respuesta = ejecutar_codigo_usuario(codigo)

  # Hubo un error al ejecutar el código (sintaxis)
  if respuesta["status"] != "ok":
    return jsonify(respuesta), 400

  entorno = respuesta["entorno"]
  print_del_codigo = respuesta["consola"]

  if pruebas:
    resultado = ejecutar_pruebas(pruebas, entorno)
    resultado["print_codigo"] = print_del_codigo 

  return jsonify(resultado)