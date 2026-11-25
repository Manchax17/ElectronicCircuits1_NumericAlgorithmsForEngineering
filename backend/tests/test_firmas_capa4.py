"""Pruebas del contrato común de los métodos de la Capa 4."""

import inspect

import pytest

from capa4_metodos import (
    MatrizDispersa,
    ResultadoSolucion,
    gauss_seidel,
    jacobi,
    sor,
    ssor,
)


METODOS = (jacobi, gauss_seidel, sor, ssor)


def test_los_metodos_tienen_la_misma_firma_tipificada() -> None:
    firma_esperada = inspect.Signature(
        parameters=(
            inspect.Parameter(
                "matriz", inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=MatrizDispersa,
            ),
            inspect.Parameter(
                "tolerancia", inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=float,
            ),
            inspect.Parameter(
                "omega", inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=float,
            ),
            inspect.Parameter(
                "max_iteraciones", inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=int,
            ),
        ),
        return_annotation=ResultadoSolucion,
    )

    for metodo in METODOS:
        assert inspect.signature(metodo) == firma_esperada


@pytest.mark.parametrize("metodo", METODOS)
def test_los_stubs_indican_que_no_estan_implementados(metodo) -> None:
    matriz = MatrizDispersa(n=1, diagonal=[1.0], vecinos=[[]], b=[1.0])

    with pytest.raises(NotImplementedError):
        metodo(matriz, 1e-6, 1.0, 100)
