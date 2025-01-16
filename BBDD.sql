-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS AcademiaIdiomas;
USE AcademiaIdiomas;

-- Tabla de Estudiantes
CREATE TABLE IF NOT EXISTS Estudiantes (
    EstudianteID INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Apellido VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Telefono VARCHAR(15),
    FechaRegistro DATE DEFAULT CURRENT_DATE
);

-- Tabla de Profesores
CREATE TABLE IF NOT EXISTS Profesores (
    ProfesorID INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Apellido VARCHAR(100) NOT NULL,
    Especialidad VARCHAR(50),
    Email VARCHAR(100) UNIQUE NOT NULL,
    Telefono VARCHAR(15)
);

-- Tabla de Cursos
CREATE TABLE IF NOT EXISTS Cursos (
    CursoID INT AUTO_INCREMENT PRIMARY KEY,
    NombreCurso VARCHAR(100) NOT NULL,
    Idioma VARCHAR(50) NOT NULL,
    Nivel ENUM('Básico', 'Intermedio', 'Avanzado') NOT NULL,
    Precio DECIMAL(10, 2) NOT NULL,
    ProfesorID INT,
    FOREIGN KEY (ProfesorID) REFERENCES Profesores(ProfesorID) ON DELETE SET NULL
);

-- Tabla de Inscripciones
CREATE TABLE IF NOT EXISTS Inscripciones (
    InscripcionID INT AUTO_INCREMENT PRIMARY KEY,
    EstudianteID INT,
    CursoID INT,
    FechaInscripcion DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (EstudianteID) REFERENCES Estudiantes(EstudianteID) ON DELETE CASCADE,
    FOREIGN KEY (CursoID) REFERENCES Cursos(CursoID) ON DELETE CASCADE
);

-- Insertar algunos datos de ejemplo en Profesores
INSERT INTO Profesores (Nombre, Apellido, Especialidad, Email, Telefono)
VALUES 
('Carlos', 'López', 'Inglés', 'carlos.lopez@academia.com', '123456789'),
('María', 'Gómez', 'Francés', 'maria.gomez@academia.com', '987654321');

-- Insertar algunos datos de ejemplo en Cursos
INSERT INTO Cursos (NombreCurso, Idioma, Nivel, Precio, ProfesorID)
VALUES 
('Inglés Básico', 'Inglés', 'Básico', 150.00, 1),
('Francés Intermedio', 'Francés', 'Intermedio', 200.00, 2),
('Inglés Avanzado', 'Inglés', 'Avanzado', 250.00, 1);

-- Insertar algunos datos de ejemplo en Estudiantes
INSERT INTO Estudiantes (Nombre, Apellido, Email, Telefono)
VALUES 
('Juan', 'Pérez', 'juan.perez@gmail.com', '111222333'),
('Ana', 'Martínez', 'ana.martinez@gmail.com', '444555666');

-- Insertar datos de ejemplo en Inscripciones
INSERT INTO Inscripciones (EstudianteID, CursoID)
VALUES 
(1, 1), -- Juan inscrito en Inglés Básico
(2, 2); -- Ana inscrita en Francés Intermedio