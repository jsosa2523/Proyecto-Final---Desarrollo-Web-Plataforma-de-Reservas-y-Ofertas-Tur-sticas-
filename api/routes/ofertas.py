# api/routes/ofertas.py
"""
Endpoints REST para consultar ofertas turísticas.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import OfertaTuristica
from schemas import OfertaOut

router = APIRouter(prefix="/api/ofertas", tags=["Ofertas"])


@router.get("/", response_model=List[OfertaOut], summary="Listar todas las ofertas")
def listar_ofertas(
    disponible: Optional[bool] = Query(None, description="Filtrar por disponibilidad"),
    destacada:  Optional[bool] = Query(None, description="Solo ofertas destacadas"),
    db: Session = Depends(get_db),
):
    """Retorna el listado completo de ofertas turísticas."""
    query = db.query(OfertaTuristica)
    if disponible is not None:
        query = query.filter(OfertaTuristica.disponible == disponible)
    if destacada is not None:
        query = query.filter(OfertaTuristica.destacada == destacada)
    return query.order_by(OfertaTuristica.destacada.desc(), OfertaTuristica.id).all()


@router.get("/buscar", response_model=List[OfertaOut], summary="Buscar ofertas")
def buscar_ofertas(
    q: str = Query(..., min_length=2, description="Texto a buscar"),
    db: Session = Depends(get_db),
):
    """Busca ofertas por nombre o descripción."""
    termino = f"%{q}%"
    results = (
        db.query(OfertaTuristica)
        .filter(
            (OfertaTuristica.nombre.ilike(termino)) |
            (OfertaTuristica.descripcion.ilike(termino))
        )
        .filter(OfertaTuristica.disponible == True)
        .all()
    )
    return results


@router.get("/{oferta_id}", response_model=OfertaOut, summary="Obtener oferta por ID")
def obtener_oferta(oferta_id: int, db: Session = Depends(get_db)):
    """Retorna los detalles completos de una oferta específica."""
    oferta = db.query(OfertaTuristica).filter(OfertaTuristica.id == oferta_id).first()
    if not oferta:
        raise HTTPException(status_code=404, detail="Oferta no encontrada")
    return oferta
