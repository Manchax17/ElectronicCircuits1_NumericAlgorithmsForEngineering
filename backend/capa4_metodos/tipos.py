"""Tipos compartidos por los métodos numéricos de la Capa 4."""

from dataclasses import dataclass


@dataclass
class MatrizDispersa:
    """Sistema disperso ``G·V = b`` en formato diagonal más vecinos."""

    n: int
    diagonal: list[float]
    vecinos: list[list[tuple[int, float]]]
    b: list[float]


@dataclass
class ResultadoSolucion:
    """Solución y métricas producidas por un método iterativo."""

    solucion: list[float]
    iteraciones: int
    tiempo_s: float
    convergio: bool
    residual_max: float
    historial_error: list[float]
