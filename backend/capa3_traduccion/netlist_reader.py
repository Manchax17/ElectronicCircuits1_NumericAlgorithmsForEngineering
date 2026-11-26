"""
Capa 3 — Traducción: lectura de netlist.

Convierte el texto de una netlist (ver ``docs/formato_netlist.md``) en una
representación intermedia (:class:`Netlist`) independiente del solver.
No construye matrices: eso lo hace :mod:`capa3_traduccion.constructor_sistema`.

Solo usa la biblioteca estándar y no importa ninguna otra capa.

Rol responsable: especialista de datos.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

NODO_TIERRA = 0


class ErrorNetlist(ValueError):
    """Error de formato o de planteamiento en una netlist.

    ``linea`` es el número de línea (desde 1) donde se detectó el problema, o
    ``None`` si el error es global (por ejemplo, un nodo sin camino a tierra).
    """

    def __init__(self, mensaje: str, linea: int | None = None) -> None:
        self.mensaje = mensaje
        self.linea = linea
        prefijo = f"Línea {linea}: " if linea is not None else ""
        super().__init__(prefijo + mensaje)


@dataclass(frozen=True)
class Resistencia:
    """Resistencia ``nombre`` de ``ohmios`` entre los nodos ``a`` y ``b``."""

    nombre: str
    a: int
    b: int
    ohmios: float
    linea: int


@dataclass(frozen=True)
class FuenteCorriente:
    """Fuente de corriente que lleva ``amperios`` del nodo ``desde`` al nodo ``hacia``.

    Con la convención del proyecto, ``I1 0 5 1.0`` inyecta 1 A en el nodo 5.
    """

    nombre: str
    desde: int
    hacia: int
    amperios: float
    linea: int


@dataclass(frozen=True)
class GeometriaMalla:
    """Disposición rectangular opcional declarada con ``.malla``.

    El nodo ``k`` (desde 1) ocupa la fila ``(k-1) // columnas`` y la columna
    ``(k-1) % columnas``. ``separacion_m`` es la distancia entre nodos vecinos.
    """

    filas: int
    columnas: int
    separacion_m: float | None = None


@dataclass
class Netlist:
    """Representación intermedia de una netlist ya validada."""

    num_nodos: int
    resistencias: list[Resistencia] = field(default_factory=list)
    fuentes: list[FuenteCorriente] = field(default_factory=list)
    geometria: GeometriaMalla | None = None


# --------------------------------------------------------------------------- #
# Lectura
# --------------------------------------------------------------------------- #


def leer_netlist(texto: str) -> Netlist:
    """Parsea y valida una netlist.

    Reglas (detalladas en ``docs/formato_netlist.md``):

    - Una línea por componente: ``R<id> a b ohmios`` o ``I<id> desde hacia amperios``.
    - ``#`` inicia un comentario (línea completa o al final de la línea).
    - El nodo ``0`` es la tierra profunda; los demás nodos van de 1 a N sin huecos.
    - Directiva opcional ``.malla filas columnas [separacion_m]``.

    Además de la sintaxis, valida que el sistema quede bien planteado: cada
    nodo debe tener un camino resistivo a tierra, de lo contrario ``G`` sería
    singular.

    Raises:
        ErrorNetlist: con el número de línea cuando aplica.
    """
    if not isinstance(texto, str):
        raise ErrorNetlist("La netlist debe ser texto.")

    resistencias: list[Resistencia] = []
    fuentes: list[FuenteCorriente] = []
    geometria: GeometriaMalla | None = None
    nombres_vistos: dict[str, int] = {}

    for numero, linea_cruda in enumerate(texto.splitlines(), start=1):
        linea = linea_cruda.split("#", 1)[0].strip()
        if not linea:
            continue

        campos = linea.split()
        cabeza = campos[0]

        if cabeza.startswith("."):
            if geometria is not None:
                raise ErrorNetlist("La directiva .malla aparece más de una vez.", numero)
            geometria = _leer_directiva(campos, numero)
            continue

        tipo = cabeza[0].upper()
        if tipo not in ("R", "I"):
            raise ErrorNetlist(
                f"Componente '{cabeza}' desconocido; se esperaba R (resistencia) o I (fuente de corriente).",
                numero,
            )
        if len(cabeza) == 1:
            raise ErrorNetlist(f"El componente '{cabeza}' necesita un identificador, por ejemplo {tipo}1.", numero)
        if len(campos) != 4:
            raise ErrorNetlist(
                f"'{cabeza}' debe tener 3 campos después del nombre (nodo, nodo, valor); tiene {len(campos) - 1}.",
                numero,
            )

        nombre = cabeza.upper()
        if nombre in nombres_vistos:
            raise ErrorNetlist(
                f"El nombre '{cabeza}' ya se usó en la línea {nombres_vistos[nombre]}.", numero
            )
        nombres_vistos[nombre] = numero

        nodo_1 = _leer_nodo(campos[1], numero)
        nodo_2 = _leer_nodo(campos[2], numero)
        valor = _leer_numero(campos[3], numero)

        if nodo_1 == nodo_2:
            raise ErrorNetlist(f"'{cabeza}' conecta el nodo {nodo_1} consigo mismo.", numero)

        if tipo == "R":
            if valor <= 0:
                raise ErrorNetlist(f"La resistencia '{cabeza}' debe ser positiva (valor: {valor}).", numero)
            resistencias.append(Resistencia(cabeza, nodo_1, nodo_2, valor, numero))
        else:
            fuentes.append(FuenteCorriente(cabeza, nodo_1, nodo_2, valor, numero))

    if not resistencias:
        raise ErrorNetlist("La netlist no contiene resistencias.")

    num_nodos = _validar_numeracion(resistencias, fuentes)
    _validar_camino_a_tierra(num_nodos, resistencias)
    if geometria is not None and geometria.filas * geometria.columnas != num_nodos:
        raise ErrorNetlist(
            f".malla declara {geometria.filas}x{geometria.columnas} = "
            f"{geometria.filas * geometria.columnas} nodos, pero la netlist tiene {num_nodos}."
        )

    return Netlist(num_nodos, resistencias, fuentes, geometria)


# --------------------------------------------------------------------------- #
# Auxiliares
# --------------------------------------------------------------------------- #


def _leer_nodo(texto: str, linea: int) -> int:
    try:
        nodo = int(texto)
    except ValueError:
        raise ErrorNetlist(f"El nodo '{texto}' no es un entero.", linea) from None
    if nodo < 0:
        raise ErrorNetlist(f"El nodo {nodo} es negativo; los nodos van de 0 (tierra) en adelante.", linea)
    return nodo


def _leer_numero(texto: str, linea: int) -> float:
    try:
        valor = float(texto)
    except ValueError:
        raise ErrorNetlist(f"El valor '{texto}' no es un número.", linea) from None
    if not math.isfinite(valor):
        raise ErrorNetlist(f"El valor '{texto}' no es finito.", linea)
    return valor


def _leer_directiva(campos: list[str], linea: int) -> GeometriaMalla:
    if campos[0].lower() != ".malla":
        raise ErrorNetlist(f"Directiva '{campos[0]}' desconocida; la única soportada es .malla.", linea)
    if len(campos) not in (3, 4):
        raise ErrorNetlist("Uso: .malla filas columnas [separacion_m]", linea)

    dimensiones = []
    for texto in campos[1:3]:
        try:
            valor = int(texto)
        except ValueError:
            raise ErrorNetlist(f"La dimensión '{texto}' de .malla no es un entero.", linea) from None
        if valor <= 0:
            raise ErrorNetlist("Las dimensiones de .malla deben ser positivas.", linea)
        dimensiones.append(valor)

    separacion = None
    if len(campos) == 4:
        separacion = _leer_numero(campos[3], linea)
        if separacion <= 0:
            raise ErrorNetlist("La separación de .malla debe ser positiva.", linea)

    return GeometriaMalla(dimensiones[0], dimensiones[1], separacion)


def _validar_numeracion(resistencias: list[Resistencia], fuentes: list[FuenteCorriente]) -> int:
    """Exige nodos 1..N sin huecos y devuelve N."""
    nodos = {r.a for r in resistencias} | {r.b for r in resistencias}
    nodos |= {f.desde for f in fuentes} | {f.hacia for f in fuentes}
    nodos.discard(NODO_TIERRA)

    if not nodos:
        raise ErrorNetlist("La netlist solo conecta componentes a tierra; no hay nodos incógnita.")

    num_nodos = max(nodos)
    faltantes = sorted(set(range(1, num_nodos + 1)) - nodos)
    if faltantes:
        muestra = ", ".join(str(n) for n in faltantes[:10])
        extra = "…" if len(faltantes) > 10 else ""
        raise ErrorNetlist(
            f"Los nodos deben numerarse de 1 a {num_nodos} sin huecos; faltan: {muestra}{extra}."
        )

    nodos_resistivos = {r.a for r in resistencias} | {r.b for r in resistencias}
    for fuente in fuentes:
        for nodo in (fuente.desde, fuente.hacia):
            if nodo != NODO_TIERRA and nodo not in nodos_resistivos:
                raise ErrorNetlist(
                    f"La fuente '{fuente.nombre}' usa el nodo {nodo}, que no tiene ninguna resistencia.",
                    fuente.linea,
                )
    return num_nodos


def _validar_camino_a_tierra(num_nodos: int, resistencias: list[Resistencia]) -> None:
    """Verifica que cada componente conexa tenga una resistencia hacia el nodo 0.

    Sin ese camino, la matriz ``G`` es singular (filas que suman cero) y el
    sistema admite infinitas soluciones.
    """
    padre = list(range(num_nodos + 1))  # el índice 0 representa la tierra

    def raiz(x: int) -> int:
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    for r in resistencias:
        padre[raiz(r.a)] = raiz(r.b)

    tierra = raiz(NODO_TIERRA)
    sin_tierra = [nodo for nodo in range(1, num_nodos + 1) if raiz(nodo) != tierra]
    if sin_tierra:
        muestra = ", ".join(str(n) for n in sin_tierra[:10])
        extra = "…" if len(sin_tierra) > 10 else ""
        raise ErrorNetlist(
            "Sin camino resistivo a tierra (nodo 0) para los nodos "
            f"{muestra}{extra}: la matriz G sería singular. Agregue resistencias de fuga hacia el nodo 0."
        )
