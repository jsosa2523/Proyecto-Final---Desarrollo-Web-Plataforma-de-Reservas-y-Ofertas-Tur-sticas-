# api/models.py
"""
Modelos de SQLAlchemy que mapean las tablas de la base de datos.
"""
from sqlalchemy import (
    Column, Integer, String, Text, Boolean,
    DECIMAL, Date, Enum, JSON, ForeignKey, TIMESTAMP
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Destino(Base):
    __tablename__ = "destinos"

    id          = Column(Integer, primary_key=True, index=True)
    nombre      = Column(String(100), nullable=False)
    region      = Column(String(100), nullable=False)
    descripcion = Column(Text)
    creado_en   = Column(TIMESTAMP, server_default=func.now())

    ofertas = relationship("OfertaTuristica", back_populates="destino")


class OfertaTuristica(Base):
    __tablename__ = "ofertas_turisticas"

    id                = Column(Integer, primary_key=True, index=True)
    destino_id        = Column(Integer, ForeignKey("destinos.id"), nullable=False)
    nombre            = Column(String(150), nullable=False)
    descripcion       = Column(Text, nullable=False)
    descripcion_larga = Column(Text)
    precio            = Column(DECIMAL(10, 2), nullable=False)
    precio_original   = Column(DECIMAL(10, 2))
    duracion_dias     = Column(Integer, default=1)
    imagen_url        = Column(String(300))
    imagenes          = Column(JSON)
    itinerario        = Column(JSON)
    incluye           = Column(JSON)
    disponible        = Column(Boolean, default=True)
    destacada         = Column(Boolean, default=False)
    creado_en         = Column(TIMESTAMP, server_default=func.now())
    actualizado_en    = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    destino  = relationship("Destino", back_populates="ofertas")
    reservas = relationship("Reserva", back_populates="oferta")


class Reserva(Base):
    __tablename__ = "reservas"

    id               = Column(Integer, primary_key=True, index=True)
    oferta_id        = Column(Integer, ForeignKey("ofertas_turisticas.id"), nullable=False)
    nombre_cliente   = Column(String(150), nullable=False)
    apellido_cliente = Column(String(150), nullable=False)
    email            = Column(String(200), nullable=False)
    telefono         = Column(String(20))
    fecha_viaje      = Column(Date, nullable=False)
    num_personas     = Column(Integer, default=1)
    metodo_pago      = Column(Enum("tarjeta", "transferencia", "efectivo"), nullable=False)
    monto_total      = Column(DECIMAL(10, 2), nullable=False)
    estado           = Column(
        Enum("pendiente", "confirmada", "cancelada"),
        default="pendiente"
    )
    notas            = Column(Text)
    creado_en        = Column(TIMESTAMP, server_default=func.now())

    oferta = relationship("OfertaTuristica", back_populates="reservas")
