"""Método iterativo de Gauss-Seidel para sistemas dispersos."""

from .tipos import MatrizDispersa, ResultadoSolucion


def gauss_seidel(
    matriz: MatrizDispersa,
    tolerancia: float,
    omega: float,
    max_iteraciones: int,
) -> ResultadoSolucion:
    """Resuelve ``G·V=b`` mediante Gauss-Seidel.

    La actualización es ``V_i^(k+1) = (b_i - Σ[j<i] G_ij V_j^(k+1)
    - Σ[j>i] G_ij V_j^k) / G_ii``; ``omega`` se recibe para mantener la firma
    común y no se utiliza. La iteración termina cuando
    ``||b-G·V||∞ / ||b||∞ < tolerancia`` o se alcanza ``max_iteraciones``.

    TODO: sprint 2.
    """
    raise NotImplementedError  # TODO sprint 2
