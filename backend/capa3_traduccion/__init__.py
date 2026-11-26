"""Capa 3 — Traducción: netlist ↔ sistema disperso ``G·V = b`` y vector solución ↔ formato interpretable."""

from .constructor_sistema import construir_sistema, sistema_a_densa
from .conversion_resultados import (
    grilla_a_potenciales,
    potenciales_a_grilla,
    potenciales_por_nodo,
)
from .generador_mallas import generar_malla
from .netlist_reader import (
    ErrorNetlist,
    FuenteCorriente,
    GeometriaMalla,
    Netlist,
    Resistencia,
    leer_netlist,
)

__all__ = [
    "ErrorNetlist",
    "FuenteCorriente",
    "GeometriaMalla",
    "Netlist",
    "Resistencia",
    "construir_sistema",
    "generar_malla",
    "grilla_a_potenciales",
    "leer_netlist",
    "potenciales_a_grilla",
    "potenciales_por_nodo",
    "sistema_a_densa",
]
