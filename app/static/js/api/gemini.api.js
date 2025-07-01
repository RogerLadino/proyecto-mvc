const mensajes = [] // { role: "user" | "model", text: string }

const API_KEY = "AIzaSyBpYhCDH81k2t-_92hVlHTI5LfGftgt1WA"

const systemPrompt = `
    Eres un asistente de programación amigable diseñado para ayudar a estudiantes a resolver desafíos de código por sí mismos. 
    No debes proporcionar la solución directamente.
    Da pistas muy cautelosas que inviten a pensar, no soluciones. 
    También puedes explicar conceptos si el estudiante lo pide, usando un lenguaje claro, con ejemplos simples. 
    Evita explicaciones innecesariamente largas. 
    Responde de forma corta, precisa, enfocada y didáctica, sin extenderte demasiado. 
    Sé amigable y respetuoso. Quieres motivar al estudiante
`


export const pedirAnalisisDeCodigo = async (codigo, ejercicio, mensajeUsuario) => {
    const URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${API_KEY}`

    const mensajesPreviosEstructurados = mensajes.map(m => ({
        role: m.role,
        parts: [{ text: m.text }]
    }));

    const mensajesBase = [
        {
            role: "model",
            parts: [
                { text: systemPrompt }
            ]
        },
        {
            role: "model",
            parts: [
                { text: `Este es el código del estudiante: \n\n${codigo}` }
            ]
        },
        {
            role: "model",
            parts: [
                { text: `Este es el enunciado del ejercicio: \n\n${ejercicio}` }
            ]
        }
    ];

    const mensajeActual = {
        role: "user",
        parts: [{ text: mensajeUsuario }]
    };

    const mensajesPeticion = [
        ...mensajesBase,
        ...mensajesPreviosEstructurados,
        mensajeActual
    ];

    const response = await fetch(URL, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            contents: mensajesPeticion
        })
    });

    const responseJSON = await response.json();
    const text = responseJSON.candidates[0].content.parts[0].text;

    mensajes.push({ role: "user", text: mensajeUsuario });
    mensajes.push({ role: "model", text });

    return text;
}