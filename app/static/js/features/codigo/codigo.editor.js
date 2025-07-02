ace.require("ace/ext/language_tools.js");

const editor = ace.edit("editor");
editor.setTheme("ace/theme/dracula");
editor.session.setMode("ace/mode/python");

editor.setOptions({
  enableBasicAutocompletion: true,
  enableLiveAutocompletion: true,
  enableSnippets: true
});

export const cambiarLenguaje = (lenguaje) => {
  editor.session.setMode("ace/mode/" + lenguaje);
}

export {
  editor
}