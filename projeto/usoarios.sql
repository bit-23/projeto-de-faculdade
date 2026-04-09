-- Active: 1771001940362@@127.0.0.1@3306@ServiceConnect
-- Active: 1771001940362@@127.0.0.1@3306@faculdade
CREATE TABLE ServiceConnect_usuarios (
    idUsuarios INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(45),
    email VARCHAR(45) DEFAULT 'não tem gmail',
    cpf VARCHAR(50),
    idade INT NOT NULL CHECK (idade > 18),
    PRIMARY KEY (idUsuarios)
) ENGINE=InnoDB;