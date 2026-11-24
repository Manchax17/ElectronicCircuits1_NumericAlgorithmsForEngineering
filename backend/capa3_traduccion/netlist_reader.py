"""
Capa 3 — Traducción.

Stub del lector de netlist y constructor del sistema lineal. No implementa
parseo, estampado nodal ni construcción de matrices.

Rol responsable: especialista de datos.
"""


def leer_netlist(netlist: str) -> dict:
    """
    Stub de lectura de una netlist.

    TODO: definir y documentar la sintaxis de entrada soportada.
    TODO: parsear componentes (resistencias, fuentes, nodos de referencia).
    TODO: normalizar nombres de nodos y detectar errores de formato.
    TODO: devolver una representación intermedia independiente del solver.
    """
    pass


def construir_sistema(netlist: str) -> tuple:
    """
    Stub de construcción de ``G`` e ``I`` mediante estampado nodal.

    TODO: aplicar KCL y la ley de Ohm para llenar la matriz de conductancias.
    TODO: construir el vector de corrientes independientes.
    TODO: devolver ``(G, I)`` sin acoplarse a las capas 2, 4 o 5.
    TODO: documentar el tratamiento del nodo de referencia (tierra).
    """
    pass
