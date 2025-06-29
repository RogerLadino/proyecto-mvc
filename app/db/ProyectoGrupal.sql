CREATE DATABASE ProyectoGrupal;

USE ProyectoGrupal;

-- Tabla: usuario
CREATE TABLE usuario (
    idUsuario INT AUTO_INCREMENT NOT NULL,
    correo VARCHAR(45) NOT NULL,
    nombre1 VARCHAR(45) NOT NULL,
    nombre2 VARCHAR(45),
    apellido1 VARCHAR(45) NOT NULL,
    apellido2 VARCHAR(45),
    contraseña VARCHAR(128) NOT NULL,
    PRIMARY KEY (idUsuario)
);

-- Tabla: aula
CREATE TABLE aula (
    idAula INT AUTO_INCREMENT NOT NULL,
    nombre VARCHAR(45) NOT NULL,
    codigo VARCHAR(20) NOT NULL,
    idUsuario INT NOT NULL,
    PRIMARY KEY (idAula),
    FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario)
);

-- Tabla intermedia: usuario_has_aula
CREATE TABLE usuario_has_aula (
    idUsuario INT NOT NULL,
    idAula INT NOT NULL,
    PRIMARY KEY (idUsuario,idAula),
    FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario),
    FOREIGN KEY (idAula) REFERENCES aula(idAula)
);

-- Tabla: tipoLenguaje
CREATE TABLE tipoLenguaje (
    idTipoLenguaje VARCHAR(50) NOT NULL,
    nombre VARCHAR(45) NOT NULL,
    descripcion TEXT,
    PRIMARY KEY (idTipoLenguaje)
);

-- Tabla: ejercicio
CREATE TABLE ejercicio (
    idEjercicio INT AUTO_INCREMENT NOT NULL,
    nombre VARCHAR(45) NOT NULL,
    descripcion TEXT,
    codigoInicial TEXT,
    fechaEntrega DATE,
    fechaCreacion DATE DEFAULT CURRENT_DATE,
    idAula INT NOT NULL,
    idTipoLenguaje VARCHAR(50) NOT NULL,
    PRIMARY KEY (idEjercicio),
    FOREIGN KEY (idAula) REFERENCES aula(idAula),
    FOREIGN KEY (idTipoLenguaje) REFERENCES tipoLenguaje(idTipoLenguaje)
);

-- Tabla: prueba
CREATE TABLE prueba (
    idPrueba INT AUTO_INCREMENT NOT NULL,
    nombreFuncion TEXT NOT NULL,
    entrada JSON NOT NULL,
    salida JSON NOT NULL,
    idEjercicio INT NOT NULL,
    PRIMARY KEY (idPrueba),
    FOREIGN KEY (idEjercicio) REFERENCES ejercicio(idEjercicio)
);

-- Tabla: codigo
CREATE TABLE codigo (
    idCodigo INT AUTO_INCREMENT NOT NULL,
    codigo TEXT NOT NULL,
    notaObtenida FLOAT,
    fechaEntrega DATE NOT NULL,
    intentosRealizados INT NOT NULL,
    resuelto TINYINT NOT NULL,
    idTipoLenguaje VARCHAR(50) NOT NULL,
    idUsuario INT NOT NULL,
    idEjercicio INT NOT NULL,
    PRIMARY KEY (idCodigo),
    FOREIGN KEY (idTipoLenguaje) REFERENCES tipoLenguaje(idTipoLenguaje),
    FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario),
    FOREIGN KEY (idEjercicio) REFERENCES ejercicio(idEjercicio)
);