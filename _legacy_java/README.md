# _legacy_java — Código legado (Spring Boot / Java)

Este directorio conserva el código original del proyecto **ElectronicCircuits1_NumericAlgorithmsForEngineering** desarrollado con Java y Spring Boot. Se mantiene únicamente como referencia histórica y **no forma parte del build ni del stack actual**.

> Este repositorio fue migrado de Spring Boot (Java) a Python/FastAPI. El código Java original se conserva en `_legacy_java/` como referencia histórica.

## Contenido archivado

- `pom.xml`: configuración Maven del proyecto original.
- `mvnw`, `mvnw.cmd`, `.mvn/`: Maven Wrapper.
- `src/main/java/...`: paquetes originales de las capas 2 a 5 y la aplicación Spring Boot.
- `src/main/resources/application.properties`: configuración del servidor (puerto 8081).
- `src/test/java/...`: test de contexto de Spring Boot.
- `HELP.md` y `.gitattributes`: archivos auxiliares del proyecto original.

## Correspondencia con la nueva estructura

| Java (legado) | Python (actual) |
| --- | --- |
| `capa2_control/CircuitController.java` | `proyecto_python/backend/capa2_control/controlador.py` |
| `capa3_traduccion/CircuitTranslatorImpl.java` | `proyecto_python/backend/capa3_traduccion/netlist_reader.py` |
| `capa4_metodos/IterativeSolverImpl.java` | `proyecto_python/backend/capa4_metodos/` |
| `capa5_servicios/ResultComparisonServiceImpl.java` | `proyecto_python/backend/capa5_servicios/exportador.py` |
| `DemoApplication.java` | `proyecto_python/backend/main.py` |

## Reglas

- No agregar código nuevo en este directorio.
- No importar este código desde el backend en Python.
- No ejecutar Maven ni Spring Boot como parte del proyecto actual.
- Si se necesita una referencia funcional, reimplementarla en la capa correspondiente de `proyecto_python/`.
