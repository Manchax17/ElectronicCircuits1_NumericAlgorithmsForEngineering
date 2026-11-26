"""
Test de desacoplamiento entre capas.

Verifica, mediante análisis estático de los imports, que:

- ``capa4_metodos`` no importa FastAPI ni las capas 2, 3 o 5.
- ``capa3_traduccion`` y ``capa5_servicios`` no se conocen entre sí.

No contiene lógica numérica ni de negocio.
"""

import ast
import sys
import unittest
from pathlib import Path

import pytest

BACKEND_DIR = Path(__file__).resolve().parents[1]

CAPA2_DIR = BACKEND_DIR / "capa2_control"
CAPA3_DIR = BACKEND_DIR / "capa3_traduccion"
CAPA4_DIR = BACKEND_DIR / "capa4_metodos"
CAPA5_DIR = BACKEND_DIR / "capa5_servicios"

MODULOS_PROHIBIDOS_CAPA4 = {
    "fastapi",
    "capa2_control",
    "capa3_traduccion",
    "capa5_servicios",
}

MODULOS_DE_OTRAS_CAPAS = {
    "capa2_control",
    "capa3_traduccion",
    "capa5_servicios",
}


def modulos_importados(archivo: Path) -> set[str]:
    """Devuelve los módulos de nivel superior importados por un archivo."""
    arbol = ast.parse(archivo.read_text(encoding="utf-8"), filename=str(archivo))
    modulos: set[str] = set()

    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Import):
            for alias in nodo.names:
                modulos.add(alias.name.split(".")[0])
        elif isinstance(nodo, ast.ImportFrom):
            if nodo.module:
                modulos.add(nodo.module.split(".")[0])

    return modulos


def archivos_python(directorio: Path) -> list[Path]:
    """Lista los archivos Python de un directorio de capa."""
    return sorted(directorio.glob("*.py"))


def revisar_imports_capa4(directorio: Path) -> list[str]:
    """Devuelve imports prohibidos hallados en los Python de una carpeta.

    Los imports relativos se consideran internos a la capa y se permiten.
    Cada infracción incluye archivo, línea y módulo para facilitar el diagnóstico.
    """
    violaciones = []

    for archivo in sorted(directorio.rglob("*.py")):
        arbol = ast.parse(archivo.read_text(encoding="utf-8"), filename=str(archivo))

        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.Import):
                modulos = [alias.name for alias in nodo.names]
            elif isinstance(nodo, ast.ImportFrom):
                if nodo.level > 0 or nodo.module is None:
                    continue
                modulos = [nodo.module]
            else:
                continue

            for modulo in modulos:
                raiz = modulo.split(".")[0]
                ruta_archivo = archivo.relative_to(directorio)
                if raiz in MODULOS_DE_OTRAS_CAPAS:
                    violaciones.append(
                        f"{ruta_archivo}:{nodo.lineno}: módulo '{modulo}' prohibido "
                        "(import de otra capa)"
                    )
                elif raiz not in sys.stdlib_module_names:
                    violaciones.append(
                        f"{ruta_archivo}:{nodo.lineno}: módulo '{modulo}' prohibido "
                        "(no pertenece a la biblioteca estándar)"
                    )

    return violaciones


class DesacoplamientoTest(unittest.TestCase):
    def test_capa4_no_importa_fastapi_ni_otras_capas(self) -> None:
        violaciones = []

        for archivo in archivos_python(CAPA4_DIR):
            prohibidos = modulos_importados(archivo) & MODULOS_PROHIBIDOS_CAPA4
            for modulo in sorted(prohibidos):
                violaciones.append(f"{archivo.name} importa '{modulo}'")

        self.assertEqual(
            violaciones,
            [],
            "La Capa 4 debe ser independiente. Violaciones: " + ", ".join(violaciones),
        )

    def test_capa4_solo_importa_biblioteca_estandar(self) -> None:
        violaciones = revisar_imports_capa4(CAPA4_DIR)

        self.assertEqual(
            violaciones,
            [],
            "La Capa 4 solo puede importar biblioteca estándar. Violaciones: "
            + ", ".join(violaciones),
        )

    def test_capa3_y_capa5_no_se_conocen_entre_si(self) -> None:
        violaciones = []

        for archivo in archivos_python(CAPA3_DIR):
            if "capa5_servicios" in modulos_importados(archivo):
                violaciones.append(f"{archivo.name} (capa 3) importa capa5_servicios")

        for archivo in archivos_python(CAPA5_DIR):
            if "capa3_traduccion" in modulos_importados(archivo):
                violaciones.append(f"{archivo.name} (capa 5) importa capa3_traduccion")

        self.assertEqual(
            violaciones,
            [],
            "Las capas 3 y 5 deben permanecer desacopladas. Violaciones: "
            + ", ".join(violaciones),
        )

    def test_capa2_es_la_unica_que_orquesta(self) -> None:
        """Las capas 3, 4 y 5 no deben importar el controlador."""
        violaciones = []

        for directorio, nombre in (
            (CAPA3_DIR, "capa 3"),
            (CAPA4_DIR, "capa 4"),
            (CAPA5_DIR, "capa 5"),
        ):
            for archivo in archivos_python(directorio):
                if "capa2_control" in modulos_importados(archivo):
                    violaciones.append(f"{archivo.name} ({nombre}) importa capa2_control")

        self.assertEqual(
            violaciones,
            [],
            "Solo la Capa 2 puede orquestar. Violaciones: " + ", ".join(violaciones),
        )


def test_revisor_detecta_imports_prohibidos_y_permite_relativos(tmp_path: Path) -> None:
    archivo_numpy = tmp_path / "con_numpy.py"
    archivo_capa2 = tmp_path / "con_capa2.py"
    archivo_relativo = tmp_path / "interno.py"
    archivo_numpy.write_text("import numpy\n", encoding="utf-8")
    archivo_capa2.write_text("from capa2_control import x\n", encoding="utf-8")
    archivo_relativo.write_text("from .tipos import MatrizDispersa\n", encoding="utf-8")

    violaciones = revisar_imports_capa4(tmp_path)

    assert len(violaciones) == 2
    assert any(
        "con_numpy.py:1" in infraccion and "numpy" in infraccion
        for infraccion in violaciones
    )
    assert any(
        "con_capa2.py:1" in infraccion and "capa2_control" in infraccion
        for infraccion in violaciones
    )
    assert not any("interno.py" in infraccion for infraccion in violaciones)


if __name__ == "__main__":
    unittest.main()
