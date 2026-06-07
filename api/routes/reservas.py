# api/routes/reservas.py
"""
Endpoints REST para gestionar reservas turísticas.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Reserva, OfertaTuristica
from schemas import ReservaCreate, ReservaOut, MensajeRespuesta

router = APIRouter(prefix="/api/reservas", tags=["Reservas"])


@router.post("/", response_model=MensajeRespuesta, status_code=201,
             summary="Crear nueva reserva")
def crear_reserva(datos: ReservaCreate, db: Session = Depends(get_db)):
    """
    Registra una nueva reserva en la base de datos.

    - Valida que la oferta exista y esté disponible.
    - Calcula el monto total automáticamente.
    """
    oferta = db.query(OfertaTuristica).filter(
        OfertaTuristica.id == datos.oferta_id,
        OfertaTuristica.disponible == True,
    ).first()

    if not oferta:
        raise HTTPException(status_code=404, detail="Oferta no encontrada o no disponible")

    monto_total = float(oferta.precio) * datos.num_personas

    reserva = Reserva(
        oferta_id        = datos.oferta_id,
        nombre_cliente   = datos.nombre_cliente,
        apellido_cliente = datos.apellido_cliente,
        email            = datos.email,
        telefono         = datos.telefono,
        fecha_viaje      = datos.fecha_viaje,
        num_personas     = datos.num_personas,
        metodo_pago      = datos.metodo_pago,
        monto_total      = monto_total,
        notas            = datos.notas,
        estado           = "pendiente",
    )
    db.add(reserva)
    db.commit()
    db.refresh(reserva)

    return MensajeRespuesta(
        mensaje=f"Reserva creada exitosamente. Total a pagar: RD$ {monto_total:,.2f}",
        id=reserva.id,
    )


@router.get("/", response_model=List[ReservaOut], summary="Listar reservas")
def listar_reservas(db: Session = Depends(get_db)):
    """Retorna todas las reservas registradas."""
    return db.query(Reserva).order_by(Reserva.creado_en.desc()).all()


@router.get("/{reserva_id}", response_model=ReservaOut, summary="Obtener reserva por ID")
def obtener_reserva(reserva_id: int, db: Session = Depends(get_db)):
    """Retorna los detalles de una reserva específica."""
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva
