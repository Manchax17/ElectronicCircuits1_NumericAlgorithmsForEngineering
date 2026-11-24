"""
Test de desacoplamiento entre capas.

Verifica, mediante análisis estático de los imports, que:

- ``capa4_metodos`` no importa FastAPI ni las capas 2, 3 o 5.
- ``capa3_traduccion`` y ``capa5_servicios`` no se conocen entre sí.

No contiene lógica numérica ni de negocio.
"""

import ast
import unittest
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()
