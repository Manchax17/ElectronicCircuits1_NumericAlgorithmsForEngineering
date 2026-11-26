# Contrato de API

> **Documento compartido:** cada responsable añade su sección. «Formato interno disperso» corresponde a N (Ingeniero numérico); la sección de endpoints y respuestas de la Capa 2 la añade L (Líder).

## Endpoints (pendiente, Capa 2)

## Formato interno disperso

La matriz se representa con la dimensión, una diagonal separada, las entradas fuera de diagonal agrupadas por fila y el vector derecho `b`. El siguiente objeto `matriz` se copia del fixture completo de la malla 3×3 en `backend/tests/fixtures/malla_3x3.json`:

```json
{
  "n": 9,
  "diagonal": [2.1, 3.1, 2.1, 3.1, 4.1, 3.1, 2.1, 3.1, 2.1],
  "vecinos": [
    [[1, -1.0], [3, -1.0]],
    [[0, -1.0], [2, -1.0], [4, -1.0]],
    [[1, -1.0], [5, -1.0]],
    [[0, -1.0], [4, -1.0], [6, -1.0]],
    [[1, -1.0], [3, -1.0], [5, -1.0], [7, -1.0]],
    [[2, -1.0], [4, -1.0], [8, -1.0]],
    [[3, -1.0], [7, -1.0]],
    [[4, -1.0], [6, -1.0], [8, -1.0]],
    [[5, -1.0], [7, -1.0]]
  ],
  "b": [0, 0, 0, 0, 1.0, 0, 0, 0, 0]
}
```

Reglas de representación:

- Los índices empiezan en 0: el nodo 1 del netlist es el índice 0.
- El nodo 0 (tierra) no es una incógnita.
- `diagonal[i]` contiene por separado el elemento `G_ii`.
- `vecinos[i]` contiene pares `[j, G_ij]`, con `j` distinto de `i`; no incluye la diagonal.
- La matriz es simétrica: si `j` está en `vecinos[i]`, entonces `i` está en `vecinos[j]` con el mismo valor.
- En este modelo resistivo, `G_ij` suele ser negativo para nodos conectados por una resistencia.
- Los pares de `vecinos` pueden llegar como listas o tuplas; la Capa 4 los trata igual.

### Justificación de memoria

Una malla de 50×50 contiene 2500 incógnitas. En formato denso tendría 6 250 000 entradas. En formato disperso de diagonal más vecinos hay hasta 5 entradas por fila, contando la diagonal: unas 12 500 entradas en total. El formato disperso evita reservar y recorrer las entradas nulas.

**Acordado por:** N (Ingeniero numérico) y D (Especialista de datos)

N: ____________________    D: ____________________    Fecha: ____________________
