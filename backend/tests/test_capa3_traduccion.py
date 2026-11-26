"""
Pruebas de la Capa 3 (traducción).

La referencia es el ejemplo 3×3 del contrato (sprint 1, sección 7): enlaces
de 1 Ω, fuga de 10 Ω por nodo y 1 A inyectado en el nodo 5. La solución de
referencia es la del fixture ``malla_3x3.json`` de la Capa 4.
"""

import unittest

from capa3_traduccion import (
    ErrorNetlist,
    construir_sistema,
    generar_malla,
    grilla_a_potenciales,
    leer_netlist,
    potenciales_a_grilla,
    potenciales_por_nodo,
    sistema_a_densa,
)

NETLIST_3X3 = """\
# Malla 3x3, enlaces de 1 ohm, fuga de 10 ohm por nodo, falla de 1 A en el nodo 5
R1 1 2 1
R2 2 3 1
R3 4 5 1
R4 5 6 1
R5 7 8 1
R6 8 9 1
R7 1 4 1
R8 4 7 1
R9 2 5 1
R10 5 8 1
R11 3 6 1
R12 6 9 1
R13 1 0 10
R14 2 0 10
R15 3 0 10
R16 4 0 10
R17 5 0 10
R18 6 0 10
R19 7 0 10
R20 8 0 10
R21 9 0 10
I1 0 5 1.0
"""

DIAGONAL_3X3 = [2.1, 3.1, 2.1, 3.1, 4.1, 3.1, 2.1, 3.1, 2.1]
VECINOS_3X3 = [
    [[1, -1.0], [3, -1.0]],
    [[0, -1.0], [2, -1.0], [4, -1.0]],
    [[1, -1.0], [5, -1.0]],
    [[0, -1.0], [4, -1.0], [6, -1.0]],
    [[1, -1.0], [3, -1.0], [5, -1.0], [7, -1.0]],
    [[2, -1.0], [4, -1.0], [8, -1.0]],
    [[3, -1.0], [7, -1.0]],
    [[4, -1.0], [6, -1.0], [8, -1.0]],
    [[5, -1.0], [7, -1.0]],
]
B_3X3 = [0, 0, 0, 0, 1.0, 0, 0, 0, 0]
SOLUCION_3X3 = [
    1.057641459545214,
    1.1105235325224747,
    1.057641459545214,
    1.1105235325224745,
    1.3273400317292436,
    1.1105235325224745,
    1.0576414595452137,
    1.1105235325224745,
    1.0576414595452137,
]


def residual_max(sistema: dict, v: list[float]) -> float:
    """max_i |b_i - (G v)_i| usando solo el formato disperso."""
    peor = 0.0
    for i in range(sistema["n"]):
        gv = sistema["diagonal"][i] * v[i] + sum(g * v[j] for j, g in sistema["vecinos"][i])
        peor = max(peor, abs(sistema["b"][i] - gv))
    return peor


class ConstruccionSistemaTest(unittest.TestCase):
    def test_ejemplo_3x3_coincide_con_el_contrato(self) -> None:
        sistema = construir_sistema(NETLIST_3X3)

        self.assertEqual(sistema["n"], 9)
        for calculado, esperado in zip(sistema["diagonal"], DIAGONAL_3X3):
            self.assertAlmostEqual(calculado, esperado, places=12)
        self.assertEqual(sistema["vecinos"], VECINOS_3X3)
        self.assertEqual(sistema["b"], B_3X3)

    def test_solucion_de_referencia_satisface_el_sistema(self) -> None:
        sistema = construir_sistema(NETLIST_3X3)
        self.assertLess(residual_max(sistema, SOLUCION_3X3), 1e-10)

    def test_matriz_es_simetrica_y_diagonal_dominante(self) -> None:
        sistema = construir_sistema(NETLIST_3X3)
        densa = sistema_a_densa(sistema)
        for i in range(sistema["n"]):
            for j in range(sistema["n"]):
                self.assertEqual(densa[i][j], densa[j][i])
            fuera = sum(abs(g) for _, g in sistema["vecinos"][i])
            self.assertGreater(sistema["diagonal"][i], fuera)

    def test_resistencias_en_paralelo_se_suman(self) -> None:
        sistema = construir_sistema("R1 1 2 2\nR2 1 2 2\nR3 1 0 1\nR4 2 0 1\n")
        self.assertEqual(sistema["vecinos"][0], [[1, -1.0]])
        self.assertAlmostEqual(sistema["diagonal"][0], 2.0)

    def test_fuente_entre_dos_nodos_saca_de_uno_y_mete_en_otro(self) -> None:
        sistema = construir_sistema("R1 1 0 1\nR2 2 0 1\nR3 1 2 1\nI1 1 2 0.5\n")
        self.assertEqual(sistema["b"], [-0.5, 0.5])

    def test_salida_es_json_serializable(self) -> None:
        import json

        sistema = construir_sistema(NETLIST_3X3)
        self.assertEqual(json.loads(json.dumps(sistema)), sistema)


class LecturaNetlistTest(unittest.TestCase):
    def test_comentarios_lineas_vacias_y_minusculas(self) -> None:
        netlist = leer_netlist("\n# cabecera\nr1 1 0 10   # fuga\n\ni1 0 1 2e-3\n")
        self.assertEqual(netlist.num_nodos, 1)
        self.assertEqual(netlist.fuentes[0].amperios, 0.002)

    def test_directiva_malla(self) -> None:
        netlist = leer_netlist(".malla 1 2 0.5\nR1 1 2 1\nR2 1 0 1\nR3 2 0 1\n")
        self.assertEqual((netlist.geometria.filas, netlist.geometria.columnas), (1, 2))
        self.assertEqual(netlist.geometria.separacion_m, 0.5)

    def assertErrorEnLinea(self, texto: str, linea: int | None, fragmento: str) -> None:
        with self.assertRaises(ErrorNetlist) as ctx:
            leer_netlist(texto)
        self.assertEqual(ctx.exception.linea, linea)
        self.assertIn(fragmento, str(ctx.exception))

    def test_errores_de_sintaxis(self) -> None:
        casos = [
            ("R1 1 0 10\nC1 1 0 5\n", 2, "desconocido"),
            ("R1 1 0\n", 1, "3 campos"),
            ("R1 1 0 diez\n", 1, "no es un número"),
            ("R1 a 0 10\n", 1, "no es un entero"),
            ("R1 -1 0 10\n", 1, "negativo"),
            ("R1 1 0 0\n", 1, "positiva"),
            ("R1 1 0 -5\n", 1, "positiva"),
            ("R1 1 1 5\n", 1, "consigo mismo"),
            ("R1 1 0 10\nR1 1 0 5\n", 2, "ya se usó"),
            ("R 1 0 10\n", 1, "identificador"),
            ("R1 1 0 inf\n", 1, "no es finito"),
            (".nodos 3\nR1 1 0 1\n", 1, "desconocida"),
            (".malla 0 3\nR1 1 0 1\n", 1, "positivas"),
        ]
        for texto, linea, fragmento in casos:
            with self.subTest(texto=texto):
                self.assertErrorEnLinea(texto, linea, fragmento)

    def test_errores_de_planteamiento(self) -> None:
        casos = [
            ("", None, "no contiene resistencias"),
            ("# solo comentarios\n", None, "no contiene resistencias"),
            ("R1 1 0 1\nR2 3 0 1\n", None, "faltan: 2"),
            ("R1 1 2 1\nR2 2 0 1\nR3 3 4 1\n", None, "nodos 3, 4"),
            (".malla 2 2\nR1 1 0 1\n", None, ".malla declara 2x2"),
        ]
        for texto, linea, fragmento in casos:
            with self.subTest(texto=texto):
                self.assertErrorEnLinea(texto, linea, fragmento)

    def test_fuente_en_nodo_sin_resistencias(self) -> None:
        self.assertErrorEnLinea(
            "R1 1 0 1\nR2 1 2 1\nR3 2 0 1\nI1 0 3 1\n", 4, "no tiene ninguna resistencia"
        )


class ConversionResultadosTest(unittest.TestCase):
    def test_tabla_por_nodo_usa_numeracion_de_netlist(self) -> None:
        tabla = potenciales_por_nodo(SOLUCION_3X3)
        self.assertEqual(tabla[4], {"nodo": 5, "indice": 4, "potencial": SOLUCION_3X3[4]})

    def test_grilla_ida_y_vuelta(self) -> None:
        grilla = potenciales_a_grilla(SOLUCION_3X3, filas=3, columnas=3)
        self.assertEqual(len(grilla), 3)
        self.assertEqual(grilla[1][1], SOLUCION_3X3[4])  # el centro es el nodo 5
        self.assertEqual(grilla_a_potenciales(grilla), SOLUCION_3X3)

    def test_grilla_desde_geometria_de_la_netlist(self) -> None:
        netlist = leer_netlist(generar_malla(2, 3, 1, 10, 1, 1.0))
        grilla = potenciales_a_grilla([1, 2, 3, 4, 5, 6], netlist.geometria)
        self.assertEqual(grilla, [[1, 2, 3], [4, 5, 6]])

    def test_errores_de_conversion(self) -> None:
        with self.assertRaises(ValueError):
            potenciales_a_grilla(SOLUCION_3X3, filas=2, columnas=4)
        with self.assertRaises(ValueError):
            potenciales_a_grilla(SOLUCION_3X3)
        with self.assertRaises(ValueError):
            potenciales_por_nodo([])
        with self.assertRaises(ValueError):
            potenciales_por_nodo([1.0, float("nan")])
        with self.assertRaises(ValueError):
            grilla_a_potenciales([[1, 2], [3]])


class GeneradorMallasTest(unittest.TestCase):
    def test_malla_3x3_generada_equivale_al_ejemplo_del_contrato(self) -> None:
        generada = construir_sistema(generar_malla(3, 3, 1, 10, 5, 1.0))
        manual = construir_sistema(NETLIST_3X3)
        self.assertEqual(generada, manual)

    def test_conteo_de_componentes(self) -> None:
        filas, columnas = 4, 5
        netlist = leer_netlist(generar_malla(filas, columnas, 0.5, 20, 1, 100, separacion_m=7))
        enlaces = filas * (columnas - 1) + (filas - 1) * columnas
        self.assertEqual(len(netlist.resistencias), enlaces + filas * columnas)
        self.assertEqual(netlist.geometria.separacion_m, 7)

    def test_malla_50x50_tiene_a_lo_sumo_cinco_entradas_por_fila(self) -> None:
        sistema = construir_sistema(generar_malla(50, 50, 1, 10, 1275, 1000))
        self.assertEqual(sistema["n"], 2500)
        self.assertLessEqual(max(len(fila) for fila in sistema["vecinos"]) + 1, 5)

    def test_parametros_invalidos(self) -> None:
        for args in [(0, 3, 1, 10, 1, 1), (3, 3, 0, 10, 1, 1), (3, 3, 1, 10, 10, 1)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                generar_malla(*args)


if __name__ == "__main__":
    unittest.main()
