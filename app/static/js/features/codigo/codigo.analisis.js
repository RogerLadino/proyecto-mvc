import { marked } from '../../lib/marked/marked.esm.js'
import { pedirAnalisisDeCodigo } from '../../api/gemini.api.js'
import { editor } from './codigo.editor.js'

let waiting = false

const agregarMensaje = (tipoUsuario, mensaje) => {
    const p = document.createElement("div");
    p.className = `message ${tipoUsuario}`;
    p.innerHTML = marked.parse(mensaje);
    document.querySelector(".messages").appendChild(p);
};

document.querySelector('.chat').addEventListener("submit", async (e) => {
    e.preventDefault()

    if (waiting) return

    const input = document.querySelector(".chat-input")
    const mensaje = input.value.trim()

    if (mensaje.length > 0) {
        input.value = ""

        agregarMensaje('user', mensaje)

        const codigo = editor.getValue()

        const descripcion = document.querySelector('.descripcion-ejercicio').innerHTML

        waiting = true

        const response = await pedirAnalisisDeCodigo(codigo, descripcion, mensaje)

        waiting = false

        agregarMensaje('agent', response)
    }
})