# Fase E · Implementación y validación

El enunciado pide que la implementación no solo funcione, sino que **coincida con el problema formalizado y con la complejidad argumentada**. Esta sección muestra cómo se cumple: qué se implementó, cómo se organiza el código, cómo se validan las entradas, qué pruebas lo respaldan y cómo se reproducen los resultados.

## 1. Qué se implementó (más de lo mínimo exigido)
| Exigido | Implementado |
|---|---|
| ≥ 1 búsqueda de rutas **o** regla FEFO/reposición | Dijkstra (con bloqueos, predecesores y detección de empates), BFS, FEFO (3 políticas) y reposición |
| ≥ 1 verificador de certificado (caso NP o NPC) | 7 verificadores: n1, n2, n3, n4, c1, c2 y c3 (además de los de p1 y p3) |
| Opcional: exacto vs heurística en un NPC | c2: enumeración y Held–Karp vs vecino más cercano · c3: ramificación vs 2-aproximación |
| — | Reducciones **ejecutables y probadas**: HAM-CYCLE ≤p TSP-DEC e IS ≤p VC |
| — | Los 3 autómatas como AFD en Python, idénticos a los `.jff` de JFLAP (probado) |

## 2. Separación lectura / procesamiento / presentación
El código tiene tres capas, y los datos fluyen en un solo sentido:

1. **Lectura** (`io_datos.py`): lee `data/*.json`, valida los datos y los convierte en estructuras de Python.
2. **Procesamiento** (`automatas/`, `rutas/`, `inventario/`, `casos/`): algoritmos puros, sin lectura de archivos ni impresión.
3. **Presentación** (`presentacion.py`, `presentacion_casos.py`): convierte los resultados en texto y tablas.

- Los módulos de procesamiento **no leen archivos ni imprimen**. `tests/test_registro.py::TestCapas` lo comprueba automáticamente analizando el código.
- Los datos de los 10 expedientes están en `data/casos_simulador.json`, no incrustados en el código (también se prueba).

## 3. Validación de entradas (ejemplos)
| Dato inválido | Reacción |
|---|---|
| Peso negativo, NaN, infinito o no numérico en la planta | `ValueError`: Dijkstra exige pesos ≥ 0 |
| Origen bloqueado, nodo inexistente, zona bloqueada desconocida | `ValueError` |
| Símbolo ∉ Σ en un autómata | `ValueError` (entrada inválida, distinta de un rechazo) |
| Cantidad ≤ 0, política desconocida, lotes con código repetido, fecha mal escrita | `ValueError` |
| SKU repetido, objetivo < mínimo, campos negativos | `ValueError` (los SKU repetidos se detectan al leer) |
| Matriz no cuadrada, no simétrica o con lazos; p no primo; cadena no binaria | `ValueError` |
| Aristas antiparalelas en la red de flujo | `ValueError` con la indicación de agregar un nodo intermedio (CLRS 26.1) |

## 4. Pruebas
- **Funcionales** (normales, límite e inválidas): `tests/test_automatas.py`, `test_jflap.py`, `test_rutas.py`, `test_inventario.py`, `test_casos_p.py`, `test_casos_np.py`, `test_casos_npc.py`, `test_registro.py`. El inventario completo, generado al ejecutar, está en `docs/generado/inventario_pruebas.md`.
- **Comparación contra fuerza bruta** en cientos de instancias aleatorias con semilla fija: Dijkstra vs todos los caminos simples, Held–Karp vs todas las permutaciones, DPLL y 2-SAT vs 2ⁿ asignaciones, ramificación vs subconjuntos, BSGS vs búsqueda lineal, y las dos reducciones vs una prueba directa.
- **Complejidad** (`tests/test_complejidad.py`), en dos niveles:
  1. *Conteo de operaciones* (determinista): cada algoritmo cuenta su operación dominante y se compara con la cota. Por ejemplo: Dijkstra hace ≤ E⃗+1 inserciones en el heap; Edmonds–Karp hace ≤ V·E aumentos y su número **no cambia** al multiplicar todas las capacidades por 10⁶; la enumeración TSP hace exactamente (n−1)! tours; la búsqueda de factores **se duplica con cada bit** extra; los verificadores son lineales o cuadráticos.
  2. *Tiempo real* (`time.perf_counter`, mínimo de mediciones intercaladas, hasta 3 intentos): al cuadruplicar la entrada, BFS y Dijkstra crecen unas 4–5 veces (no 16, que sería cuadrático); la enumeración TSP crece unas 9 veces al pasar de 8 a 9 centros; los factores, unas 4 veces con 2 bits más.

## 5. Coherencia código ⇄ Big-O (decisiones de implementación)
- No se ordena dentro de los bucles de BFS ni de Edmonds–Karp, porque agregaría un factor log a O(V+E) y a O(V·E²). El orden de recorrido es el de la lista (determinista).
- Held–Karp recorre las máscaras en orden creciente con una tabla 2ⁿ × n, lo que da O(n²·2ⁿ) real (no O(n³·2ⁿ)).
- Los verificadores de c2 y c3 no ordenan: marcan "visto" en O(n) y O(V+E).
- La reposición procesa con un generador (O(1) extra); la detección de SKU repetidos está en la capa de lectura.
- Dijkstra recorre los vecinos en orden alfabético para que los empates sean reproducibles: Σ d·log d = O(E log V), dentro de la cota O((V+E) log V).

## 6. Reproducibilidad
- Solo biblioteca estándar de Python ≥ 3.8. Semillas fijas en todas las pruebas aleatorias. Desempates deterministas.
- `python -m unittest discover -s tests -v` (o el notebook de Colab, celda 2) · `python -m logistpulse` · `python scripts/verificar_entrega.py`.
- Las salidas observadas de las fichas y de `docs/generado/salidas_observadas.md` se **generan ejecutando** el código (`scripts/generar_docs.py`). `verificar_entrega.py` avisa si quedaron desactualizadas.
