CREATE DATABASE mikmikmom;
USE mikmikmom;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE mikrotik (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ip VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    hotspot_name VARCHAR(255) NOT NULL,
    dns_name VARCHAR(255) NOT NULL
);

INSERT INTO users (username, password) VALUES ('admin', 'admin');