# Formato de netlist

Entrada de la Capa 3 (traducción). Describe una malla de puesta a tierra como una red de resistencias y fuentes de corriente. La implementación está en `backend/capa3_traduccion/netlist_reader.py`.

## 1. Ejemplo

Malla 3×3 con enlaces de 1 Ω, fuga de 10 Ω por nodo y una falla de 1 A en el nodo central:

```text
# Malla 3x3, enlaces de 1 ohm, fuga de 10 ohm por nodo, falla de 1 A en el nodo 5
.malla 3 3
R1  1 2 1
R2  2 3 1
R3  4 5 1
R4  5 6 1
R5  7 8 1
R6  8 9 1
R7  1 4 1
R8  4 7 1
R9  2 5 1
R10 5 8 1
R11 3 6 1
R12 6 9 1
R13 1 0 10      # fugas a tierra: una por nodo
R14 2 0 10
R15 3 0 10
R16 4 0 10
R17 5 0 10
R18 6 0 10
R19 7 0 10
R20 8 0 10
R21 9 0 10
I1  0 5 1.0     # inyecta 1 A en el nodo 5
```

```text
 1 ── 2 ── 3
 │    │    │
 4 ── 5 ── 6        cada nodo, además, con una R de fuga al nodo 0
 │    │    │
 7 ── 8 ── 9
```

## 2. Sintaxis

Una línea por elemento. Los campos se separan con espacios o tabulaciones.

| Línea | Significado |
| --- | --- |
| `R<id> a b ohmios` | Resistencia de `ohmios` Ω entre los nodos `a` y `b`. |
| `I<id> desde hacia amperios` | Fuente de corriente que lleva `amperios` A del nodo `desde` al nodo `hacia`. |
| `.malla filas columnas [separacion_m]` | Opcional. Declara que los nodos forman una cuadrícula (para el mapa de calor) y, si se da, la distancia entre nodos vecinos en metros. |
| `# texto` | Comentario, en línea propia o al final de una línea. |
| línea vacía | Se ignora. |

- **Nombres:** `R` o `I` seguido de un identificador (`R1`, `R_fuga3`, `I1`). No distinguen mayúsculas (`r1` = `R1`) y no pueden repetirse.
- **Valores:** números decimales con punto, se admite notación científica (`1e-3`, `2.5E2`). No se admiten sufijos tipo `1k`: escriba `1000`.
- **Nodo 0:** es la tierra profunda, la referencia de potencial (V = 0). No es una incógnita.
- **Nodos 1..N:** enteros consecutivos, sin huecos. El nodo `k` de la netlist es el índice `k-1` del vector de potenciales.

### 2.1 Fugas a tierra

La fuga de corriente al terreno se escribe como resistencias hacia el nodo 0. Son obligatorias: sin ellas la matriz `G` tiene filas que suman cero, es singular y el sistema admite infinitas soluciones. Por eso la Capa 3 rechaza cualquier netlist en la que un grupo de nodos no tenga un camino resistivo hasta el nodo 0.

### 2.2 Sentido de las fuentes

`I1 0 5 1.0` lleva 1 A **desde** la tierra **hacia** el nodo 5, es decir, inyecta la corriente de falla en el nodo 5. En el vector `b`: `b[hacia] += amperios` y `b[desde] -= amperios`; el término del nodo 0 se omite.

### 2.3 Directiva `.malla`

Con `.malla F C`, el nodo `k` ocupa la fila `(k-1) // C` y la columna `(k-1) % C`, con la fila 0 arriba. `F × C` debe ser igual al número de nodos. Si la netlist no la incluye, la conversión a grilla necesita que se indiquen las dimensiones aparte.

## 3. Reglas de error

Toda netlist inválida produce un `ErrorNetlist` con un mensaje en español y, cuando aplica, el número de línea. Se propone que la Capa 2 lo traduzca a una respuesta HTTP 422 con ese mensaje.

| Situación | Ejemplo | Mensaje (resumen) |
| --- | --- | --- |
| Elemento desconocido | `C1 1 0 5` | Componente desconocido; se esperaba R o I |
| Sin identificador | `R 1 0 10` | Necesita un identificador |
| Número de campos incorrecto | `R1 1 0` | Debe tener 3 campos después del nombre |
| Nodo no entero o negativo | `R1 a 0 10`, `R1 -1 0 10` | No es un entero / es negativo |
| Valor no numérico o no finito | `R1 1 0 diez`, `R1 1 0 inf` | No es un número / no es finito |
| Resistencia ≤ 0 | `R1 1 0 0` | Debe ser positiva |
| Elemento entre un nodo y sí mismo | `R1 3 3 5` | Conecta el nodo consigo mismo |
| Nombre repetido | dos `R1` | Ya se usó en la línea N |
| Directiva desconocida o mal formada | `.nodos 3`, `.malla 0 3` | Directiva desconocida / dimensiones positivas |
| `.malla` repetida | dos `.malla` | Aparece más de una vez |
| Netlist sin resistencias | archivo vacío | No contiene resistencias |
| Huecos en la numeración | nodos 1 y 3 sin 2 | Faltan: 2 |
| Fuente en un nodo sin resistencias | `I1 0 7 1` y el nodo 7 sin `R` | El nodo no tiene ninguna resistencia |
| Nodos sin camino a tierra | isla `R3 3 4 1` sin fuga | Sin camino resistivo a tierra; G sería singular |
| `.malla` incoherente | `.malla 2 2` con 9 nodos | Declara 4 nodos, la netlist tiene 9 |

Las fuentes con valor 0 o negativo se aceptan: una corriente negativa equivale a invertir el sentido.

## 4. Salida de la Capa 3

`construir_sistema(netlist)` devuelve el formato disperso del contrato entre capas:

```json
{
  "n": 9,
  "diagonal": [2.1, 3.1, 2.1, 3.1, 4.1, 3.1, 2.1, 3.1, 2.1],
  "vecinos": [[[1, -1.0], [3, -1.0]], [[0, -1.0], [2, -1.0], [4, -1.0]], "..."],
  "b": [0, 0, 0, 0, 1.0, 0, 0, 0, 0]
}
```

- `diagonal[i]` = `G_ii`: suma de las conductancias que tocan el nodo `i+1`, incluida la fuga.
- `vecinos[i]` = lista de `[j, G_ij]` con `j ≠ i`, ordenada por `j`. `G_ij = -1/R`. Las resistencias en paralelo entre el mismo par se suman.
- `b[i]` = corriente neta inyectada en el nodo `i+1`.

Es un `dict` de tipos nativos, serializable a JSON. La Capa 2 lo convierte a `MatrizDispersa` antes de llamar a la Capa 4.

Para volver del vector solución a algo interpretable están `potenciales_por_nodo(V)` (tabla `nodo → potencial`) y `potenciales_a_grilla(V, geometria)` (matriz `filas × columnas` para el mapa de calor). `grilla_a_potenciales(grilla)` hace el camino contrario, útil para cargar las mediciones del montaje físico.

## 5. Mallas sintéticas

`generar_malla(filas, columnas, r_enlace, r_fuga, nodo_falla, corriente, separacion_m=None)` escribe la netlist de una malla rectangular en este mismo formato. La usan los casos de estudio (10×10, 20×20, 50×50) y produce, para 3×3, exactamente el sistema del ejemplo anterior.
