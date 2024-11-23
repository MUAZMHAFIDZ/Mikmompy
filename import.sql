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
    hotspot_name VARCHAR(255) NOT NULL
);

-- CREATE TABLE mikrotik_profile (
--     id VARCHAR(255) PRIMARY KEY,
--     limit_bandwidth VARCHAR(255) NOT NULL,
--     nama_paket VARCHAR(255) NOT NULL,
--     harga INT
-- );

-- CREATE TABLE mikrotik_voucher (
--     id VARCHAR(255) NOT NULL PRIMARY KEY,
--     username VARCHAR(255) NOT NULL,
--     password VARCHAR(255) NOT NULL,
--     harga INT,
--     limit_bandwidth VARCHAR(255) NOT NULL,
--     nama_paket VARCHAR(255) NOT NULL,
-- );

INSERT INTO users (username, password) VALUES ('admin', 'admin');