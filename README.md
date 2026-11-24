# ElectronicCircuits1_NumericAlgorithmsForEngineering

Proyecto de análisis de circuitos electrónicos mediante métodos numéricos iterativos, organizado en cinco capas desacopladas.

> **Nota de migración**
> Este repositorio fue migrado de Spring Boot (Java) a Python/FastAPI. El código Java original se conserva en `_legacy_java/` como referencia histórica.

## Estado actual: scaffolding

La base del proyecto está creada. **No hay lógica de negocio implementada todavía**: únicamente estructura de carpetas, stubs con firmas vacías, configuración mínima y documentación. Cada responsable completará su capa durante el Sprint 1 y 2.

## Contenido del repositorio

| Ruta | Descripción |
| --- | --- |
| `proyecto_python/` | Aplicación migrada: backend FastAPI, frontend React + Vite y documentación. |
| `_legacy_java/` | Código Java/Spring Boot original, conservado como referencia histórica. |

La documentación detallada (estructura, reglas de desacoplamiento, flujo de ramas y próximos pasos) está en [`proyecto_python/README.md`](proyecto_python/README.md).

## Stack

- **Backend:** Python 3.11+, FastAPI, Uvicorn, Pydantic, NumPy.
- **Frontend:** React, Vite, Chart.js.
- **Control de versiones:** Git con ramas `main` y `develop`.

## Inicio rápido

### Backend

```bash
cd proyecto_python/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Verificar: `GET http://127.0.0.1:8000/health` → `{"status": "ok"}`.

### Frontend

```bash
cd proyecto_python/frontend
npm install
npm run dev
```

Verificar: `http://localhost:5173` muestra el placeholder del Sprint 1.

### Test de desacoplamiento

```bash
cd proyecto_python/backend
python -m unittest discover -s tests -v
```

## Flujo de ramas

- `main`: rama estable.
- `develop`: rama de integración del Sprint.
- Ramas de trabajo: `feature/capa2-control`, `feature/capa3-traduccion`, `feature/capa4-metodos`, `feature/capa5-servicios`, `feature/frontend`, `feature/docs`.

Cada integrante trabaja en su rama y abre un Pull Request hacia `develop`. No se hace push directo a `main`.
