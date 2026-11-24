# Decisiones de modelado y hallazgos

**Lectura obligatoria antes de redactar cualquier sección.** Así el informe es coherente con el código y las pruebas, y los tres escribimos lo mismo sobre cada tema. Si alguien quiere cambiar una decisión, la cambia en el código, corre las pruebas y avisa al equipo.

---

## 1. Decisiones de modelado

### Fase A · Autómatas
| # | Decisión | Por qué |
|---|---|---|
| A1 | **F = estados terminales legítimos** (el ciclo cerró de forma válida) en los 3 AFD. Pedido: F = {Entregado, Cancelado}. Reserva: F = {Consumida, Liberada, Expirada, Rechazada}. Compra: F = {Recibida, Rechazada}. | Las Figuras 3 y 4 marcan *Rechazada* como final; la Figura 2 no marca *Cancelado*. Usamos un criterio único para los tres. La variante "solo pedidos entregados" está en `PEDIDO_ESTRICTO` (F = {Entregado}), así que se puede cambiar en una línea. |
| A2 | Símbolos de **1 carácter** (ej. `c` = confirmar). | JFLAP *Multiple Run* lee una cadena por línea, carácter a carácter. |
| A3 | δ **parcial**; lo no declarado va a un **sumidero ERROR** (no final y absorbente). | Así δ es total, como pide la definición formal. JFLAP hace lo mismo implícitamente: si no hay transición, rechaza. |
| A4 | Un símbolo ∉ Σ **no es un rechazo**: es una entrada inválida (ValueError). | La cadena no está en Σ*. Separamos "rechazada por el modelo" de "dato mal formado". |
| A5 | Pedido: "liberar/cancelar" en Reservado = **un solo evento `x`** (cancelar libera la reserva). | La Figura 2 lo dibuja como una sola flecha. |
| A6 | Pedido: **no se puede cancelar en Preparación** ni después. | La Figura 2 no tiene esa flecha: una vez iniciado el picking, el pedido sigue. Se prueba con la cadena `crix`, que se rechaza. |
| A7 | Compra: se agrega el bucle **δ(Recepción parcial, p) = Recepción parcial**. | Se pueden recibir varias entregas parciales antes de completar. Es la parte del enunciado que pide "completar eventos". |
| A8 | Los estados finales **no tienen transiciones de salida**. | Un proceso cerrado no se reabre. Así se rechaza "Rechazada → Enviada". |

### Fase B · Planta
| # | Decisión |
|---|---|
| B1 | Grafo **no dirigido** (pasillos de doble sentido), pesos = metros (≥ 0), origen **R**, destino **D**. Datos en `data/planta.json`. |
| B2 | Zona bloqueada = vértice eliminado. **Origen bloqueado = dato inválido** (error). **Destino bloqueado = no hay ruta** (dist = ∞). |
| B3 | Desempate reproducible: el heap compara (distancia, nombre del vértice) y los vecinos se recorren en orden alfabético. |

### Fase C · Inventario
| # | Decisión |
|---|---|
| C1 | Lote elegible ⇔ mismo SKU ∧ disponible > 0 ∧ **vencimiento > fecha de referencia**. Un lote que vence **hoy** ya no se reserva. |
| C2 | Orden FEFO: (vencimiento ↑, código de lote ↑). |
| C3 | Si el stock no alcanza, las **tres** políticas del enunciado están implementadas: `parcial` (reserva lo que hay y reporta el pendiente → PARCIAL), `rechazar` (no reserva nada → RECHAZADO) y `esperar` (no reserva; el pedido queda EN_ESPERA con `requiere_reposicion = True`, que alimenta la regla de reposición). |
| C4 | `en_orden` = solo órdenes de compra **abiertas** (emitidas y no recibidas). Esto evita sugerencias duplicadas (ver H5). |

### Fase E · Código
| # | Decisión |
|---|---|
| E1 | Capas separadas: **lectura** (`io_datos.py`, que lee `data/*.json`, incluidos los 10 expedientes en `data/casos_simulador.json`), **procesamiento** (`automatas/`, `rutas/`, `inventario/`, `casos/`: algoritmos puros, sin E/S) y **presentación** (`presentacion.py`, `presentacion_casos.py`). Lo comprueba `tests/test_registro.py::TestCapas`. |
| E2 | Cada algoritmo acepta un `Contador` opcional que cuenta su operación dominante. `tests/test_complejidad.py` compara esos conteos con la cota Big-O (y además mide tiempos reales con tolerancia). Así el Big-O del informe queda **atado al código**. |
| E3 | Nada se ordena dentro de bucles cuya cota no lo permita (BFS, Edmonds–Karp, verificadores). Held–Karp recorre las máscaras en orden creciente: O(n²·2ⁿ) real. |
| E4 | Las salidas observadas se **generan ejecutando** el código (`scripts/generar_docs.py`), también dentro de cada ficha (bloque `SALIDA`), así que nunca se inventan. |

---

## 2. Hallazgos (úsenlos en el informe y en la exposición: suman puntos)

| # | Hallazgo | Dónde se prueba |
|---|---|---|
| **H1** | **Empate en la planta.** Dijkstra devuelve R→B→A→**E**→D = 11 m. La ruta de la Figura 5, R→B→A→**P**→E→D, también cuesta 11 m. Las dos son óptimas: Dijkstra garantiza el **costo** mínimo, no una ruta única. | `test_ruta_de_la_figura_es_optima_y_empata` |
| H2 | BFS en la planta da R→A→E→D: 3 tramos pero **12 m**. BFS minimiza tramos, no metros. Con pesos hay que usar Dijkstra. | `test_bfs_minimiza_tramos_no_costo` |
| H3 | p2 también empata: Quito→Latacunga→Guayaquil = Quito→Ambato→Guayaquil = 8. | `TestP2` |
| H4 | p3: lo que sale de Planta suma 12, pero el **flujo máximo es 10**. El corte mínimo es {Quito→Clientes, Guayaquil→Clientes}. El correo advierte justamente esto. | `TestP3` |
| H5 | Reposición sin duplicados: con 18 unidades disponibles, 5 reservadas y ninguna orden abierta, la regla sugiere 37. Después de emitir esa orden (en_orden += 37) la posición sube a 50 > 30 y la nueva sugerencia es **0**. Con las 10 unidades en orden del ejemplo del enunciado sugiere 27. | `test_no_duplica_si_ya_hay_orden_abierta` |
| **H6** | **c1: la instancia del simulador es 2-CNF** (x1∨¬x2)∧(x2∨x3), y 2-SAT ∈ **P** (O(n+m)). La ficha del simulador dice "fórmula 3-CNF" y el correo habla de reglas booleanas en general: ese problema general sigue siendo NP-completo. **Que una instancia sea fácil no cambia la clase del problema.** | `test_instancia_simulador_es_2cnf` |
| H7 | c3: el asunto y la ficha del simulador hablan de "k almacenes" y de "zona cubierta por un almacén propio o vecino" (eso es *Dominating Set*). El **cuerpo del correo** pide otra cosa: hasta k **equipos de inspección**, con un equipo en al menos un extremo de **cada corredor** (*Vertex Cover*); el mapa del portal se titula "Corredores entre zonas" y los datos preguntan "¿Cubre toda arista?". Seguimos el cuerpo del correo. Los dos son NP-completos y en esta instancia dan la misma respuesta: S = {B}. | `TestC3` |
| H8 | c2: el correo pide **regresar** al punto de salida, así que es un **ciclo** hamiltoniano (TSP), no un camino. | `TestC2` |
| **H9** | n2 y n3: O(B) **no es polinomial**. B ocupa log₂B bits, así que B = 2^(log B) y la búsqueda es **exponencial en el tamaño de la entrada** (pseudo-polinomial). El verificador sí es polinomial. | — |
| H10 | n2: si B ≥ N, la respuesta es trivialmente Sí (d = N). El caso interesante es B < N. | `test_limites` (n2) |
| H11 | n4: decir "No" exige **agotar** las n! permutaciones (720 con 6 vértices). Para el "No" no hay un certificado corto conocido. | `test_grafo_asimetrico_agota_las_permutaciones` |
| H12 | Heurística vs exacto (c2): el vecino más cercano da 13 y el óptimo (Held–Karp) es 6. La heurística es rápida pero **no garantiza** el óptimo. En c3, la 2-aproximación sí garantiza \|S\| ≤ 2·ÓPT. | `test_heuristica_valida_pero_no_optima`, `test_exactos_y_aproximacion` |
| H13 | Edmonds–Karp hace **el mismo número de aumentos** si se multiplican todas las capacidades por 10⁶. Es la prueba empírica de que O(V·E²) no depende del valor de las capacidades. | `test_edmonds_karp_cota_independiente_de_las_capacidades` |
| H14 | Búsqueda de factores: con N primo y B = N−1, las divisiones se **duplican con cada bit** extra (8 → 16 bits). Es la prueba empírica de H9. | `test_factor_rango_exponencial_en_bits` |

---

## 3. Convenciones de redacción
- **Modelo de cómputo**: máquina de Turing determinista; enteros codificados en **binario**; M(k) es el costo de multiplicar números de k bits (O(k²) con el método escolar).
- **Big-O siempre con variables definidas** (V, E, n, m, k, L, P, B…), en tiempo **y** espacio.
- **Grupo B**: nunca escribir "es NP-completo". Escribir: "pertenece a NP (certificado + verificador polinómico); no se conoce un algoritmo polinómico ni una prueba de NP-completitud".
- **Grupo C**: la reducción va **del problema conocido al nuestro**: CONOCIDO ≤p NUESTRO. Hay que dar la construcción, la correctitud (⇔) y el costo polinómico de la transformación.
- **Decidible ≠ eficiente**. Los 10 casos son decidibles; los grupos B y C pueden ser impracticables en instancias grandes.
- P ⊆ NP y NPC ⊆ NP. **No** son tres conjuntos disjuntos (Figura 1 del enunciado). "NP" **no** significa "no polinómico". No se afirma P ≠ NP.
- Referencias a Sipser con la numeración de la **3.ª edición**: PATH ∈ P (Teo. 7.14); Cook–Levin (§7.4); VERTEX-COVER y HAMPATH NP-completos (§7.5); A_TM indecidible por diagonalización (Teo. 4.11); HALT_TM indecidible por reducción desde A_TM (Teo. 5.1).

---

## 4. Qué seleccionar en el simulador (coincide con nuestro análisis)
| Correo | Clasificación | Algoritmo (desplegable) | ¿Decidible? | Estado del caso |
|---|---|---|---|---|
| 1 · p1 | P | BFS | Decidible | Problema de decisión |
| 2 · p2 | P | Dijkstra | Decidible | Problema de optimización |
| 3 · p3 | P | Edmonds–Karp | Decidible | Problema de optimización |
| 4 · n1 | NP | Búsqueda exhaustiva de permutaciones | Decidible | Problema de decisión |
| 5 · n2 | NP | Prueba por división exhaustiva | Decidible | Problema de decisión |
| 6 · n3 | NP | Búsqueda exhaustiva con exponenciación modular | Decidible | Problema de decisión |
| 7 · n4 | NP | Permutaciones + verificación de adyacencia | Decidible | Problema de decisión |
| 8 · c1 | NP-completo | DPLL / retroceso con poda | Decidible | Problema de decisión |
| 9 · c2 | NP-completo | Backtracking / enumerar permutaciones | Decidible | Problema de decisión |
| 10 · c3 | NP-completo | Backtracking / ramificación | Decidible | Problema de decisión |

En los campos de texto del simulador peguen la computabilidad y la complejidad de la ficha, y el código del módulo `logistpulse/casos/<id>_*.py`. El simulador guarda el avance en **un solo navegador**, así que una sola persona (Jessica) lo llena completo al final con el texto de las tres y descarga el informe .txt.
