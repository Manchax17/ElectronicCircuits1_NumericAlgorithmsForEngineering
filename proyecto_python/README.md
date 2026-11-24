# Proyecto Python — ElectronicCircuits1

Aplicación migrada a **Python + FastAPI** (backend) y **React + Vite** (frontend) para el análisis de circuitos electrónicos mediante métodos numéricos iterativos.

> **Nota de migración**
> Este repositorio fue migrado de Spring Boot (Java) a Python/FastAPI. El código Java original se conserva en `_legacy_java/` como referencia histórica.

## Estado: scaffolding

Esta entrega deja la **base del proyecto**, no la funcionalidad. Todo el código de negocio está pendiente y cada capa contiene únicamente stubs con firmas y `# TODO` asignados a su rol responsable.

| Elemento | Estado |
| --- | --- |
| Estructura de carpetas y paquetes | ✅ Creada |
| Backend mínimo con `GET /health` | ✅ Operativo |
| Stubs de las capas 2, 3, 4 y 5 | ✅ Con firmas y `# TODO` |
| Frontend placeholder (React + Vite) | ✅ Arranca sin interfaz |
| Modelo matemático documentado | ✅ `docs/modelo_matematico.md` |
| Test de desacoplamiento | ✅ Pasa |
| Validaciones, orquestación y métodos numéricos | ⛔ Pendientes (Sprint 1–2) |
| Lectura de netlist y exportación | ⛔ Pendientes (Sprint 1) |
| Vistas, componentes y servicios del frontend | ⛔ Pendientes (Sprint 1) |

## Stack

| Capa técnica | Tecnología |
| --- | --- |
| Backend / API | Python 3.11+, FastAPI, Uvicorn |
| Validación de datos | Pydantic v2 |
| Álgebra numérica | NumPy |
| Frontend | React 18, Vite 5 |
| Gráficas (previsto) | Chart.js |
| Pruebas | unittest / pytest |

## Estructura

Los archivos de control del repositorio (`.gitignore`, `_legacy_java/`) viven en la **raíz**; la aplicación está dentro de `proyecto_python/`.

```text
ElectronicCircuits1_NumericAlgorithmsForEngineering/
├── .gitignore
├── README.md                      # Nota de migración y resumen
├── _legacy_java/                  # Código Java/Spring Boot original (solo referencia)
└── proyecto_python/
    ├── README.md
    ├── backend/
    │   ├── main.py                # FastAPI mínima: solo /health
    │   ├── requirements.txt       # fastapi, uvicorn, pydantic, numpy
    │   ├── requirements-dev.txt   # pytest
    │   ├── capa2_control/
    │   │   ├── __init__.py
    │   │   └── controlador.py     # Stub (solo firmas y # TODO)
    │   ├── capa3_traduccion/
    │   │   ├── __init__.py
    │   │   └── netlist_reader.py  # Stub (solo firmas y # TODO)
    │   ├── capa4_metodos/
    │   │   ├── __init__.py
    │   │   ├── jacobi.py          # Stub
    │   │   ├── gauss_seidel.py    # Stub
    │   │   ├── sor.py             # Stub
    │   │   └── ssor.py            # Stub
    │   ├── capa5_servicios/
    │   │   ├── __init__.py
    │   │   └── exportador.py      # Stub CSV/TXT
    │   └── tests/
    │       ├── __init__.py
    │       └── test_desacoplamiento.py
    ├── frontend/
    │   ├── package.json           # Vite + React + Chart.js
    │   ├── vite.config.js
    │   ├── index.html
    │   └── src/
    │       ├── main.jsx
    │       ├── App.jsx            # Placeholder del Sprint 1
    │       ├── index.css
    │       ├── views/             # Landing, Simulacion, Comparacion,
    │       │                      # CasosReales y Validacion (vacías)
    │       ├── components/        # Vacía
    │       └── services/          # Vacía
    └── docs/
        ├── modelo_matematico.md   # Teoría GV = I (sin implementación)
        └── mockups/               # Vacía
```

## Las 5 capas

| Capa | Directorio | Responsable | Alcance del Sprint 1 |
| --- | --- | --- | --- |
| 1. Presentación | `proyecto_python/frontend/` | Diseñador UI | Vistas y componentes; solo consume HTTP de la Capa 2 |
| 2. Control | `proyecto_python/backend/capa2_control/` | Líder / responsable Capa 2 | Validaciones, contrato de API y orquestación |
| 3. Traducción | `proyecto_python/backend/capa3_traduccion/` | Especialista de datos | Lectura de netlist y construcción de `G` e `I` |
| 4. Métodos | `proyecto_python/backend/capa4_metodos/` | Ingeniero numérico | Jacobi, Gauss-Seidel, SOR y SSOR |
| 5. Servicios | `proyecto_python/backend/capa5_servicios/` | Datos y servicios | Exportación CSV/TXT y comparación de resultados |

## Reglas de desacoplamiento

Estas reglas son obligatorias y se verifican con `backend/tests/test_desacoplamiento.py`:

1. **`capa4_metodos` no importa FastAPI ni las otras capas.** Es matemática pura: recibe `G` e `I` y devuelve resultados. No conoce HTTP, archivos ni el controlador.
2. **`capa3_traduccion` y `capa5_servicios` no se conocen entre sí.** La traducción no exporta y la exportación no parsea netlists.
3. **`capa2_control` es la única que conoce a las demás.** Orquesta el flujo y es el único punto de entrada de la aplicación.
4. **El frontend solo habla con `capa2_control` por HTTP.** No importa código Python ni accede directamente a las capas 3, 4 o 5.

Reglas adicionales:

- Ninguna capa importa `_legacy_java/`; ese directorio es solo referencia histórica.
- Los stubs no deben llenarse con lógica de otra capa. Si una tarea cruza responsabilidades, se coordina con el líder.
- La Capa 2 puede importar las capas 3, 4 y 5; lo contrario está prohibido.
- Las capas 3, 4 y 5 no crean rutas FastAPI.

## Flujo de ramas

```text
main                  # estable
└── develop           # integración del sprint
    ├── feature/capa2-control
    ├── feature/capa3-traduccion
    ├── feature/capa4-jacobi
    ├── feature/capa5-exportacion
    ├── feature/frontend-vistas
    └── feature/docs
```

- `main` solo recibe cambios estables, mediante merge desde `develop`.
- `develop` integra el trabajo del sprint.
- Cada integrante crea una rama desde `develop` con el nombre `feature/capaX-descripcion` o `feature/integrante-descripcion`.
- El trabajo se integra a `develop` mediante Pull Request; no se hace push directo a `main`.
- Commits atómicos y descriptivos, en estilo Conventional Commits: `feat(capa4): ...`, `fix(capa2): ...`, `docs: ...`, `test: ...`, `chore: ...`, `refactor: ...`.

## Ejecución

### Backend

```bash
cd proyecto_python/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

- API: `http://127.0.0.1:8000`
- Salud: `GET http://127.0.0.1:8000/health` → `{"status": "ok"}`
- Documentación automática: `http://127.0.0.1:8000/docs`

### Frontend

```bash
cd proyecto_python/frontend
npm install
npm run dev
```

- Aplicación: `http://localhost:5173`
- Debe mostrar: **“Frontend en construcción — Sprint 1”**.

### Tests

```bash
cd proyecto_python/backend
python -m unittest discover -s tests -v
# o, con dependencias de desarrollo:
pip install -r requirements-dev.txt
pytest tests -q
```

## Próximos pasos por rol

| Rol | Tarea | Archivo(s) |
| --- | --- | --- |
| Líder / Capa 2 | Implementar validaciones y orquestación; definir endpoints y contrato de respuesta | `capa2_control/controlador.py`, `main.py` |
| Especialista de datos | Parsear netlist y construir `G`, `I` con estampado nodal | `capa3_traduccion/netlist_reader.py` |
| Ingeniero numérico | Implementar Jacobi, Gauss-Seidel, SOR y SSOR con criterios de parada | `capa4_metodos/*.py` |
| Datos y servicios | Implementar exportación CSV/TXT y comparación de resultados | `capa5_servicios/exportador.py` |
| Diseñador UI | Construir las cinco vistas y el consumo HTTP | `frontend/src/views/`, `frontend/src/components/` |
| QA / todos | Ampliar pruebas de integración y contrato | `backend/tests/` |

## Modelo matemático

La teoría completa de \(G V = I\), la obtención de \(G\) a partir de KCL y la ley de Ohm, y las propiedades de la matriz (simétrica, definida positiva, dispersa) están en [`docs/modelo_matematico.md`](docs/modelo_matematico.md).

## Código legado

El código Java/Spring Boot anterior está archivado en `../_legacy_java/` y no se ejecuta ni se importa. Su correspondencia con la estructura actual está documentada en `../_legacy_java/README.md`.
