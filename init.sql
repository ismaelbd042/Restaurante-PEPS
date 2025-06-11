CREATE DATABASE IF NOT EXISTS ciber;
CREATE USER 'user'@'%' IDENTIFIED BY 'userpw';
GRANT ALL PRIVILEGES ON ciber.* TO 'user'@'%';
FLUSH PRIVILEGES;
USE ciber;
CREATE TABLE reserva(
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    cliente VARCHAR(255) NOT NULL,
    fecha VARCHAR(255) NOT NULL,
    hora VARCHAR(255) NOT NULL,
    numero_personas VARCHAR(255),
    observaciones VARCHAR(255)
);
CREATE TABLE usuarios(
	usuario VARCHAR(100) NOT NULL PRIMARY KEY,
    clave VARCHAR(255) NOT NULL,
    perfil VARCHAR(100) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    correo VARCHAR(255) NOT NULL,
    fechaUltimoAcceso DATE,
    fechaBloqueo DATE,
    numeroAccesosErroneo INTEGER,
    debeCambiarClave BOOLEAN
);



INSERT INTO `usuarios` (`usuario`, `clave`, `perfil`,`estado`, `correo`,`numeroAccesosErroneo`,`fechaUltimoAcceso`) VALUES ('root','$2b$10$hJtLt4u0SqSf.h3S5Uuev.nu98ARhn.6SpvFCYbc1eeynJmy81cmK', 'admin', 'activo','root@pp.es', 0, '2022-03-01 00:00');
INSERT INTO `reserva` (`cliente`, `fecha`, `hora`, `numero_personas`, `observaciones`) VALUES ('Ismael', '24/04/2025', '14:00', '4', 'Un alérgico al huevo');
