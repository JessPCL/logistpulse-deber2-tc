# Roles, reparto y prompts · Deber 2 LOGISTPULSE

## Reparto (equilibrado por puntos de la rúbrica)

| | **Camila** | **Luis** | **Jessica** |
|---|---|---|---|
| Rol | Formalización | Algoritmos y análisis | Coordinación e integración |
| Fases | **A** · autómatas + JFLAP (2,0) | **B** · rutas (1,5) + **C** · FEFO/reposición (1,5) | **F** · nota sobre la parada + gestión/sprints/release (1,0) + informe |
| Fichas | n1, n2, n3, n4 (grupo B · NP) | p2, p3 (grupo A · P); p1 ya está hecha como **ficha modelo** (solo la revisa) | c1, c2, c3 (grupo C · NPC) |
| Archivos que edita | `docs/fase_A_automatas.md`, `jflap/capturas/`, `docs/fichas/n*.md` | `docs/fase_B_rutas.md`, `docs/fase_C_fefo_reposicion.md`, `docs/fichas/p*.md` | `docs/fase_F_nota_parada.md`, `docs/conclusiones.md`, `docs/fichas/c*.md`, `docs/sprints/`, `README.md`, informe PDF |
| Rama | `camila/fase-a-fichas-np` | `luis/fase-bc-fichas-p` | `jessica/fase-df-gestion` |
| Revisa los PR de | Luis | Jessica | Camila |
| Expone (≈3 min) | Autómatas + demo JFLAP | Ruta de la planta + FEFO/reposición | Caso de complejidad (c2) + parada + intro/cierre |

**Implementación y pruebas (1,5)**: el código ya está hecho y probado (más de 140 pruebas, entre ellas las de complejidad). Cada uno **lee, ejecuta y entiende** los módulos de su parte, porque en la exposición se los pueden preguntar, y revisa por PR el trabajo del compañero.

## Roles rotativos (sección 5 del enunciado)
El enunciado sugiere 4 roles **rotativos**. Separamos dos cosas: el **dueño del contenido** (fijo, tabla de arriba) y el **rol de proceso** de cada sprint, que rota para que los 3 hagan los 4 roles al menos una vez (cada fila es una permutación).

| Rol de proceso | Sprint 1 | Sprint 2 | Sprint 3 |
|---|---|---|---|
| Coordinación y backlog (prioriza, dependencias, evidencias del sprint) | Jessica | Camila | Luis |
| Formalización (revisa entradas, restricciones, pregunta de decisión y certificado de TODO lo del sprint) | Camila | Luis | Jessica |
| Algoritmos y análisis (revisa algoritmo y complejidad) | Luis | Jessica | Camila |
| Implementación y validación (corre `verificar_entrega.py`, mantiene código y pruebas, comparte resultados) | Luis | Jessica | Camila |

Esto queda registrado en cada `docs/sprints/sprint_N.md` (tabla "Roles de este sprint").

## Calendario sugerido (ajústenlo a la fecha real de entrega)
| Sprint | Fechas | Meta | Quién cierra qué |
|---|---|---|---|
| 1 | 17–23 nov | Repo creado; autómatas probados en JFLAP; grafo definido | Jessica sube el repo base. Camila: capturas JFLAP + borrador de la Fase A. Luis: borrador de la Fase B |
| 2 | 24–30 nov | Pseudocódigo + Big-O revisados por pares | Luis: Fases B y C. Camila: Fase A final. Jessica: backlog + sprint 1–2 |
| 3 | 1–7 dic | 10 fichas, nota de la parada, informe PDF, release v1.0, ensayo | Cada uno sus fichas. Jessica integra, llena el simulador y crea el tag v1.0 |

## Antes de usar el prompt (los tres)
1. Jessica crea el **repo público** y sube el **zip v3.3** siguiendo `equipo/GUIA_CODESPACES.md`; cada uno abre su Codespace. A la IA le adjuntan el zip v3.3 (o el enlace del repo público), el enunciado (.docx) y el simulador (.html).
2. Abran su IA (ChatGPT, Gemini, Claude…), **adjunten los 3 archivos** y peguen **su** prompt tal cual. Si su IA no acepta zip, adjunten los archivos que el prompt pide leer.
3. La IA primero propone un plan; respondan "ok". Cuando pida una salida de código, córranla en la terminal de su Codespace (o en Colab) y péguenle el resultado. El flujo de Git está en `equipo/GUIA_CODESPACES.md`.
4. Antes de cada commit, corran `python scripts/verificar_entrega.py` en la terminal del Codespace (o la celda 11 de Colab): dice qué falta, criterio por criterio de la rúbrica.

---

## Prompt de CAMILA

```
CONTEXTO: soy parte de un equipo de 3 (Camila, Luis, Jessica) de Teoría de la Computación (USFQ). Hacemos el Deber 2 "LOGISTPULSE: decisiones, algoritmos y límites computacionales". Adjunto: (1) el enunciado del deber (.docx), (2) el simulador con los 10 correos (.html) y (3) el repositorio del equipo (logistpulse-deber2-tc.zip). Lee los tres antes de responder. Del zip lee primero README.md, docs/DECISIONES_Y_HALLAZGOS.md, docs/MATRIZ_TRAZABILIDAD.md, docs/PLANTILLA_FICHA.md, docs/fichas/p1.md (FICHA MODELO terminada: imita su formato, profundidad y estructura) y los dos ejemplos de docs/referencias/, y además: logistpulse/automatas/*.py, docs/generado/tablas_transiciones.md, jflap/esperado_*.md, jflap/COMO_PROBAR_EN_JFLAP.md, docs/fichas/n1–n4.md, logistpulse/casos/n1_*.py–n4_*.py y tests/test_casos_np.py.

REGLAS GENERALES:
1. Escribe todo en español académico, claro y conciso. Entrega cada archivo en Markdown, en un bloque separado con su ruta como título.
2. No cambies las condiciones ni los datos de los correos, ni las decisiones de docs/DECISIONES_Y_HALLAZGOS.md. Si algo es ambiguo o el enunciado se contradice, avísame y propón una lectura; no adivines en silencio.
3. Clasifica según la evidencia que exige cada grupo:
   - P: algoritmo polinómico conocido.
   - NP: certificado + verificador polinómico, aclarando que eso NO prueba que el problema esté fuera de P ni que sea NP-completo.
   - NP-completo: pertenencia a NP + problema NP-completo de origen + reducción polinómica en la dirección CONOCIDO ≤p NUESTRO (construcción, correctitud ⇔ y tiempo de la transformación) + consecuencia práctica.
   Recuerda: P ⊆ NP; "NP" no significa "no polinómico"; no afirmes que P ≠ NP. Cita a Sipser con la numeración de la 3.ª edición (está en docs/DECISIONES_Y_HALLAZGOS.md §3).
4. Cada ficha sigue docs/PLANTILLA_FICHA.md, en este orden: 0) respuesta al correo para el remitente; 1) resumen sin cambiar condiciones; 2) entrada/salida/restricciones y si es decisión u optimización (si es optimización, se clasifica su versión de decisión asociada y debe quedar escrito); 3) clasificación y evidencia; 4) decidibilidad y computabilidad con el modelo de cómputo nombrado; 5) algoritmo, justificación, terminación y si es exacto/aproximado/heurístico; 6) Big-O temporal y espacial con variables definidas (distingue el VALOR de un número de su TAMAÑO en bits); 7) código, pruebas y salida observada; 8) observaciones; tabla "¿Qué concluimos?"; 3 preguntas de defensa oral.
5. El código YA existe en logistpulse/ y pasa más de 140 pruebas (unittest, Python 3.8+, solo biblioteca estándar, con lectura/procesamiento/presentación separadas). NO lo reescribas: explícalo y cita archivos, funciones y pruebas. Si propones un cambio, dámelo aparte, con su prueba. NO edites los bloques entre <!-- SALIDA:INICIO --> y <!-- SALIDA:FIN -->: los genera scripts/generar_docs.py al ejecutar el código.
6. La "salida observada" y los tiempos deben ser REALES: usa los bloques SALIDA de las fichas, docs/generado/salidas_observadas.md y docs/generado/crecimiento.md, o pídeme que corra un comando en mi Codespace (o en Colab) y te pegue el resultado. Para respaldar cada Big-O cita la prueba correspondiente de tests/test_complejidad.py, que cuenta operaciones y mide tiempos. Nunca inventes salidas ni tiempos.
7. Trabaja por partes: primero dame un plan breve y tus supuestos y espera mi "ok"; luego entrega en el orden indicado. Termina cada entregable con la lista de verificación de docs/PLANTILLA_FICHA.md marcada.
8. Explícame el razonamiento para que pueda defenderlo oralmente (exposición de 8–10 min, cada uno habla ~3 min). Al final de cada entregable incluye 3 preguntas probables del profesor con su respuesta en 2–3 frases.
9. No uses emojis en ningún documento (tampoco en títulos ni en la lista de verificación: escribe "Lista de verificación" sin símbolos).


MI PARTE (rol de contenido: Formalización; los roles de proceso rotan por sprint según equipo/ROLES_Y_PROMPTS.md):
A) FASE A (Sprints 1–2; es el criterio que más pesa, 2,0 pts) → docs/fase_A_automatas.md. Para pedido, reserva y orden de compra:
   a. M = (Q, Σ, δ, q0, F) y el significado operativo de cada estado y evento.
   b. Tabla de transiciones completa + estado sumidero ERROR (por qué δ queda total).
   c. Justificación de F con el criterio único "cierre legítimo" (decisión A1), incluido por qué Cancelado es final aunque la Figura 2 no lo marque, y de los eventos completados (A5–A8).
   d. Al menos 2 secuencias válidas y 2 inválidas por autómata (incluidas las 4 del enunciado): cadena, eventos, resultado y la transición exacta que acepta o rechaza.
   e. Cómo se probaron: JFLAP (determinismo, Multiple Run, Step by State) + tests/test_automatas.py y tests/test_jflap.py (el .jff es idéntico al AFD probado), citando las capturas de jflap/capturas/. Ejecutar una cadena cuesta O(n): lo respalda test_afd_un_paso_por_simbolo.
   f. Por qué el modelo evita transiciones imposibles (ej.: consumir una reserva no confirmada).
   g. Un checklist paso a paso para que YO pruebe los 3 .jff en JFLAP 7.1 y saque las capturas con los nombres de jflap/capturas/LEEME.md.
B) Fichas del grupo B (NP con certificado): n1 (isomorfismo), n2 (factor en rango), n3 (logaritmo discreto acotado) y n4 (automorfismo no trivial). Completa SOLO las secciones marcadas con [POR REDACTAR] (borra la marca al completarlas) de docs/fichas/n*.md. Usa el formato BUSCAR vs VERIFICAR del ejemplo docs/referencias/ejemplo_n2_buscar_vs_verificar.md. En n2 y n3 los números vienen en BINARIO: explica por qué O(B) no es polinomial (H9) con la evidencia de test_factor_rango_exponencial_en_bits (H14). En n4 explica cómo se concluye "No" agotando las n! permutaciones (H11). NUNCA digas que son NP-completos.

ORDEN: Fase A (a→g) → n1 → n2 → n3 → n4 → mi guion de 3 min (autómatas + demo de Multiple Run) con 3 diapositivas.
Al terminar, dame una lista corta de lo que debo verificar yo antes de hacer commit en mi rama camila/fase-a-fichas-np (incluye correr `python scripts/verificar_entrega.py`).
```

---

## Prompt de LUIS

```
CONTEXTO: soy parte de un equipo de 3 (Camila, Luis, Jessica) de Teoría de la Computación (USFQ). Hacemos el Deber 2 "LOGISTPULSE: decisiones, algoritmos y límites computacionales". Adjunto: (1) el enunciado del deber (.docx), (2) el simulador con los 10 correos (.html) y (3) el repositorio del equipo (logistpulse-deber2-tc.zip). Lee los tres antes de responder. Del zip lee primero README.md, docs/DECISIONES_Y_HALLAZGOS.md, docs/MATRIZ_TRAZABILIDAD.md, docs/PLANTILLA_FICHA.md, docs/fichas/p1.md (FICHA MODELO terminada: imita su formato, profundidad y estructura) y los dos ejemplos de docs/referencias/, y además: logistpulse/rutas/*.py, logistpulse/inventario/*.py, data/*.json, docs/diagramas/planta_ruta.png, docs/generado/salidas_observadas.md, tests/test_rutas.py, tests/test_inventario.py, tests/test_complejidad.py, docs/fichas/p1–p3.md y logistpulse/casos/p1_*.py–p3_*.py.

REGLAS GENERALES:
1. Escribe todo en español académico, claro y conciso. Entrega cada archivo en Markdown, en un bloque separado con su ruta como título.
2. No cambies las condiciones ni los datos de los correos, ni las decisiones de docs/DECISIONES_Y_HALLAZGOS.md. Si algo es ambiguo o el enunciado se contradice, avísame y propón una lectura; no adivines en silencio.
3. Clasifica según la evidencia que exige cada grupo:
   - P: algoritmo polinómico conocido.
   - NP: certificado + verificador polinómico, aclarando que eso NO prueba que el problema esté fuera de P ni que sea NP-completo.
   - NP-completo: pertenencia a NP + problema NP-completo de origen + reducción polinómica en la dirección CONOCIDO ≤p NUESTRO (construcción, correctitud ⇔ y tiempo de la transformación) + consecuencia práctica.
   Recuerda: P ⊆ NP; "NP" no significa "no polinómico"; no afirmes que P ≠ NP. Cita a Sipser con la numeración de la 3.ª edición (está en docs/DECISIONES_Y_HALLAZGOS.md §3).
4. Cada ficha sigue docs/PLANTILLA_FICHA.md, en este orden: 0) respuesta al correo para el remitente; 1) resumen sin cambiar condiciones; 2) entrada/salida/restricciones y si es decisión u optimización (si es optimización, se clasifica su versión de decisión asociada y debe quedar escrito); 3) clasificación y evidencia; 4) decidibilidad y computabilidad con el modelo de cómputo nombrado; 5) algoritmo, justificación, terminación y si es exacto/aproximado/heurístico; 6) Big-O temporal y espacial con variables definidas (distingue el VALOR de un número de su TAMAÑO en bits); 7) código, pruebas y salida observada; 8) observaciones; tabla "¿Qué concluimos?"; 3 preguntas de defensa oral.
5. El código YA existe en logistpulse/ y pasa más de 140 pruebas (unittest, Python 3.8+, solo biblioteca estándar, con lectura/procesamiento/presentación separadas). NO lo reescribas: explícalo y cita archivos, funciones y pruebas. Si propones un cambio, dámelo aparte, con su prueba. NO edites los bloques entre <!-- SALIDA:INICIO --> y <!-- SALIDA:FIN -->: los genera scripts/generar_docs.py al ejecutar el código.
6. La "salida observada" y los tiempos deben ser REALES: usa los bloques SALIDA de las fichas, docs/generado/salidas_observadas.md y docs/generado/crecimiento.md, o pídeme que corra un comando en mi Codespace (o en Colab) y te pegue el resultado. Para respaldar cada Big-O cita la prueba correspondiente de tests/test_complejidad.py, que cuenta operaciones y mide tiempos. Nunca inventes salidas ni tiempos.
7. Trabaja por partes: primero dame un plan breve y tus supuestos y espera mi "ok"; luego entrega en el orden indicado. Termina cada entregable con la lista de verificación de docs/PLANTILLA_FICHA.md marcada.
8. Explícame el razonamiento para que pueda defenderlo oralmente (exposición de 8–10 min, cada uno habla ~3 min). Al final de cada entregable incluye 3 preguntas probables del profesor con su respuesta en 2–3 frases.
9. No uses emojis en ningún documento (tampoco en títulos ni en la lista de verificación: escribe "Lista de verificación" sin símbolos).


MI PARTE (rol de contenido: Algoritmos y análisis; los roles de proceso rotan por sprint según equipo/ROLES_Y_PROMPTS.md):
A) FASE B (Sprints 1–2) → docs/fase_B_rutas.md. Planta como grafo ponderado: zonas como vértices, pasillos como aristas con pesos ≥ 0 (tabla V, E, pesos); por qué es NO dirigido; zonas bloqueadas y escenarios; origen R y destino D del AMR. Pseudocódigo de Dijkstra con precondiciones, predecesores para reconstruir la ruta, terminación (cada vértice se finaliza una vez; inserciones acotadas en el heap) y Big-O O((V+E) log V) de tiempo y O(V+E) de espacio, respaldado por test_dijkstra_operaciones_de_heap_acotadas y test_dijkstra_crece_casi_lineal; pseudocódigo de BFS con O(V+E) (test_bfs_es_O_V_mas_E). Tabla paso a paso de Dijkstra en la planta (de docs/generado/salidas_observadas.md). Ruta R→B→A→E→D = 11 m y EMPATE con la Figura 5 (H1); comparación con BFS (H2); resultados con bloqueos. Explica las pruebas de tests/test_rutas.py (normales, grafo sin ruta, pesos negativos rechazados, origen = destino, nodo inexistente).
B) FASE C (Sprint 2) → docs/fase_C_fefo_reposicion.md: pseudocódigo FEFO y de reposición coherentes con el código; lote elegible (vence hoy = no elegible), desempate por código, las TRES políticas si no alcanza el stock (parcial / rechazar / esperar → EN_ESPERA); terminación y Big-O (FEFO O(L log L) tiempo y O(L) espacio; reposición O(P) tiempo y O(1) extra), respaldados por test_fefo_O_L_log_L_y_reposicion_O_P; anti-duplicado con órdenes abiertas (H5) y el ejemplo del enunciado (posición 23 → 27); tabla de pruebas normales, límite e inválidas (tests/test_inventario.py).
C) Fichas del grupo A (P): revisa p1 (ya terminada como modelo; es tuya, ajústala si algo no te convence) y completa las secciones marcadas con [POR REDACTAR] de p2 (borra la marca al completarlas) (Dijkstra; qué debe conservar el sistema para reconstruir la ruta (pred); empate de 8; por qué falla con pesos negativos usando el contraejemplo del código y la alternativa Bellman–Ford) y p3 (Edmonds–Karp: terminación con la cota O(V·E²), que NO depende del valor de las capacidades, con la evidencia de test_edmonds_karp_cota_independiente_de_las_capacidades (H13); el registro de tramos usado/disponible que pide el correo; flujo máximo = 10 y corte mínimo como certificado de optimalidad; por qué no son 12 (H4)). p2 y p3 son de optimización: la clasificación en P se hace sobre su versión de decisión asociada (costo ≤ K, flujo ≥ K) y debe quedar escrito.

ORDEN: Grafo de la planta → Dijkstra (pseudocódigo + explicación del código y sus pruebas) → Fase C → p2 → p3 → mi guion de 3 min (ruta de la planta + FEFO/reposición) con 3 diapositivas.
Al terminar, dame una lista corta de lo que debo verificar yo antes de hacer commit en mi rama luis/fase-bc-fichas-p (incluye correr `python scripts/verificar_entrega.py`).
```

---

## Prompt de JESSICA

```
CONTEXTO: soy parte de un equipo de 3 (Camila, Luis, Jessica) de Teoría de la Computación (USFQ). Hacemos el Deber 2 "LOGISTPULSE: decisiones, algoritmos y límites computacionales". Adjunto: (1) el enunciado del deber (.docx), (2) el simulador con los 10 correos (.html) y (3) el repositorio del equipo (logistpulse-deber2-tc.zip). Lee los tres antes de responder. Del zip lee primero README.md, docs/DECISIONES_Y_HALLAZGOS.md, docs/MATRIZ_TRAZABILIDAD.md, docs/PLANTILLA_FICHA.md, docs/fichas/p1.md (FICHA MODELO terminada: imita su formato, profundidad y estructura) y los dos ejemplos de docs/referencias/, y además: equipo/ROLES_Y_PROMPTS.md, docs/fichas/c1–c3.md, logistpulse/casos/c1_*.py–c3_*.py, tests/test_casos_npc.py, tests/test_complejidad.py, docs/generado/tabla_resumen.md, docs/generado/crecimiento.md, docs/sprints/*, docs/conclusiones.md y docs/presentacion_guion.md.

REGLAS GENERALES:
1. Escribe todo en español académico, claro y conciso. Entrega cada archivo en Markdown, en un bloque separado con su ruta como título.
2. No cambies las condiciones ni los datos de los correos, ni las decisiones de docs/DECISIONES_Y_HALLAZGOS.md. Si algo es ambiguo o el enunciado se contradice, avísame y propón una lectura; no adivines en silencio.
3. Clasifica según la evidencia que exige cada grupo:
   - P: algoritmo polinómico conocido.
   - NP: certificado + verificador polinómico, aclarando que eso NO prueba que el problema esté fuera de P ni que sea NP-completo.
   - NP-completo: pertenencia a NP + problema NP-completo de origen + reducción polinómica en la dirección CONOCIDO ≤p NUESTRO (construcción, correctitud ⇔ y tiempo de la transformación) + consecuencia práctica.
   Recuerda: P ⊆ NP; "NP" no significa "no polinómico"; no afirmes que P ≠ NP. Cita a Sipser con la numeración de la 3.ª edición (está en docs/DECISIONES_Y_HALLAZGOS.md §3).
4. Cada ficha sigue docs/PLANTILLA_FICHA.md, en este orden: 0) respuesta al correo para el remitente; 1) resumen sin cambiar condiciones; 2) entrada/salida/restricciones y si es decisión u optimización (si es optimización, se clasifica su versión de decisión asociada y debe quedar escrito); 3) clasificación y evidencia; 4) decidibilidad y computabilidad con el modelo de cómputo nombrado; 5) algoritmo, justificación, terminación y si es exacto/aproximado/heurístico; 6) Big-O temporal y espacial con variables definidas (distingue el VALOR de un número de su TAMAÑO en bits); 7) código, pruebas y salida observada; 8) observaciones; tabla "¿Qué concluimos?"; 3 preguntas de defensa oral.
5. El código YA existe en logistpulse/ y pasa más de 140 pruebas (unittest, Python 3.8+, solo biblioteca estándar, con lectura/procesamiento/presentación separadas). NO lo reescribas: explícalo y cita archivos, funciones y pruebas. Si propones un cambio, dámelo aparte, con su prueba. NO edites los bloques entre <!-- SALIDA:INICIO --> y <!-- SALIDA:FIN -->: los genera scripts/generar_docs.py al ejecutar el código.
6. La "salida observada" y los tiempos deben ser REALES: usa los bloques SALIDA de las fichas, docs/generado/salidas_observadas.md y docs/generado/crecimiento.md, o pídeme que corra un comando en mi Codespace (o en Colab) y te pegue el resultado. Para respaldar cada Big-O cita la prueba correspondiente de tests/test_complejidad.py, que cuenta operaciones y mide tiempos. Nunca inventes salidas ni tiempos.
7. Trabaja por partes: primero dame un plan breve y tus supuestos y espera mi "ok"; luego entrega en el orden indicado. Termina cada entregable con la lista de verificación de docs/PLANTILLA_FICHA.md marcada.
8. Explícame el razonamiento para que pueda defenderlo oralmente (exposición de 8–10 min, cada uno habla ~3 min). Al final de cada entregable incluye 3 preguntas probables del profesor con su respuesta en 2–3 frases.
9. No uses emojis en ningún documento (tampoco en títulos ni en la lista de verificación: escribe "Lista de verificación" sin símbolos).


MI PARTE (rol de contenido: Coordinación e integración; los roles de proceso rotan por sprint según equipo/ROLES_Y_PROMPTS.md):
A) Fichas del grupo C (NP-completo): completa SOLO las secciones marcadas con [POR REDACTAR] (borra la marca al completarlas) de docs/fichas/c1.md (SAT de despacho; reducción identidad desde 3-SAT + Cook–Levin; hallazgo H6: la instancia del simulador es 2-CNF, que está en P), c2.md (TSP de decisión; reducción desde Ciclo Hamiltoniano con pesos 1/2 y L = n; verificador O(n); versión de decisión vs optimización con Held–Karp; búsqueda exacta vs vecino más cercano: 13 vs 6, y qué garantiza cada una; H8 ciclo vs camino) y c3.md (Vertex Cover; reducción desde INDEPENDENT-SET con k' = |V| − k; ramificación O(2^k·(V+E)) vs 2-aproximación; H7 Vertex Cover vs Dominating Set). Para la consecuencia práctica usa los tiempos REALES de docs/generado/crecimiento.md y las pruebas test_enumeracion_tsp_es_factorial, test_held_karp_es_n2_por_2n, test_vertex_cover_ramificacion_2_a_la_k y test_sat_fuerza_bruta_2n_y_dpll_acotado.
B) FASE F → docs/fase_F_nota_parada.md (máximo 1 página, unas 600 palabras): decidibilidad vs computabilidad (función/relación + modelo) vs complejidad vs "resoluble en tiempo útil"; caso límite: TSP-DEC con 20–25 centros es decidible pero impracticable (cita la tabla de crecimiento medida); contraste con "¿este programa arbitrario termina para toda entrada?": A_TM es indecidible por diagonalización (Sipser Teo. 4.11) y HALT_TM por reducción desde A_TM (Teo. 5.1); "termina para TODA entrada" es aún más difícil; qué hacemos en cambio: probar la terminación de NUESTROS algoritmos con cotas o variantes (Fases B y C) y comprobarlas con conteos (tests/test_complejidad.py).
C) docs/conclusiones.md: supuestos (con referencia a DECISIONES), límites de la inferencia (el código es correcto respecto de sus datos; P vs NP sigue abierto; los tiempos dependen de la máquina) y conclusiones por fase.
D) GESTIÓN (1,0 pt): completa docs/sprints/backlog.md (ya trae una unidad de trabajo por correo) y sprint_1–3.md (objetivo, tareas, responsable, PR, revisor, roles rotativos ya asignados, retrospectiva) con fechas reales, dejando marcado lo que se llena cuando ocurra; plan Git (parte de equipo/GUIA_CODESPACES.md, que ya trae los comandos: adáptalo a nuestras fechas y súmalo al informe de gestión); cómo usar scripts/armar_informe.py → INFORME.docx → PDF; la declaración de uso de IA del README; el guion completo de la presentación de 8–10 min (docs/presentacion_guion.md), que debe cubrir estados y transiciones, una ruta de la planta, FEFO/reposición y un caso de complejidad.

ORDEN: c2 (la que voy a exponer) → c1 → c3 → nota de la parada → conclusiones → sprints y plan Git → informe y declaración de IA → guion completo.
Al terminar, dame una lista corta de lo que debo verificar yo antes de hacer commit en mi rama jessica/fase-df-gestion (incluye correr `python scripts/verificar_entrega.py`).
```
