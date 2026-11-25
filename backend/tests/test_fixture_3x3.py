"""Propiedades de la malla de puesta a tierra 3x3 de referencia."""

import json
from pathlib import Path

import numpy as np

from tests.referencia import resolver_referencia


RUTA_FIXTURE = Path(__file__).parent / "fixtures" / "malla_3x3.json"


def cargar_fixture() -> dict:
    """Carga los datos compartidos de la malla 3x3."""
    return json.loads(RUTA_FIXTURE.read_text(encoding="utf-8"))


def matriz_densa(matriz: dict) -> np.ndarray:
    """Construye la matriz densa G desde su representación dispersa."""
    n = matriz["n"]
    densa = np.zeros((n, n), dtype=float)
    for i, valor in enumerate(matriz["diagonal"]):
        densa[i, i] = valor
    for i, fila in enumerate(matriz["vecinos"]):
        for j, valor in fila:
            densa[i, j] = valor
    return densa


def test_matriz_es_simetrica() -> None:
    matriz = cargar_fixture()["matriz"]
    vecinos = [{j: valor for j, valor in fila} for fila in matriz["vecinos"]]

    for i, fila in enumerate(matriz["vecinos"]):
        for j, valor in fila:
            assert vecinos[j][i] == valor


def test_diagonal_es_estrictamente_dominante() -> None:
    matriz = cargar_fixture()["matriz"]

    for i, fila in enumerate(matriz["vecinos"]):
        assert matriz["diagonal"][i] > sum(abs(valor) for _, valor in fila)


def test_matriz_es_definida_positiva() -> None:
    matriz = cargar_fixture()["matriz"]
    autovalor_minimo = np.linalg.eigvalsh(matriz_densa(matriz)).min()

    assert autovalor_minimo > 0


def test_solver_directo_coincide_con_solucion_referencia() -> None:
    fixture = cargar_fixture()
    calculada = resolver_referencia(fixture["matriz"])

    np.testing.assert_allclose(
        calculada,
        fixture["solucion_referencia"],
        rtol=0.0,
        atol=1e-8,
    )


def test_residual_de_solucion_referencia_es_menor_a_1e_10() -> None:
    matriz = cargar_fixture()["matriz"]
    solucion = np.asarray(cargar_fixture()["solucion_referencia"], dtype=float)
    vector_b = np.asarray(matriz["b"], dtype=float)
    residual_max = np.max(np.abs(vector_b - matriz_densa(matriz) @ solucion))

    assert residual_max < 1e-10
