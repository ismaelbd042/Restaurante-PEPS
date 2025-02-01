DROP DATABASE IF EXISTS PEPS;
-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS PEPS;
USE PEPS;

-- Tabla de clientes
CREATE TABLE clientes (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    telefono VARCHAR(15),
    correo VARCHAR(255),
    fechaRegistro DATE NOT NULL
);

-- Tabla de mesas
CREATE TABLE mesas (
    id_mesa BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    numero INT NOT NULL UNIQUE,
    capacidad INT NOT NULL,
    ubicacion VARCHAR(255) NOT NULL
);

-- Tabla de platos
CREATE TABLE platos (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    precio DECIMAL(9,2) NOT NULL,
    foto VARCHAR(255)
);

-- Tabla de reservas
CREATE TABLE reservas(
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_Cliente VARCHAR(255) NOT NULL,
    lugar VARCHAR(255) NOT NULL,
    precio_reserva DECIMAL(9,2) NOT NULL,
    foto_comida_reserva VARCHAR(255),
    id_cliente BIGINT UNSIGNED NOT NULL,
    id_mesa BIGINT UNSIGNED NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado VARCHAR(50) DEFAULT 'pendiente',
    FOREIGN KEY (id_cliente) REFERENCES clientes(id),
    FOREIGN KEY (id_mesa) REFERENCES mesas(id_mesa)  -- Cambio aquí
);

-- Tabla de usuarios
CREATE TABLE usuarios (
    usuario VARCHAR(100) NOT NULL PRIMARY KEY,
    clave VARCHAR(255) NOT NULL,
    perfil VARCHAR(100) NOT NULL,
    fechaUltimoAcceso DATE
);

-- Insertar un usuario de ejemplo
INSERT INTO usuarios (usuario, clave, perfil, fechaUltimoAcceso) VALUES
('admin', '1234', 'admin', '2022-03-01');

-- Insertar datos de ejemplo en las tablas
INSERT INTO clientes (nombre, telefono, correo, fechaRegistro) VALUES
('Juan Perez', '123456789', 'juan@example.com', '2023-01-01'),
('Maria Lopez', '987654321', 'maria@example.com', '2023-02-15');

INSERT INTO mesas (numero, capacidad, ubicacion) VALUES
(1, 2, 'Interior'),
(3, 4, 'Terraza');

INSERT INTO platos (nombre, precio, foto) VALUES
('Carne', 4.00, NULL),
('Pescado', 5.00, NULL);

INSERT INTO reservas (id_cliente, id_mesa, lugar, precio_reserva, estado, fecha, hora, nombre_Cliente) VALUES
(1, 1, 'Comedor', 19.00, 'confirmada', '2025-06-12', '19:00', 'Juan Perez'),
(2, 2, 'Terraza', 25.00, 'pendiente', '2025-06-12', '20:00', 'Maria Lopez');