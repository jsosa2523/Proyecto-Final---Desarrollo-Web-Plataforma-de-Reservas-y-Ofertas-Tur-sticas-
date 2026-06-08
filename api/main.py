# api/main.py
"""
TuristicaRD — API REST Principal
Punto de entrada de la aplicación FastAPI.
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routes import ofertas, reservas

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TuristicaRD API",
    description="API REST para la plataforma de reservas y ofertas turísticas de República Dominicana.",
    version="1.2.0",
    contact={
        "name": "TuristicaRD",
        "email": "dev@turistica-rd.com",
    },
)

# CORS — permite peticiones del frontend
origins = [
    "http://localhost:3000",
    "https://turistica-rd.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(ofertas.router)
app.include_router(reservas.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "api": "TuristicaRD",
        "version": "1.2.0",
        "docs": "/docs",
        "status": "ok",
    }


@app.get("/health", tags=["Root"])
def health():
    return {"status": "healthy"}

# v1.0 - API REST completa con endpoints de ofertas y reservas