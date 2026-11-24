"""
Punto de entrada mínimo del backend.

En esta fase solo expone el endpoint de salud. Las rutas de negocio se
agregarán en la Capa 2 durante el Sprint 1.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ElectronicCircuits1 — API",
    version="0.1.0",
    description="Scaffolding del backend para el análisis de circuitos con métodos iterativos.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["infraestructura"])
def health() -> dict[str, str]:
    """Indica que el servicio está en ejecución."""
    return {"status": "ok"}
