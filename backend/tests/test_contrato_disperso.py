"""Validación del contrato interno de matrices dispersas."""

import json
from pathlib import Path

import pytest


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "malla_3x3.json"


def validar_matriz_dispersa(matriz: dict) -> None:
    """Comprueba dimensiones, índices, diagonal excluida y simetría."""
    n = matriz.get("n")
    if not isinstance(n, int) or isinstance(n, bool) or n < 0:
        raise ValueError("n debe ser un entero no negativo")

    for campo in ("diagonal", "vecinos", "b"):
        valores = matriz.get(campo)
        if not isinstance(valores, (list, tuple)) or len(valores) != n:
            raise ValueError(f"{campo} debe tener longitud n={n}")

    vecinos = matriz["vecinos"]
    entradas_por_fila: list[dict[int, object]] = []

    for i, fila in enumerate(vecinos):
        if not isinstance(fila, (list, tuple)):
            raise ValueError(f"vecinos[{i}] debe ser una lista o tupla de pares")

        entradas: dict[int, object] = {}
        for par in fila:
            if not isinstance(par, (list, tuple)) or len(par) != 2:
                raise ValueError(f"vecinos[{i}] debe contener pares [j, G_ij]")

            j, valor = par
            if not isinstance(j, int) or isinstance(j, bool) or not 0 <= j < n:
                raise ValueError(f"índice vecino {j!r} fuera de rango en vecinos[{i}]")
            if j == i:
                raise ValueError(f"la diagonal no debe aparecer en vecinos[{i}]")
            entradas[j] = valor
        entradas_por_fila.append(entradas)

    for i, entradas in enumerate(entradas_por_fila):
        for j, valor in entradas.items():
            if i not in entradas_por_fila[j] or entradas_por_fila[j][i] != valor:
                raise ValueError(
                    f"vecinos[{i}] contiene ({j}, {valor!r}) sin par simétrico "
                    f"igual en vecinos[{j}]"
                )


def cargar_matriz_fixture() -> dict:
    """Lee la matriz dispersa de la malla 3x3 de referencia."""
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    return fixture["matriz"]


def test_fixture_malla_3x3_cumple_el_contrato() -> None:
    validar_matriz_dispersa(cargar_matriz_fixture())


def test_validacion_detecta_vecino_no_simetrico() -> None:
    matriz = cargar_matriz_fixture()
    matriz["vecinos"][1].remove([0, -1.0])

    with pytest.raises(ValueError, match="simétrico"):
        validar_matriz_dispersa(matriz)
