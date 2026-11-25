"""Método SSOR para sistemas dispersos."""

from .tipos import MatrizDispersa, ResultadoSolucion


def ssor(
    matriz: MatrizDispersa,
    tolerancia: float,
    omega: float,
    max_iteraciones: int,
) -> ResultadoSolucion:
    """Resuelve ``G·V=b`` mediante SOR simétrico (SSOR).

    La barrida hacia adelante calcula
    ``y_i = (1-omega)V_i^k + omega (b_i - Σ[j<i]G_ij y_j
    - Σ[j>i]G_ij V_j^k) / G_ii``. La barrida hacia atrás calcula
    ``V_i^(k+1) = (1-omega)y_i + omega (b_i - Σ[j<i]G_ij y_j
    - Σ[j>i]G_ij V_j^(k+1)) / G_ii``. La iteración termina cuando
    ``||b-G·V||∞ / ||b||∞ < tolerancia`` o se alcanza ``max_iteraciones``.

    TODO: sprint 2.
    """
    raise NotImplementedError  # TODO sprint 2
