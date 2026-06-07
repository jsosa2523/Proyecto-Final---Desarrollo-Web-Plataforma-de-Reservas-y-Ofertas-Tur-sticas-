# api/schemas.py
"""
Esquemas Pydantic para validación de entrada/salida de la API.
"""
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List, Any
from datetime import date
from decimal import Decimal


# ── Destinos ────────────────────────────────────────────────

class DestinoBase(BaseModel):
    nombre: str
    region: str
    descripcion: Optional[str] = None


class DestinoOut(DestinoBase):
    id: int

    class Config:
        from_attributes = True


# ── Ofertas Turísticas ───────────────────────────────────────

class OfertaBase(BaseModel):
    nombre: str
    descripcion: str
    precio: Decimal
    duracion_dias: int


class OfertaOut(OfertaBase):
    id: int
    destino_id: int
    descripcion_larga: Optional[str] = None
    precio_original: Optional[Decimal] = None
    imagen_url: Optional[str] = None
    imagenes: Optional[List[str]] = None
    itinerario: Optional[List[Any]] = None
    incluye: Optional[List[str]] = None
    disponible: bool
    destacada: bool
    destino: Optional[DestinoOut] = None

    class Config:
        from_attributes = True


# ── Reservas ────────────────────────────────────────────────

class ReservaCreate(BaseModel):
    oferta_id: int
    nombre_cliente: str
    apellido_cliente: str
    email: EmailStr
    telefono: Optional[str] = None
    fecha_viaje: date
    num_personas: int = 1
    metodo_pago: str
    notas: Optional[str] = None

    @field_validator("num_personas")
    @classmethod
    def personas_positivas(cls, v):
        if v < 1:
            raise ValueError("El número de personas debe ser mayor a 0")
        return v

    @field_validator("metodo_pago")
    @classmethod
    def metodo_valido(cls, v):
        allowed = {"tarjeta", "transferencia", "efectivo"}
        if v not in allowed:
            raise ValueError(f"Método de pago debe ser uno de: {allowed}")
        return v

    @field_validator("fecha_viaje")
    @classmethod
    def fecha_futura(cls, v):
        from datetime import date as _date
        if v <= _date.today():
            raise ValueError("La fecha de viaje debe ser una fecha futura")
        return v


class ReservaOut(BaseModel):
    id: int
    oferta_id: int
    nombre_cliente: str
    apellido_cliente: str
    email: str
    telefono: Optional[str]
    fecha_viaje: date
    num_personas: int
    metodo_pago: str
    monto_total: Decimal
    estado: str

    class Config:
        from_attributes = True


class MensajeRespuesta(BaseModel):
    mensaje: str
    id: Optional[int] = None
