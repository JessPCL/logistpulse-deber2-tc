# Supuestos, límites y conclusiones
**Responsable: Jessica**

## Supuestos
Cada supuesto se justifica en `docs/DECISIONES_Y_HALLAZGOS.md` (decisiones A1–A8, B1–B3, C1–C4 y E1–E4); aquí se resumen.
- **Modelo de cómputo:** máquina de Turing determinista, o de forma equivalente el modelo RAM con enteros codificados **en binario**. Por eso el tamaño de un número B es log₂B bits, y un algoritmo O(B) no es polinomial (H9).
- **Autómatas (A1–A8):** F son los estados donde el proceso cerró de forma legítima; *Cancelado* y *Rechazada* cuentan como cierre válido. La variante "solo pedidos entregados" queda en `PEDIDO_ESTRICTO`. La función δ es parcial con un sumidero ERROR, y un símbolo fuera de Σ es un dato inválido, no un rechazo.
- **Planta (B1–B3):** el grafo es no dirigido, los pesos son metros ≥ 0, el origen es R y el destino D. Una zona bloqueada se modela como vértice eliminado. Los empates se resuelven por nombre para que la salida sea reproducible.
- **Inventario (C1–C4):** un lote que vence **hoy** ya no es elegible. FEFO ordena por (vencimiento, código de lote). `en_orden` cuenta solo las órdenes abiertas.
- **Correos:** manda el **cuerpo del correo**, no la tarjeta del simulador (H7 en c3). Los tramos de p1, p2 y p3 tienen sentido, como muestran las flechas del mapa del portal. Los valores de n1 y c2 que la tabla no trae se toman del código de ejemplo del propio caso.

## Límites de la inferencia
- **El código prueba lo que dicen sus datos, no la operación real.** Las 146 pruebas confirman que los algoritmos dan la respuesta correcta sobre estas instancias y sobre instancias aleatorias generadas. No prueban que la planta, los tiempos o las capacidades reales sean los del expediente: si cambian, hay que volver a ejecutar.
- **Una instancia fácil no cambia la clase del problema.** La fórmula de c1 es 2-CNF y se resuelve en tiempo lineal (H6), pero el problema que describe el correo sigue siendo NP-completo.
- **P vs NP sigue abierto.** Clasificar un problema como NP-completo no demuestra que no exista un algoritmo polinómico: dice que, si existiera, entonces P = NP. Para n1–n4 solo afirmamos que están en NP (certificado y verificador polinómico), sin afirmar NP-completitud.
- **Los tiempos medidos dependen de la máquina.** Los números de `docs/generado/crecimiento.md` cambian entre ejecuciones; lo que se mantiene es la **forma** del crecimiento. Por eso el Big-O se respalda además con conteos de operaciones (`tests/test_complejidad.py`), que no dependen de la máquina.
- **Las extrapolaciones son órdenes de magnitud.** Decir "20 centros: unos 4 800 años" multiplica el costo medido por el número de candidatos. Sirve para mostrar que la búsqueda exhaustiva es impracticable, no para predecir un tiempo exacto.

## Conclusiones por fase
- **A · Autómatas:** los tres procesos (pedido, reserva, orden de compra) son lenguajes regulares. Cada AFD responde en un paso por símbolo, y los archivos .jff de JFLAP son idénticos a los autómatas probados en Python, así que las dos herramientas aceptan y rechazan las mismas secuencias.
- **B · Rutas:** Dijkstra da R → B → A → E → D = **11 m**. La ruta de la Figura 5 también cuesta 11 m: hay **empate**, y Dijkstra garantiza el costo mínimo, no una ruta única (H1). BFS minimiza tramos, no metros: da 12 m (H2).
- **C · FEFO y reposición:** las tres políticas (parcial, rechazar, esperar) dan resultados distintos ante falta de stock. La regla del enunciado sugiere **27** unidades y no duplica pedidos cuando ya hay una orden abierta (H5).
- **D · Los 10 correos:**
  - **P:** p1, p2 y p3.
  - **NP, sin afirmar NP-completitud:** n1–n4.
  - **NP-completo:** c1, c2 y c3, cada uno con verificador y reducción ejecutable.
  - En p3 lo que sale de la planta suma 12, pero el flujo máximo es **10** (H4).
  - En n2 y n3, buscar cuesta O(B), que es exponencial en los bits de B, mientras que verificar es polinomial (H9).
- **E · Implementación:** el código está separado en capas (lectura, procesamiento y presentación). Las salidas del informe se generan ejecutándolo, y cada cota Big-O está atada a un conteo de operaciones que una prueba revisa.
- **F · Parada:** "decidible" no es lo mismo que "resoluble en tiempo útil". TSP-DEC con 20 centros es decidible pero tomaría miles de años por búsqueda exhaustiva. En cambio, decidir si un programa arbitrario termina es indecidible: para eso no existe ningún algoritmo, por mucho tiempo que se le dé.

## Checklist
- [x] Supuestos (modelo de cómputo, codificación binaria, criterio de F, planta no dirigida, "vence hoy = no elegible"…) con referencia a `docs/DECISIONES_Y_HALLAZGOS.md`
- [x] Límites de la inferencia: lo que el código prueba (sobre sus datos) y lo que no (la realidad operativa); que P vs NP sigue abierto; que la medición de tiempos depende de la máquina
- [x] Conclusiones por fase (A–F) en 1–2 líneas cada una, incluidos los hallazgos H1, H4, H6 y H9
