"""
Capa 3 — Traducción: netlist → sistema disperso ``G·V = b``.

Aplica el estampado nodal (KCL + ley de Ohm) y entrega el formato disperso
acordado en el contrato entre capas (sprint 1, sección 7.2)::

    {
        "n": 9,
        "diagonal": [2.1, 3.1, ...],          # G_ii
        "vecinos": [[[1, -1.0], [3, -1.0]],   # por fila i: [j, G_ij], j != i
                    ...],
        "b": [0, 0, 0, 0, 1.0, 0, 0, 0, 0],   # corrientes inyectadas
    }

Los índices empiezan en 0: el nodo ``k`` de la netlist es el índice ``k - 1``.
La tierra (nodo 0) no es incógnita; las resistencias hacia ella solo suman a
la diagonal, y eso es lo que hace a ``G`` definida positiva.

El resultado es un ``dict`` de tipos nativos (serializable a JSON). La Capa 2
lo convierte al tipo que espere la Capa 4; esta capa no la importa.

Rol responsable: especialista de datos.
"""

from __future__ import annotations

from .netlist_reader import NODO_TIERRA, Netlist, leer_netlist


def construir_sistema(netlist: str | Netlist) -> dict:
    """Construye el sistema disperso a partir de una netlist (texto o ya leída).

    - Resistencia ``R`` entre ``a`` y ``c`` con ``g = 1/R``:
      ``G_aa += g``, ``G_cc += g``, ``G_ac -= g``, ``G_ca -= g``.
      Si uno de los nodos es tierra, solo se suma ``g`` a la diagonal del otro.
      Resistencias en paralelo entre el mismo par se acumulan.
    - Fuente ``I`` de ``desde`` a ``hacia`` con valor ``A``:
      ``b_hacia += A`` y ``b_desde -= A`` (se omite el término de tierra).

    Raises:
        ErrorNetlist: si el texto no es una netlist válida.
    """
    if isinstance(netlist, str):
        netlist = leer_netlist(netlist)

    n = netlist.num_nodos
    diagonal = [0.0] * n
    acoples: list[dict[int, float]] = [{} for _ in range(n)]
    b = [0.0] * n

    for r in netlist.resistencias:
        g = 1.0 / r.ohmios
        if r.a != NODO_TIERRA:
            diagonal[r.a - 1] += g
        if r.b != NODO_TIERRA:
            diagonal[r.b - 1] += g
        if r.a != NODO_TIERRA and r.b != NODO_TIERRA:
            i, j = r.a - 1, r.b - 1
            acoples[i][j] = acoples[i].get(j, 0.0) - g
            acoples[j][i] = acoples[j].get(i, 0.0) - g

    for fuente in netlist.fuentes:
        if fuente.hacia != NODO_TIERRA:
            b[fuente.hacia - 1] += fuente.amperios
        if fuente.desde != NODO_TIERRA:
            b[fuente.desde - 1] -= fuente.amperios

    vecinos = [[[j, valor] for j, valor in sorted(fila.items())] for fila in acoples]

    return {"n": n, "diagonal": diagonal, "vecinos": vecinos, "b": b}


def sistema_a_densa(sistema: dict) -> list[list[float]]:
    """Expande el formato disperso a una matriz densa ``n×n``.

    Solo para depuración, mostrar el sistema en la interfaz con mallas
    pequeñas o exportarlo. Los métodos iterativos trabajan con el disperso.
    """
    n = sistema["n"]
    densa = [[0.0] * n for _ in range(n)]
    for i, valor in enumerate(sistema["diagonal"]):
        densa[i][i] = valor
    for i, fila in enumerate(sistema["vecinos"]):
        for j, valor in fila:
            densa[i][j] = valor
    return densa
