"""
Capa 2 — Control.

Stub del controlador. Solo contiene firmas y pendientes: en esta fase no se
implementa la orquestación ni las validaciones de negocio.

Rol responsable: líder de proyecto / Capa 2 (Control).
"""


def validar_parametros(omega: float, tol: float, max_iter: int) -> None:
    """
    Stub de validación de parámetros de entrada.

    TODO: validar que ``omega`` esté en el rango permitido por el método.
    TODO: validar que ``tol`` sea un número positivo y razonable.
    TODO: validar que ``max_iter`` sea un entero positivo.
    TODO: definir el error de dominio que se lanzará ante entradas inválidas.
    """
    pass


def resolver_circuito(
    netlist: str,
    metodo: str = "jacobi",
    omega: float = 1.0,
    tol: float = 1e-6,
    max_iter: int = 1000,
) -> dict:
    """
    Stub de orquestación del flujo completo.

    Flujo previsto (no implementado):

    1. Validar parámetros de entrada.
    2. Delegar en ``capa3_traduccion`` la lectura de la netlist y la
       construcción de ``G`` e ``I``.
    3. Delegar en ``capa4_metodos`` la resolución de ``G V = I``.
    4. Delegar en ``capa5_servicios`` la exportación de resultados.
    5. Devolver el resultado consolidado a la API.

    TODO: implementar en Sprint 1 (rol: líder de proyecto / Capa 2).
    TODO: definir el contrato de respuesta (solución, iteraciones, error, etc.).
    TODO: decidir si la exportación es síncrona o se expone como endpoint aparte.
    """
    pass


def comparar_metodos(
    netlist: str,
    metodos: list[str] | None = None,
    omega: float = 1.0,
    tol: float = 1e-6,
    max_iter: int = 1000,
) -> dict:
    """
    Stub de comparación de métodos iterativos.

    TODO: validar la lista de métodos solicitados.
    TODO: resolver el mismo sistema con cada método disponible.
    TODO: consolidar métricas por método (iteraciones, error final, tiempo).
    TODO: delegar la exportación comparativa en ``capa5_servicios``.
    """
    pass
