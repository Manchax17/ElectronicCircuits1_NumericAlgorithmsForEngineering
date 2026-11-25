"""Capa 4: métodos iterativos y tipos compartidos."""

from .gauss_seidel import gauss_seidel
from .jacobi import jacobi
from .sor import sor
from .ssor import ssor
from .tipos import MatrizDispersa, ResultadoSolucion

__all__ = [
    "MatrizDispersa",
    "ResultadoSolucion",
    "gauss_seidel",
    "jacobi",
    "sor",
    "ssor",
]
