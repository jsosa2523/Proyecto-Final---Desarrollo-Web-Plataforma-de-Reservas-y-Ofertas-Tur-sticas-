-- ============================================================
--  TuristicaRD — Esquema de Base de Datos
--  Archivo: database/schema.sql
--  Versión: 1.0.0
-- ============================================================

CREATE DATABASE IF NOT EXISTS turistica_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE turistica_db;

-- ------------------------------------------------------------
-- Tabla: destinos
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS destinos (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  nombre      VARCHAR(100) NOT NULL,
  region      VARCHAR(100) NOT NULL,
  descripcion TEXT,
  creado_en   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Tabla: ofertas_turisticas
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ofertas_turisticas (
  id              INT AUTO_INCREMENT PRIMARY KEY,
  destino_id      INT NOT NULL,
  nombre          VARCHAR(150) NOT NULL,
  descripcion     TEXT NOT NULL,
  descripcion_larga TEXT,
  precio          DECIMAL(10,2) NOT NULL,
  precio_original DECIMAL(10,2),
  duracion_dias   INT NOT NULL DEFAULT 1,
  imagen_url      VARCHAR(300),
  imagenes        JSON,
  itinerario      JSON,
  incluye         JSON,
  disponible      BOOLEAN DEFAULT TRUE,
  destacada       BOOLEAN DEFAULT FALSE,
  creado_en       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  actualizado_en  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (destino_id) REFERENCES destinos(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Tabla: reservas
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS reservas (
  id              INT AUTO_INCREMENT PRIMARY KEY,
  oferta_id       INT NOT NULL,
  nombre_cliente  VARCHAR(150) NOT NULL,
  apellido_cliente VARCHAR(150) NOT NULL,
  email           VARCHAR(200) NOT NULL,
  telefono        VARCHAR(20),
  fecha_viaje     DATE NOT NULL,
  num_personas    INT NOT NULL DEFAULT 1,
  metodo_pago     ENUM('tarjeta','transferencia','efectivo') NOT NULL,
  monto_total     DECIMAL(10,2) NOT NULL,
  estado          ENUM('pendiente','confirmada','cancelada') DEFAULT 'pendiente',
  notas           TEXT,
  creado_en       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (oferta_id) REFERENCES ofertas_turisticas(id) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- Índices para mejorar rendimiento
CREATE INDEX idx_reservas_email    ON reservas(email);
CREATE INDEX idx_reservas_estado   ON reservas(estado);
CREATE INDEX idx_ofertas_destino   ON ofertas_turisticas(destino_id);
CREATE INDEX idx_ofertas_disponible ON ofertas_turisticas(disponible);
