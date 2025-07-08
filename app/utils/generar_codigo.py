import random
import string

def generar_codigo(cantidadLetras=6):
    """Genera un código aleatorio con letras mayúsculas y minúsculas."""
    return ''.join(random.choices(string.ascii_letters, k=cantidadLetras))