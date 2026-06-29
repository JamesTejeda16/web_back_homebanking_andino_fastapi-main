"""HOMEBANKING — Backend FastAPI · Banca Internet Banco Andino.

Portal del CLIENTE. Proyecto separado del core bancario; se conecta a la base
PostgreSQL YA EXISTENTE bd_core_financiero (no crea tablas). Corre en el puerto 8002.

Levantar:  uvicorn main:app --reload --port 8002
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Carga .env explícitamente antes de cualquier import que use settings
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.cfg_config import settings
from app.routes import route_auth, route_creditos, route_cuentas, route_operaciones

app = FastAPI(
    title="Banca Internet Banco Andino — Homebanking API",
    description="Portal del cliente de Banca Internet Banco Andino. Solo consultas y "
    "operaciones del cliente del portal (dcliente / usuarios_homebanking).",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    # Cambiamos esto para agregar tu enlace de Vercel directamente
    allow_origins=[
        "http://localhost:5173", 
        "https://web-front-homebanking-andino-react-one.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(route_auth.router)
app.include_router(route_cuentas.router)
app.include_router(route_operaciones.router)
app.include_router(route_creditos.router)


@app.get("/", tags=["root"])
def raiz():
    return {
        "servicio": "Banca Internet Banco Andino — Homebanking API",
        "version": "1.0.0",
        "estado": "ok",
        "docs": "/docs",
        "puerto": settings.PORT,
    }
