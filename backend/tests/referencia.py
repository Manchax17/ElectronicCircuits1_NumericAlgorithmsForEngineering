"""Solver directo de referencia, reservado para pruebas."""

import numpy as np


def resolver_referencia(matriz: dict) -> list[float]:
    """Arma la matriz densa ``G`` y resuelve ``G·V=b`` con NumPy."""
    n = matriz["n"]
    densa = np.zeros((n, n), dtype=float)

    for i, valor in enumerate(matriz["diagonal"]):
        densa[i, i] = valor

    for i, fila in enumerate(matriz["vecinos"]):
        for j, valor in fila:
            densa[i, j] = valor

    solucion = np.linalg.solve(densa, np.asarray(matriz["b"], dtype=float))
    return solucion.tolist()
