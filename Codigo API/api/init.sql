-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS peps;
USE peps;

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
    descripcion TEXT NOT NULL,
    precio DECIMAL(9,2) NOT NULL,
    foto VARCHAR(255)
);

-- Tabla de reservas 
CREATE TABLE reservas (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_cliente VARCHAR(255) NOT NULL,
    id_mesa BIGINT UNSIGNED NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    lugar VARCHAR(255) NOT NULL,
    precio_reserva DECIMAL(9,2) NOT NULL,
    foto_comida_reserva VARCHAR(255),
    estado VARCHAR(50) DEFAULT 'pendiente',
    FOREIGN KEY (id_mesa) REFERENCES mesas(id_mesa) ON DELETE CASCADE
);


-- Tabla de usuarios
CREATE TABLE usuarios (
    usuario VARCHAR(100) NOT NULL PRIMARY KEY,
    clave VARCHAR(255) NOT NULL,
    perfil VARCHAR(100) NOT NULL,
    fechaUltimoAcceso DATE
);

-- Insertar un usuario de ejemplo (contraseña en texto plano, deberías usar bcrypt en Flask)
INSERT INTO usuarios (usuario, clave, perfil, fechaUltimoAcceso) VALUES
('admin', '1234', 'admin', '2022-03-01');

-- Insertar datos de ejemplo en las tablas
INSERT INTO clientes (nombre, telefono, correo, fechaRegistro) VALUES
('Juan Perez', '123456789', 'juan@example.com', '2023-01-01'),
('Maria Lopez', '987654321', 'maria@example.com', '2023-02-15');

INSERT INTO mesas (numero, capacidad, ubicacion) VALUES
(1, 2, 'Interior'),
(2, 4, 'Terraza');

INSERT INTO platos (nombre, descripcion, precio, foto) VALUES
('Carne', 'Delicioso corte de res a la parrilla', 4.00, NULL),
('Pescado', 'Filete de pescado frito con guarnición', 5.00, NULL);

INSERT INTO reservas (nombre_cliente, id_mesa, fecha, hora, lugar, precio_reserva, estado) VALUES
('Juan Perez', 1, '2025-06-12', '19:00', 'Interior', 20.00, 'confirmada'),
('Maria Lopez', 2, '2025-06-12', '20:00', 'Terraza', 15.00, 'pendiente');
