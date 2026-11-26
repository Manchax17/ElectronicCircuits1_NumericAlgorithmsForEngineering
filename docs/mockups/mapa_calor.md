# Especificación: mapa de calor y semáforo de riesgo

Componente de la Capa 1 usado en **Casos de estudio** (y en miniatura en Simulación). Muestra la salida de la Capa 3 `potenciales_a_grilla()` y las zonas de riesgo. Mockup de referencia: [`4_casos.html`](4_casos.html) / [`capturas/4_casos.png`](capturas/4_casos.png).

## 1. Dos capas, no una

El proyecto pide "zonas verde, amarilla y roja". Se dibujan **dos mapas lado a lado con la misma geometría**, en lugar de un único mapa arcoíris:

| Mapa | Qué codifica | Tipo de color |
| --- | --- | --- |
| **Potencial del terreno** | Magnitud continua: V en cada nodo | Secuencial de un solo tono (azul claro → azul oscuro) |
| **Zonas de riesgo** | Estado discreto: tensión de paso o toque frente al límite | Semáforo verde / amarillo / rojo, **con icono** |

Motivos: (1) un arcoíris rojo-verde no lo distingue ~8 % de los hombres (daltonismo) y no tiene orden perceptual; (2) "mucho potencial" no es lo mismo que "peligro": el riesgo depende de las **diferencias** entre puntos, no del valor absoluto. Mezclarlos en un solo color engaña.

## 2. Paleta

### 2.1 Potencial (secuencial)

13 pasos del más claro (mínimo de la malla) al más oscuro (máximo). La escala se normaliza **por escenario** (mín → máx del mapa mostrado), y la leyenda muestra esos dos valores en V.

```
#cce3fd #b6d5f8 #9dc8f7 #84b9f3 #6aabf1 #519ced #338ced #257de0 #2370cd #1b64be #1757ac #0f4a96 #0e3d7e
```

Asignación: `paso = round((V - Vmin) / (Vmax - Vmin) * 12)`.

### 2.2 Zonas (semáforo)

Para cada nodo, `r = max(E_paso / límite_paso, E_toque / límite_toque)`.

| Zona | Condición | Relleno | Icono | Texto |
| --- | --- | --- | --- | --- |
| Verde | `r < 0,8` | `#c8eccd` | ninguno | "Dentro del límite" |
| Amarilla | `0,8 ≤ r ≤ 1` | `#fbb315` | `!` en `#0b0b0b` | "Cerca del límite" |
| Roja | `r > 1` | `#dc3c3d` | `✕` en `#ffffff` | "Supera el límite" |

- El umbral del 80 % es una **propuesta** de diseño; se confirma con el ingeniero numérico junto con el escalado de IEEE Std 80.
- Estos colores de estado se reservan para riesgo: **no** se reutilizan como colores de series en otras gráficas.
- El color nunca va solo: icono en la celda + leyenda con texto + fila "Zona" en el tooltip.

### 2.3 Veredicto

`INSEGURO` si existe al menos una celda roja; si no, `SEGURO`. Se muestra con icono (✓ / ✕), palabra y frase que diga **qué** límite se superó.

## 3. Geometría

| Malla | Tamaño de celda | Separación | Lado total aprox. |
| --- | --- | --- | --- |
| 3×3 a 10×10 | 40 px | 2 px | ≤ 400 px |
| 20×20 | 22 px | 2 px | 444 px |
| 50×50 | 9 px | 1 px | 450 px |

- Regla: `celda = floor(450 / columnas)`, mínimo 8 px. La separación es del color de la superficie (blanco), no una línea.
- Esquinas de celda redondeadas 2 px. Fila 0 arriba; nodo `k` en fila `(k-1) // columnas`, columna `(k-1) % columnas` (misma convención de la directiva `.malla`).
- **Nodo de falla:** contorno negro de 2 px y ⚡ en el mapa de potencial; contorno negro en el de zonas.

## 4. Interacción

| Acción | Comportamiento |
| --- | --- |
| Pasar el cursor por una celda | Contorno blanco + negro en la celda **en ambos mapas a la vez** y tarjeta flotante. |
| Tarjeta flotante | Nodo y posición (fila, col.), potencial (V), tensión de paso (V), tensión de toque (V o "— sin estructura"), zona. Valores en cifras tabulares. |
| Área sensible | La celda completa más la separación (sin huecos muertos entre celdas). |
| Clic en una celda | Fija la selección (la tarjeta queda visible) y en Simulación la usa como nodo de falla. |
| Teclado | Las flechas mueven la selección; `Enter` fija; `Esc` libera. |
| Salir del mapa | La tarjeta desaparece salvo que haya selección fija. |

La tarjeta se coloca a la derecha y abajo del cursor y se voltea si se saldría del contenedor.

## 5. Accesibilidad

- Cada mapa tiene `role="img"` y `aria-label` con el resumen ("Malla 20×20, falla en el nodo 1, 3 nodos en zona roja").
- Botón "Ver como tabla" debajo del mapa: la misma información en una tabla ordenable (nodo, fila, columna, V, paso, toque, zona).
- Con `forced-colors` o impresión, las zonas se distinguen por el icono y un rayado a 45° en las rojas.
- Contraste del texto de la leyenda ≥ 4,5:1 sobre la superficie.

## 6. Exportación

"⭳ Mapa PNG" genera la imagen de los dos mapas con leyenda y título del escenario (Capa 5). Los datos van en CSV con una fila por nodo: `nodo,fila,columna,potencial_V,paso_V,toque_V,zona`.

## 7. Datos que consume

Desde la API (Capa 2, `POST /veredicto`), por propuesta:

```json
{
  "filas": 20, "columnas": 20,
  "potencial": [[8063.1, 7310.4, "..."], "..."],
  "zona": [[0, 2, "..."], "..."],
  "paso": [[...]], "toque": [[...]],
  "nodo_falla": 1,
  "limites": { "paso_V": 2231, "toque_V": 681 },
  "veredicto": "INSEGURO"
}
```

`potencial` sale de `capa3_traduccion.potenciales_a_grilla()`. Los nombres de campo finales se fijan en `docs/contrato_api.md`.
