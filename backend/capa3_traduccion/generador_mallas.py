"""
Capa 3 — Traducción: generador de mallas sintéticas.

Escribe la netlist de una malla rectangular ``filas × columnas`` para los
casos de estudio (10×10, 20×20, 50×50) sin tener que escribirla a mano. La
salida es texto en el mismo formato que lee :func:`leer_netlist`, de modo que
una malla generada y una escrita a mano siguen exactamente el mismo camino.

Numeración: el nodo ``k`` ocupa la fila ``(k-1) // columnas`` y la columna
``(k-1) % columnas``. Orden de las resistencias: enlaces horizontales,
enlaces verticales y luego fugas a tierra (igual que el ejemplo 3×3 del
contrato).

Rol responsable: especialista de datos.
"""

from __future__ import annotations


def generar_malla(
    filas: int,
    columnas: int,
    r_enlace: float,
    r_fuga: float,
    nodo_falla: int,
    corriente: float,
    separacion_m: float | None = None,
) -> str:
    """Genera la netlist de una malla rectangular con fuga uniforme a tierra.

    Args:
        filas, columnas: dimensiones de la malla (nodos por lado).
        r_enlace: resistencia entre nodos vecinos (Ω). Menor = conductores más densos.
        r_fuga: resistencia de cada nodo hacia la tierra profunda (Ω).
        nodo_falla: nodo (desde 1) donde se inyecta la corriente de falla.
        corriente: corriente de falla inyectada (A).
        separacion_m: distancia entre nodos vecinos; se escribe en ``.malla``.

    Raises:
        ValueError: si algún parámetro está fuera de rango.
    """
    if filas <= 0 or columnas <= 0:
        raise ValueError("Las dimensiones de la malla deben ser positivas.")
    if r_enlace <= 0 or r_fuga <= 0:
        raise ValueError("Las resistencias deben ser positivas.")
    total = filas * columnas
    if not 1 <= nodo_falla <= total:
        raise ValueError(f"El nodo de falla debe estar entre 1 y {total}.")
    if separacion_m is not None and separacion_m <= 0:
        raise ValueError("La separación debe ser positiva.")

    def nodo(f: int, c: int) -> int:
        return f * columnas + c + 1

    sep = f" {_fmt(separacion_m)}" if separacion_m is not None else ""
    lineas = [
        f"# Malla {filas}x{columnas}, enlaces de {_fmt(r_enlace)} ohm, fuga de {_fmt(r_fuga)} ohm "
        f"por nodo, falla de {_fmt(corriente)} A en el nodo {nodo_falla}",
        f".malla {filas} {columnas}{sep}",
    ]

    k = 0
    for f in range(filas):
        for c in range(columnas - 1):
            k += 1
            lineas.append(f"R{k} {nodo(f, c)} {nodo(f, c + 1)} {_fmt(r_enlace)}")
    for f in range(filas - 1):
        for c in range(columnas):
            k += 1
            lineas.append(f"R{k} {nodo(f, c)} {nodo(f + 1, c)} {_fmt(r_enlace)}")
    for n in range(1, total + 1):
        k += 1
        lineas.append(f"R{k} {n} 0 {_fmt(r_fuga)}")

    lineas.append(f"I1 0 {nodo_falla} {_fmt(corriente)}")
    return "\n".join(lineas) + "\n"


def _fmt(valor: float) -> str:
    """Formato compacto y sin pérdida (``repr`` de float, sin ``.0`` sobrante)."""
    texto = repr(float(valor))
    return texto[:-2] if texto.endswith(".0") else texto
