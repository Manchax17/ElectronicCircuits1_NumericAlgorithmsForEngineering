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

Supónganse resistencias positivas y conductancias finitas y positivas. Forme el grafo de nodos incógnita con las ramas resistivas como aristas. \(G\) es **simétrica definida positiva** (SDP) si y solo si cada componente conexa tiene al menos un camino resistivo a tierra. En efecto,

\[
x^TGx=\sum_{(a,b)\in\mathcal E}\frac{(x_a-x_b)^2}{R_{ab}}+
\sum_a\frac{x_a^2}{R_{a0}}\ge0.
\]

La energía solo puede anularse si \(x\) es constante en cada componente y cero en cualquier componente que tenga camino a tierra. Si alguna componente carece de camino a tierra, un vector constante no nulo en esa componente da \(x^TGx=0\), por lo que \(G\) es singular. Cuando todas las componentes tienen camino a tierra, la energía es positiva para todo \(x\ne0\); entonces \(G\) es invertible y el sistema tiene solución única, y sus autovalores son reales y positivos.

En este modelo resistivo pasivo, las fuentes independientes modifican el vector derecho, no la definitud de \(G\). Fuentes ideales de tensión requieren otra formulación y quedan fuera de esta matriz conductiva simple. La Capa 3 debe detectar las componentes sin referencia.
### 5.3 Dispersa

Cada nodo físico se conecta solo a unos pocos nodos vecinos. Por ello cada fila de \(G\) tiene a lo sumo \(d_a + 1\) entradas no nulas, donde \(d_a\) es el grado del nodo \(a\). Para circuitos grandes:

\[
\text{nnz}(G) \ll n^2.
\]

Esta dispersidad es la razón principal para preferir métodos iterativos sobre una inversión directa de \(G\).

### 5.4 Dominancia diagonal y estructura de M-matriz

En un circuito resistivo típico:

\[
G_{aa}=\sum_{b\ne a}|G_{ab}|+G_{a0},\qquad
G_{ab}\le0\quad(a\ne b).
\]

Así, \(G\) es una **M-matriz** débilmente dominante por filas. Cada componente conexa de la malla incógnita produce un bloque irreducible; si tiene camino a tierra, al menos una fila del bloque es estrictamente dominante. Bajo estas hipótesis Jacobi y Gauss-Seidel convergen. Para varias componentes, la condición debe cumplirse bloque a bloque. La dominancia débil por sí sola no garantiza convergencia.

### 5.5 Fuente real y equivalente de Norton

Una fuente de tensión ideal \(V_s\) en serie con \(R_s>0\) equivale, vista desde sus terminales, a una fuente de corriente \(I_N=V_s/R_s\) en paralelo con la misma \(R_s\). Si el terminal positivo está en el nodo \(a\) y el otro en tierra, la resistencia añade \(1/R_s\) a \(G_{aa}\), y la fuente añade \(+I_N\) a \(b_a\) si inyecta corriente en \(a\) (el signo cambia con la orientación). Entre nodos \(a,c\), la resistencia añade \(+1/R_s\) a \(G_{aa},G_{cc}\) y \(-1/R_s\) a \(G_{ac},G_{ca}\); para una fuente con terminal positivo en \(a\), la corriente Norton apunta de \(c\) a \(a\) y agrega \(+I_N\) a \(b_a\), \(-I_N\) a \(b_c\).

## 6. Métodos iterativos asociados

La Capa 4 resuelve \(GV=b\), donde \(b\) es el vector de corrientes llamado \(I\) antes. Sea \(d_i=G_{ii}\), \(\mathcal N_i=\texttt{vecinos}[i]\), y cada \((j,g_{ij})\in\mathcal N_i\) el término fuera de diagonal \(G_{ij}\). La fila es

\[
d_iV_i+\sum_{(j,g_{ij})\in\mathcal N_i}g_{ij}V_j=b_i.
\]

Se supone \(d_i\ne0\). Todas las sumas recorren solo vecinos almacenados.

### 6.1 Fórmulas de actualización

**Jacobi** (usa solo la iteración anterior):

\[
V_i^{(k+1)}=\frac{b_i-\sum_{(j,g_{ij})\in\mathcal N_i}g_{ij}V_j^{(k)}}{d_i}.
\]

**Gauss-Seidel** en recorrido creciente (valores nuevos para \(j<i\), anteriores para \(j>i\)):

\[
V_i^{(k+1)}=\frac{b_i-\sum_{\substack{(j,g_{ij})\in\mathcal N_i\\j<i}}g_{ij}V_j^{(k+1)}-\sum_{\substack{(j,g_{ij})\in\mathcal N_i\\j>i}}g_{ij}V_j^{(k)}}{d_i}.
\]

**SOR**:

\[
V_i^{(k+1)}=(1-\omega)V_i^{(k)}+\frac{\omega}{d_i}\left(b_i-\sum_{\substack{(j,g_{ij})\in\mathcal N_i\\j<i}}g_{ij}V_j^{(k+1)}-\sum_{\substack{(j,g_{ij})\in\mathcal N_i\\j>i}}g_{ij}V_j^{(k)}\right).
\]

**SSOR** aplica una barrida hacia adelante y otra hacia atrás, ambas con \(\omega\). Para \(i=0,\ldots,n-1\):

\[
Y_i=(1-\omega)V_i^{(k)}+\frac{\omega}{d_i}\left(b_i-\sum_{\substack{j<i\\(j,g_{ij})\in\mathcal N_i}}g_{ij}Y_j-\sum_{\substack{j>i\\(j,g_{ij})\in\mathcal N_i}}g_{ij}V_j^{(k)}\right),
\]

y luego, para \(i=n-1,\ldots,0\):

\[
V_i^{(k+1)}=(1-\omega)Y_i+\frac{\omega}{d_i}\left(b_i-\sum_{\substack{j<i\\(j,g_{ij})\in\mathcal N_i}}g_{ij}Y_j-\sum_{\substack{j>i\\(j,g_{ij})\in\mathcal N_i}}g_{ij}V_j^{(k+1)}\right).
\]

Jacobi y Gauss-Seidel reciben \(\omega\) por la firma común, pero no la usan.

Con la representación diagonal más vecinos, cada iteración recorre las entradas no nulas de la matriz; su costo es \(O(\mathrm{nnz})\). SSOR realiza dos barridos, que mantienen ese mismo orden asintótico por iteración.

### 6.2 Criterio de parada

Tras cada iteración:

\[
r_i=b_i-d_iV_i-\sum_{(j,g_{ij})\in\mathcal N_i}g_{ij}V_j,\qquad
\frac{\lVert b-GV\rVert_\infty}{\lVert b\rVert_\infty}
=\frac{\max_i|r_i|}{\max_i|b_i|}<\text{tolerancia}.
\]

También se detiene al llegar a max_iteraciones; si el criterio no se cumplió, no se declara convergencia. Si \(b=0\), el cociente no está definido: la convención para ese caso (por ejemplo, residuo absoluto) queda [POR CONFIRMAR].

### 6.3 Hipótesis de convergencia

Para la iteración estacionaria \(V^{(k+1)}=TV^{(k)}+c\), la condición necesaria y suficiente para converger desde todo vector inicial es \(\rho(T)<1\).

- **Jacobi:** suficiente que \(G\) sea estrictamente dominante por filas en todas sus filas. También basta que sea irreducible, débilmente dominante por filas y estricta en al menos una fila. Si es reducible, este segundo resultado se aplica a cada bloque irreducible y cada bloque debe satisfacer ambas propiedades. SDP por sí sola no es una garantía suficiente para Jacobi.
- **Gauss-Seidel:** las mismas condiciones de dominancia son suficientes; además, cualquier matriz SDP da convergencia.
- **SOR (teorema de Ostrowski-Reich):** si \(G\) es simétrica definida positiva, converge si y solo si \(0<\omega<2\). El intervalo de \(\omega\) sin la hipótesis SDP no da esa garantía.
- **SSOR:** para la iteración estándar de dos barridas definida arriba y \(G\) SDP, converge si y solo si \(0<\omega<2\).

Las afirmaciones presuponen diagonal no nula. Resistencias positivas y un camino a tierra por componente dan SDP; cada bloque conectado es además irreducible, débilmente dominante y estricto en al menos una fila, por lo que las garantías de Jacobi y Gauss-Seidel también aplican.

> La convergencia depende de las propiedades espectrales de \(G\) y del valor de \(\omega\). La Capa 2 valida los parámetros; la Capa 4 documenta y aplica el criterio de parada; la Capa 5 compara y exporta los resultados.

## 7. Ejemplo: malla 3×3

La malla tiene nodos del netlist 1 a 9 (índices 0 a 8), resistencias de \(1\,\Omega\) entre vecinos horizontales y verticales, fugas de \(10\,\Omega\) a tierra en todos los nodos e inyección de \(1\,A\) en el nodo 5 (índice 4). El fixture backend/tests/fixtures/malla_3x3.json contiene la netlist y la matriz dispersa. La diagonal es \([2.1,3.1,2.1,3.1,4.1,3.1,2.1,3.1,2.1]\), los acoplamientos entre vecinos son \(-1\,S\), y \(b=[0,0,0,0,1,0,0,0,0]^T\,A\).

La solución generada con numpy.linalg.solve, en voltios, es

\[
V\approx[1.05764146,\ 1.11052353,\ 1.05764146,\ 1.11052353,\ 1.32734003,\ 1.11052353,\ 1.05764146,\ 1.11052353,\ 1.05764146]^T.
\]

## 8. Tensión de paso y de toque

Según la decisión A2, cada nodo de la malla representa un punto del terreno y cada componente \(V_i\) es el potencial del terreno en ese punto. La **tensión de paso** entre nodos vecinos \(i\) y \(j\) es

\[
E_{\mathrm{paso}}=|V_i-V_j|,
\]

donde la separación entre puntos de la malla queda [POR CONFIRMAR]. La **tensión de toque** es la diferencia entre el potencial del nodo que representa la estructura y el potencial del terreno en el punto \(i\):

\[
E_{\mathrm{toque}}=|V_{\mathrm{estructura}}-V_i|,
\]

con la identificación del nodo de estructura y el punto \(i\) de evaluación [POR CONFIRMAR]. No se fijan límites normativos de IEEE Std 80.

## 9. Flujo completo del sistema

1. **Capa 3:** lee la netlist, identifica nodos y componentes, elige la referencia y construye \(G\) e \(I\) mediante estampado nodal.
2. **Capa 2:** valida parámetros y solicita la resolución del sistema.
3. **Capa 4:** recibe la matriz dispersa \((n,\text{diagonal},\text{vecinos},b)\) y ejecuta Jacobi, Gauss-Seidel, SOR o SSOR.
4. **Capa 5:** serializa y exporta los resultados; compara métricas entre métodos.
5. **Frontend:** consume únicamente la API de la Capa 2 y presenta los resultados.

## 10. Alcance de este documento

Este documento describe la teoría necesaria para implementar y validar las capas 3, 4 y 5. No incluye código, algoritmos implementados ni decisiones de interfaz. El formato interno de almacenamiento es disperso (diagonal más vecinos); cualquier otra optimización, como los precondicionadores, se decidirá en el Sprint correspondiente y deberá respetar las reglas de desacoplamiento del `README.md`.

## 11. Referencias

- R. L. Burden y J. D. Faires, *Análisis Numérico*.
- G. Strang, *Introduction to Linear Algebra*.
- C. A. Desoer y E. S. Kuh, *Basic Circuit Theory*.
- D. M. Young, *Iterative Solution of Large Linear Systems*.
- Y. Saad, *Iterative Methods for Sparse Linear Systems*.
- J. Demmel, *Applied Numerical Linear Algebra*, cap. 6.5.5, [material del autor](https://www.stat.uchicago.edu/~lekheng/courses/302/demmel/demmch6.pdf).
- N. Hu, *Linear stationary iterative methods*, [notas de UCLA](https://www.math.ucla.edu/~njhu/notes/nla/lin-iter/lsiter/).

## 12. Supuestos para validar con el docente

1. Para \(b=0\), ¿se usará residuo absoluto y qué valor de tolerancia se define?
2. ¿Qué modelo, distancias y ubicaciones se usarán para obtener potenciales de superficie en los cálculos de paso y toque? Los valores normativos quedan [POR CONFIRMAR].
3. ¿Se admitirán equivalentes Norton entre dos nodos además de nodo-tierra, y qué convención de orientación/signo tendrá la netlist?
