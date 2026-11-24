# Modelo matemático: \(G\,V = I\)

Documento de referencia teórica para la Capa 3 (traducción) y la Capa 4 (métodos numéricos). **No contiene implementación**; describe el problema que el sistema debe resolver.

## 1. Objetivo

Dado un circuito resistivo lineal con fuentes independientes, se busca el vector de voltajes nodales \(V\) que satisface el sistema lineal

\[
G\,V = I,
\]

donde:

- \(G \in \mathbb{R}^{n \times n}\) es la **matriz de conductancias** (admitancias) del circuito.
- \(V \in \mathbb{R}^{n}\) es el vector de **voltajes nodales** respecto al nodo de referencia.
- \(I \in \mathbb{R}^{n}\) es el vector de **corrientes independientes** inyectadas en cada nodo.
- \(n\) es el número de nodos desconocidos (todos menos el nodo de referencia/tierra).

Este sistema es la base del **análisis nodal modificado** en su versión resistiva y es el punto de entrada de los métodos iterativos de la Capa 4.

## 2. Notación

| Símbolo | Significado | Unidad |
| --- | --- | --- |
| \(V_a\) | Voltaje del nodo \(a\) respecto a tierra | V |
| \(R_{ab}\) | Resistencia entre los nodos \(a\) y \(b\) | \(\Omega\) |
| \(G_{ab} = 1/R_{ab}\) | Conductancia de la rama \(a\)-\(b\) | S |
| \(I_s\) | Corriente de una fuente independiente | A |
| \(G\) | Matriz de conductancias nodales | S |
| \(I\) | Vector de corrientes nodales | A |

Convención de signos: las corrientes que **salen** de un nodo se consideran positivas en la ecuación de Kirchhoff; una fuente que **inyecta** corriente hacia el nodo contribuye con signo positivo en \(I\).

## 3. Leyes fundamentales

### 3.1 Ley de corrientes de Kirchhoff (KCL)

Para cada nodo \(a\), la suma algebraica de las corrientes que salen del nodo es cero:

\[
\sum_{b \neq a} I_{a \to b} + I_{a,\text{fuentes}} = 0.
\]

### 3.2 Ley de Ohm

La corriente que circula por una resistencia \(R_{ab}\) desde \(a\) hacia \(b\) es

\[
I_{a \to b} = \frac{V_a - V_b}{R_{ab}} = G_{ab}\,(V_a - V_b).
\]

Sustituyendo en KCL y agrupando por voltajes se obtiene una ecuación lineal por nodo.

## 4. Construcción de \(G\) e \(I\) (estampado nodal)

Para cada resistencia \(R_{ab}\) conectada entre los nodos \(a\) y \(b\), con \(g = 1/R_{ab}\):

\[
G_{aa} \mathrel{+}= g, \qquad
G_{bb} \mathrel{+}= g, \qquad
G_{ab} \mathrel{-}= g, \qquad
G_{ba} \mathrel{-}= g.
\]

Para cada fuente de corriente independiente \(I_s\):

- Si la fuente **inyecta** corriente en el nodo \(a\): \(I_a \mathrel{+}= I_s\).
- Si la fuente **extrae** corriente del nodo \(a\): \(I_a \mathrel{-}= I_s\).

Las resistencias conectadas al nodo de referencia (tierra) solo aportan a su diagonal: \(G_{aa} \mathrel{+}= 1/R_{a0}\).

### 4.1 Nodo de referencia

El sistema \(G V = I\) solo tiene solución única si se fija una referencia de potencial. Se elige un nodo de tierra con \(V_0 = 0\) y se **elimina su fila y columna** de \(G\) (o se impone la condición directamente). Sin esta referencia, \(G\) es singular porque sumar una constante a todos los voltajes deja las corrientes invariantes.

### 4.2 Ejemplo mínimo (solo teoría)

Circuito con nodos 1 y 2, tierra en el nodo 0, resistencia \(R_1\) entre 1 y tierra, resistencia \(R_2\) entre 1 y 2, y una fuente de corriente \(I_s\) inyectando en el nodo 1:

\[
G =
\begin{bmatrix}
\dfrac{1}{R_1} + \dfrac{1}{R_2} & -\dfrac{1}{R_2} \\[6pt]
-\dfrac{1}{R_2} & \dfrac{1}{R_2}
\end{bmatrix},
\qquad
I =
\begin{bmatrix}
I_s \\
0
\end{bmatrix}.
\]

Resolver \(G V = I\) entrega \(V_1\) y \(V_2\). Este ejemplo muestra la estructura general: diagonal con la suma de conductancias incidentes y fuera de la diagonal los acoplamientos negativos.

## 5. Propiedades de \(G\)

### 5.1 Simetría

La ley de Ohm es recíproca, por lo que

\[
G = G^{T}.
\]

La contribución de cada resistencia es simétrica: \(G_{ab} = G_{ba} = -1/R_{ab}\).

### 5.2 Definida positiva

Para un circuito conectado, con resistencias positivas y un nodo de referencia fijo, la matriz \(G\) es **simétrica definida positiva** (SDP). Para cualquier vector \(x \neq 0\):

\[
x^{T} G x
= \sum_{(a,b) \in \mathcal{E}} \frac{(x_a - x_b)^2}{R_{ab}}
\;+\; \sum_{a} \frac{x_a^2}{R_{a0}}
\;\ge\; 0,
\]

donde \(\mathcal{E}\) es el conjunto de ramas resistivas y \(R_{a0}\) las resistencias a tierra. La suma es estrictamente positiva si el circuito está conectado y \(x \neq 0\). En consecuencia:

- \(G\) es invertible y el sistema tiene solución única.
- Todos sus autovalores son reales y positivos.
- Es adecuada para métodos iterativos estacionarios y para gradiente conjugado.

Si hay nodos flotantes, islas sin referencia o fuentes de tensión mal planteadas, \(G\) puede ser singular o indefinida; la Capa 3 debe detectar y reportar esos casos.

### 5.3 Dispersa

Cada nodo físico se conecta solo a unos pocos nodos vecinos. Por ello cada fila de \(G\) tiene a lo sumo \(d_a + 1\) entradas no nulas, donde \(d_a\) es el grado del nodo \(a\). Para circuitos grandes:

\[
\text{nnz}(G) \ll n^2.
\]

Esta dispersidad es la razón principal para preferir métodos iterativos sobre una inversión directa de \(G\).

### 5.4 Dominancia diagonal y estructura de M-matriz

En un circuito resistivo típico:

\[
G_{aa} = \sum_{b \neq a} |G_{ab}| + G_{a0},
\qquad
G_{ab} \le 0 \text{ para } a \neq b.
\]

Es decir, \(G\) es una **M-matriz** débilmente dominante por filas. Si además todos los nodos tienen camino a tierra, la dominancia es estricta al menos en una fila y el radio espectral de la matriz de iteración de Jacobi es menor que 1, lo que garantiza convergencia para circuitos conectados.

## 6. Métodos iterativos asociados

La Capa 4 resuelve \(G V = I\) sin invertir \(G\). Se usa la descomposición

\[
G = D - L - U,
\]

con \(D\) la parte diagonal, \(-L\) la parte estrictamente triangular inferior y \(-U\) la parte estrictamente triangular superior.

- **Jacobi:** actualiza cada componente usando solo la iteración anterior.
- **Gauss-Seidel:** usa los valores ya actualizados dentro de la misma iteración.
- **SOR:** aplica un factor de relajación \(\omega\) a Gauss-Seidel; para \(0 < \omega < 2\) y \(G\) SDP, el método converge.
- **SSOR:** variante simétrica de SOR, útil como precondicionador y para problemas con \(G\) simétrica.

El criterio de parada habitual es el residuo relativo

\[
\frac{\lVert I - G V^{(k)} \rVert}{\lVert I \rVert} < \text{tol},
\]

o bien un número máximo de iteraciones `max_iter`. La solución numérica es una aproximación; la calidad se mide por el residuo, el número de iteraciones y el historial de error.

> La convergencia depende de las propiedades espectrales de \(G\) y del valor de \(\omega\). La Capa 2 valida los parámetros; la Capa 4 documenta y aplica el criterio de parada; la Capa 5 compara y exporta los resultados.

## 7. Flujo completo del sistema

1. **Capa 3:** lee la netlist, identifica nodos y componentes, elige la referencia y construye \(G\) e \(I\) mediante estampado nodal.
2. **Capa 2:** valida parámetros y solicita la resolución del sistema.
3. **Capa 4:** ejecuta Jacobi, Gauss-Seidel, SOR o SSOR sobre \((G, I)\).
4. **Capa 5:** serializa y exporta los resultados; compara métricas entre métodos.
5. **Frontend:** consume únicamente la API de la Capa 2 y presenta los resultados.

## 8. Alcance de este documento

Este documento describe la teoría necesaria para implementar y validar las capas 3, 4 y 5. No incluye código, algoritmos implementados ni decisiones de interfaz. Cualquier optimización (por ejemplo, almacenamiento disperso o precondicionadores) se decidirá en el Sprint correspondiente y deberá respetar las reglas de desacoplamiento del `README.md`.

## 9. Referencias

- R. L. Burden y J. D. Faires, *Análisis Numérico*.
- G. Strang, *Introduction to Linear Algebra*.
- C. A. Desoer y E. S. Kuh, *Basic Circuit Theory*.
- D. M. Young, *Iterative Solution of Large Linear Systems*.
- Y. Saad, *Iterative Methods for Sparse Linear Systems*.
