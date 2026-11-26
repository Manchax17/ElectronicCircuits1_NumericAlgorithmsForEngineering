# ElectronicCircuits1 — Análisis de circuitos con métodos numéricos

Aplicación para el análisis de circuitos electrónicos mediante métodos numéricos iterativos, organizada en cinco capas desacopladas. El backend está migrado a **Python + FastAPI** y el frontend a **React + Vite**.

> **Nota de migración**
> Este repositorio fue migrado de Spring Boot (Java) a Python/FastAPI. El código Java original se conservó en `_legacy_java/` y se retiró del árbol de trabajo en el commit `8e50ea7`; permanece disponible en el historial de Git como referencia histórica.

## Estado actual — Sprint 1

| Elemento | Estado |
| --- | --- |
| Estructura del repositorio (`backend/`, `frontend/`, `docs/`) | ✅ Creada |
| Backend mínimo con `GET /health` | ✅ Operativo |
| Capa 3: lectura de netlist, construcción dispersa de `G·V = b`, conversión de resultados y generador de mallas | ✅ Implementada y probada |
| Capa 4: tipos compartidos, firmas y pruebas de contrato | ✅ Definidos |
| Capa 4: Jacobi, Gauss-Seidel, SOR y SSOR | ⛔ Pendiente (Sprint 2) |
| Capa 2: validaciones, contrato de API y orquestación | ⛔ Pendiente (stub) |
| Capa 5: exportación CSV/TXT y comparación | ⛔ Pendiente (stub) |
| Frontend: base Vite + React | ✅ Arranca en modo placeholder |
| Frontend: vistas y componentes | ⛔ Pendientes (Sprint 1) |
| Documentación y mockups | ✅ Disponibles en `docs/` |
| Pruebas de desacoplamiento y de capas 3–4 | ✅ 36 pruebas pasan |

## Stack

| Capa técnica | Tecnología |
| --- | --- |
| Backend / API | Python 3.11+, FastAPI, Uvicorn |
| Validación de datos | Pydantic v2 |
| Álgebra numérica | NumPy |
| Frontend | React 18, Vite 5 |
| Gráficas (previsto) | Chart.js |
| Pruebas | pytest |

## Estructura

```text
ElectronicCircuits1_NumericAlgorithmsForEngineering/
├── .gitignore
├── README.md
├── backend/
│   ├── main.py                     # FastAPI mínima: GET /health
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── capa2_control/
│   │   ├── __init__.py
│   │   └── controlador.py          # Stub: firmas y # TODO
│   ├── capa3_traduccion/
│   │   ├── __init__.py
│   │   ├── netlist_reader.py       # Lectura y validación de netlist
│   │   ├── constructor_sistema.py  # Estampado nodal → sistema disperso
│   │   ├── conversion_resultados.py# Vector solución → tabla / grilla
│   │   └── generador_mallas.py     # Netlists sintéticas de malla
│   ├── capa4_metodos/
│   │   ├── __init__.py
│   │   ├── tipos.py                # MatrizDispersa, ResultadoSolucion
│   │   ├── jacobi.py               # Firma + TODO Sprint 2
│   │   ├── gauss_seidel.py         # Firma + TODO Sprint 2
│   │   ├── sor.py                  # Firma + TODO Sprint 2
│   │   └── ssor.py                 # Firma + TODO Sprint 2
│   ├── capa5_servicios/
│   │   ├── __init__.py
│   │   └── exportador.py           # Stub CSV/TXT
│   └── tests/
│       ├── fixtures/malla_3x3.json
│       ├── referencia.py
│       ├── test_capa3_traduccion.py
│       ├── test_contrato_disperso.py
│       ├── test_desacoplamiento.py
│       ├── test_firmas_capa4.py
│       └── test_fixture_3x3.py
├── frontend/
│   ├── package.json                # Vite + React + Chart.js
│   ├── package-lock.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx                 # Placeholder del Sprint 1
│       ├── index.css
│       ├── components/             # Vacía
│       ├── services/               # Vacía
│       └── views/                  # Landing, Simulacion, Comparacion,
│                                   # CasosReales y Validacion (vacías)
└── docs/
    ├── modelo_matematico.md        # Teoría G·V = b
    ├── formato_netlist.md          # Sintaxis y reglas de error
    ├── contrato_api.md             # Formato disperso y contrato de API
    └── mockups/                    # Mockups HTML, capturas y guía visual
```

## Las 5 capas

| Capa | Directorio | Responsable | Estado |
| --- | --- | --- | --- |
| 1. Presentación | `frontend/` | Diseñador UI | Placeholder; solo debe consumir HTTP de la Capa 2 |
| 2. Control | `backend/capa2_control/` | Líder / responsable Capa 2 | Stub; validaciones y orquestación pendientes |
| 3. Traducción | `backend/capa3_traduccion/` | Especialista de datos | Implementada en Sprint 1 |
| 4. Métodos | `backend/capa4_metodos/` | Ingeniero numérico | Contratos y firmas listos; algoritmos pendientes |
| 5. Servicios | `backend/capa5_servicios/` | Datos y servicios | Stub; exportación pendiente |

### Flujo de datos previsto

```text
Netlist
   │
   ▼
Capa 3: G·V = b (formato disperso)
   │
   ▼
Capa 4: Jacobi / Gauss-Seidel / SOR / SSOR
   │
   ▼
Capa 2: valida, orquesta y expone la API
   │                         │
   ▼                         ▼
Frontend (HTTP)          Capa 5: CSV / TXT
```

## Reglas de desacoplamiento

Obligatorias y verificadas por `backend/tests/test_desacoplamiento.py`:

1. **`capa4_metodos` no importa FastAPI ni las otras capas.** Es matemática pura: recibe la matriz y el vector, y devuelve resultados.
2. **`capa3_traduccion` y `capa5_servicios` no se conocen entre sí.** La traducción no exporta y la exportación no parsea netlists.
3. **`capa2_control` es la única que conoce a las demás.** Orquesta el flujo y es el único punto de entrada de la aplicación.
4. **El frontend solo habla con `capa2_control` por HTTP.** No importa código Python ni accede directamente a las capas 3, 4 o 5.

Reglas adicionales:

- La Capa 2 puede importar las capas 3, 4 y 5; lo contrario está prohibido.
- Las capas 3, 4 y 5 no crean rutas FastAPI.
- Ninguna capa depende del código Java legado; este solo vive en el historial de Git.
- Si una tarea cruza responsabilidades, se coordina con el líder antes de implementarla.

## Documentación

| Documento | Contenido |
| --- | --- |
| [`docs/modelo_matematico.md`](docs/modelo_matematico.md) | Obtención de `G` desde KCL y la ley de Ohm, propiedades de la matriz y convergencia |
| [`docs/formato_netlist.md`](docs/formato_netlist.md) | Sintaxis de netlist, componentes y reglas de error |
| [`docs/contrato_api.md`](docs/contrato_api.md) | Formato interno disperso acordado entre las capas 3 y 4 |
| [`docs/mockups/README.md`](docs/mockups/README.md) | Índice de mockups, mapa de calor y semáforo de riesgo |

## Ejecución

### Backend

```bash
cd backend
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
cd frontend
npm install
npm run dev
```

- Aplicación: `http://localhost:5173`
- Debe mostrar: **“Frontend en construcción — Sprint 1”**.

### Pruebas

```bash
cd backend
source .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest -q
```

Las pruebas cubren la Capa 3, los contratos de la Capa 4, el fixture 3×3 y las reglas de desacoplamiento.

## Ramas y flujo de trabajo

```text
main                  # producción / entregas estables
└── develop           # integración del sprint (rama por defecto)
    ├── feature/capa2-control
    ├── feature/capa3-traduccion
    ├── feature/capa4-jacobi
    ├── feature/capa5-exportacion
    ├── feature/frontend-vistas
    └── feature/docs
```

- Cada integrante crea su rama desde `develop`: `feature/capaX-descripcion` o `feature/integrante-descripcion`.
- El trabajo se integra a `develop` mediante Pull Request.
- `main` solo recibe versiones estables desde `develop`.
- Commits atómicos en estilo Conventional Commits: `feat(capa4): ...`, `fix(capa2): ...`, `docs: ...`, `test: ...`, `chore: ...`, `refactor: ...`.

## Próximos pasos por rol

| Rol | Tarea | Archivo(s) |
| --- | --- | --- |
| Líder / Capa 2 | Validaciones, endpoints y orquestación | `capa2_control/controlador.py`, `main.py` |
| Especialista de datos | Revisión y ampliación de netlists y conversiones | `capa3_traduccion/` |
| Ingeniero numérico | Implementar Jacobi, Gauss-Seidel, SOR y SSOR | `capa4_metodos/*.py` |
| Datos y servicios | Exportación CSV/TXT y comparación de resultados | `capa5_servicios/exportador.py` |
| Diseñador UI | Construir las cinco vistas y el consumo HTTP | `frontend/src/views/`, `frontend/src/components/` |
| QA / todos | Pruebas de integración y de contrato de API | `backend/tests/` |

## Código legado

El código Java/Spring Boot original se retiró del árbol actual en el commit `8e50ea7` y no se ejecuta ni se importa. Se puede consultar en el historial:

```bash
git log --oneline --all -- _legacy_java
git show 8e50ea7^:_legacy_java/pom.xml
```
