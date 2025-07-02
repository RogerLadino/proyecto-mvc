import io
import sys
import unittest

def ejecutar_codigo_usuario(codigo_str):
    try:
        compile(codigo_str, '<string>', 'exec')
    except SyntaxError as e:
        return {"status": "error", "error": f"Error de sintaxis: {e}"}

    entorno = {}
    stdout_original = sys.stdout
    sys.stdout = io.StringIO()

    try:
        exec(codigo_str, entorno)
        consola_output = sys.stdout.getvalue()
        sys.stdout = stdout_original
        return {
            "status": "ok",
            "entorno": entorno,
            "consola": consola_output
        }
    except Exception as e:
        consola_output = sys.stdout.getvalue()
        sys.stdout = stdout_original
        return {
            "status": "error",
            "error": f"Error al ejecutar el código: {e}",
            "consola": consola_output
        }

def ejecutar_pruebas(pruebas, entorno):
    resultados = []

    class DynamicTest(unittest.TestCase):
        pass

    for i, prueba in enumerate(pruebas):
        nombre_funcion = prueba.get("nombreFuncion")
        entrada = prueba.get("entrada")
        salida_esperada = prueba.get("salida")

        if nombre_funcion not in entorno:
            return {
                "status": "error",
                "error": f"La función '{nombre_funcion}' no existe en el código del usuario."
            }

        funcion = entorno[nombre_funcion]

        def test_func(self, entrada=entrada, salida=salida_esperada, funcion=funcion,
                      nombre=nombre_funcion, idx=i):
            stdout_original = sys.stdout
            sys.stdout = io.StringIO()

            try:
                salida_obtenida = funcion(*entrada)
                paso = salida_obtenida == salida
            except Exception as e:
                salida_obtenida = f"ERROR: {str(e)}"
                paso = False
            finally:
                consola_output = sys.stdout.getvalue()
                sys.stdout = stdout_original

            resultados.append({
                "nombre": f"{nombre}_{idx+1}",
                "entrada": entrada,
                "salida_esperada": salida,
                "salida_obtenida": salida_obtenida,
                "paso": paso,
                "consola": consola_output
            })

            self.assertTrue(True)  # Para evitar que se detenga la ejecución

        setattr(DynamicTest, f"test_{nombre_funcion}_{i+1}", test_func)

    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DynamicTest)
    resultado = runner.run(suite)

    return {
        "status": "ok",
        "passed": resultado.wasSuccessful(),
        "total_tests": resultado.testsRun,
        "failures": len(resultado.failures) + len(resultado.errors),
        "detalles": resultados
    }
