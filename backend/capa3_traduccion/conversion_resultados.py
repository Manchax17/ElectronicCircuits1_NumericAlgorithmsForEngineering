"""
Capa 3 — Traducción: vector solución → formato interpretable.

Es la conversión inversa de :mod:`capa3_traduccion.constructor_sistema`. El
vector ``V`` que devuelve la Capa 4 se traduce a:

- una tabla por nodo (numeración de la netlist, desde 1);
- una grilla ``filas × columnas`` para el mapa de calor.

Además incluye :func:`grilla_a_potenciales`, que hace el camino contrario
(por ejemplo, para pasar a vector las mediciones del montaje físico tomadas
sobre la cuadrícula).

Convención de la grilla (igual que ``.malla`` en la netlist): el nodo ``k``
ocupa la fila ``(k-1) // columnas`` y la columna ``(k-1) % columnas``; la
fila 0 es la superior.

Rol responsable: especialista de datos.
"""

from __future__ import annotations

import math
from typing import Sequence

from .netlist_reader import GeometriaMalla


def potenciales_por_nodo(potenciales: Sequence[float]) -> list[dict]:
    """Devuelve ``[{"nodo": 1, "indice": 0, "potencial": V0}, ...]``.

    ``nodo`` usa la numeración de la netlist e ``indice`` la del vector.
    """
    _validar_vector(potenciales)
    return [
        {"nodo": i + 1, "indice": i, "potencial": float(v)}
        for i, v in enumerate(potenciales)
    ]


def potenciales_a_grilla(
    potenciales: Sequence[float],
    geometria: GeometriaMalla | None = None,
    *,
    filas: int | None = None,
    columnas: int | None = None,
) -> list[list[float]]:
    """Reorganiza el vector de potenciales en una grilla ``filas × columnas``.

    Las dimensiones salen de ``geometria`` (la directiva ``.malla``) o de
    ``filas`` y ``columnas`` explícitos; no se pueden dar ambos.

    Raises:
        ValueError: si faltan dimensiones o no coinciden con la longitud del vector.
    """
    _validar_vector(potenciales)
    if geometria is not None:
        if filas is not None or columnas is not None:
            raise ValueError("Indique la geometría o filas/columnas, no ambas.")
        filas, columnas = geometria.filas, geometria.columnas
    if filas is None or columnas is None:
        raise ValueError(
            "Faltan las dimensiones de la malla: declare .malla en la netlist o indique filas y columnas."
        )
    if filas <= 0 or columnas <= 0:
        raise ValueError("Las dimensiones de la malla deben ser positivas.")
    if filas * columnas != len(potenciales):
        raise ValueError(
            f"Una malla {filas}x{columnas} tiene {filas * columnas} nodos, "
            f"pero el vector tiene {len(potenciales)} potenciales."
        )

    return [
        [float(v) for v in potenciales[f * columnas:(f + 1) * columnas]]
        for f in range(filas)
    ]


def grilla_a_potenciales(grilla: Sequence[Sequence[float]]) -> list[float]:
    """Aplana una grilla rectangular al vector de potenciales (orden de nodos).

    Raises:
        ValueError: si la grilla está vacía, no es rectangular o tiene valores no finitos.
    """
    if not grilla or not grilla[0]:
        raise ValueError("La grilla está vacía.")
    columnas = len(grilla[0])
    for numero, fila in enumerate(grilla):
        if len(fila) != columnas:
            raise ValueError(
                f"La grilla no es rectangular: la fila {numero} tiene {len(fila)} valores y la fila 0 tiene {columnas}."
            )
    vector = [float(v) for fila in grilla for v in fila]
    _validar_vector(vector)
    return vector


def _validar_vector(potenciales: Sequence[float]) -> None:
    if len(potenciales) == 0:
        raise ValueError("El vector de potenciales está vacío.")
    for i, v in enumerate(potenciales):
        if not math.isfinite(float(v)):
            raise ValueError(f"El potencial del índice {i} no es finito ({v}).")
