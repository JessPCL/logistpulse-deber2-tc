# Matriz de trazabilidad: cada requisito → dónde se cumple → cómo se comprueba

Fuentes: **E** = enunciado del Deber 2 (.docx, por sección) · **S** = simulador (instrucciones generales y los 10 correos) · **R** = rúbrica · **Ej** = ejemplos de referencia (`docs/referencias/`).
Estado: **Hecho** = hecho y comprobado (prueba o script) · **Pendiente** = lo completa la persona indicada (lo detecta `scripts/verificar_entrega.py`).

## 1. Requisitos generales (E §1–§2)
| # | Requisito | Dónde | Cómo se comprueba | Estado |
|---|---|---|---|---|
| G1 | Cada modelo define estados, eventos, transiciones válidas e inválidas, entradas, salidas, terminación y evidencia de prueba (E §1) | `automatas/definiciones.py`, `rutas/`, `inventario/`, docstrings con terminación | `test_automatas.py`, `test_rutas.py`, `test_inventario.py` | Hecho: código · Pendiente: redacción en fases A–C |
| G2 | P ⊆ NP, NPC ⊆ NP; clasificar por nivel de evidencia (A/B/C); no suponer P ≠ NP (E §2) | `DECISIONES_Y_HALLAZGOS.md` §3, `casos/__init__.py` | `test_registro.py` (3/4/3, clase ⇔ grupo, B sin reducción, C con ≤p); `verificar_entrega.py` busca "es NP-completo" en fichas n* | Hecho |

## 2. Fase A · Autómatas (E §3)
| # | Requisito | Dónde | Cómo se comprueba | Estado |
|---|---|---|---|---|
| A1 | Q, Σ, q₀, F, δ de pedido, reserva y orden de compra | `definiciones.py`; `docs/generado/tablas_transiciones.md` | `AFD._validar` (q₀ ∈ Q, F ⊆ Q, δ ⊆ Q×Σ×Q) + `test_definiciones_mal_formadas` | Hecho |
| A2 | Probar secuencias en JFLAP | `jflap/*.jff`, `entradas_*.txt`, `esperado_*.md`, `COMO_PROBAR_EN_JFLAP.md` | `test_jflap.py` (el .jff es idéntico al AFD probado) | Hecho: archivos · Pendiente: capturas (Camila) |
| A3 | Si hay diagrama, adjuntar tabla de transiciones y cómo se probaron las secuencias | `docs/diagramas/afd_*.png` + `tablas_transiciones.md` | `generar_diagramas.py`, `generar_docs.py` | Hecho: · Pendiente: texto en `fase_A_automatas.md` |
| A4 | Pruebas mínimas: pedido válido completo; Borrador→Despachado inválida; reserva válida; Rechazada→Enviada inválida | `SECUENCIAS` marcadas [ENUNCIADO] | `test_pruebas_minimas_del_enunciado` | Hecho |
| A5 | ≥ 2 válidas y ≥ 2 inválidas por autómata, con la transición que acepta o rechaza | `SECUENCIAS` (9 por autómata); `ResultadoAFD.motivo` indica el paso y δ | `test_minimo_dos_validas_y_dos_invalidas_por_automata`, `test_traza_identifica_la_transicion_que_rechaza` | Hecho |
| A6 | Justificar estados finales | Decisión A1 (criterio único) + variante `PEDIDO_ESTRICTO` | `test_variante_estricta_del_pedido`, `test_estados_finales_no_tienen_salidas` | Hecho: · Pendiente: redacción (Camila) |
| A7 | Evitar transiciones imposibles (consumir una reserva no confirmada) | δ parcial + sumidero ERROR | `test_no_se_consume_reserva_sin_confirmar` | Hecho |
| A8 | Completar eventos | Bucle en Recepción parcial; cancelar = liberar en Reservado | `test_varias_recepciones_parciales` | Hecho |

## 3. Fase B · Planta y rutas (E §3)
| # | Requisito | Dónde | Cómo se comprueba | Estado |
|---|---|---|---|---|
| B1 | Zonas = V, pasillos = E con pesos ≥ 0 | `data/planta.json`, `GrafoPonderado` | `test_pesos_invalidos` (negativo, NaN, ∞, texto) | Hecho |
| B2 | Declarar si es dirigido, zonas bloqueadas, origen y destino del AMR | `planta.json` (`dirigido`, `escenarios`, `origen`, `destino`) | `test_tamano_y_tipo`, `test_bloqueos` | Hecho |
| B3 | Dijkstra con predecesores para reconstruir la ruta; O((V+E) log V) | `rutas/dijkstra.py` | `test_ruta_base_costo_11`; **`test_dijkstra_operaciones_de_heap_acotadas`** y `test_dijkstra_crece_casi_lineal` | Hecho |
| B4 | Si no hay pesos, BFS (menor número de aristas) en O(V+E) | `rutas/bfs.py` | `test_bfs_minimiza_tramos_no_costo`; **`test_bfs_es_O_V_mas_E`**, `test_bfs_crece_lineal` | Hecho |
| B5 | Ruta encontrada (Figura 5: 11 m) | `planta_ruta.png` | `test_ruta_de_la_figura_es_optima_y_empata` (hallazgo H1) | Hecho: · Pendiente: redacción (Luis) |
| B6 | Pseudocódigo de búsqueda de ruta con terminación y Big-O | docstrings de `dijkstra.py` y `bfs.py` | revisión por PR | Pendiente: `fase_B_rutas.md` (Luis) |

## 4. Fase C · FEFO y reposición (E §3)
| # | Requisito | Dónde | Cómo se comprueba | Estado |
|---|---|---|---|---|
| C1 | Excluir lotes vencidos o sin cantidad | `fefo.py` (vence hoy = no elegible) | `test_excluye_vencidos_que_vencen_hoy_y_sin_stock` | Hecho |
| C2 | Desempate reproducible si vencen el mismo día | orden (vencimiento, código) | `test_pedido_normal_y_desempate_por_codigo`, `test_orden_independiente_del_orden_de_entrada` | Hecho |
| C3 | Política si no se cubre la demanda: rechazar, reservar parcial o esperar reposición | `POLITICAS = (parcial, rechazar, esperar)` | `test_stock_insuficiente_las_tres_politicas` | Hecho |
| C4 | FEFO O(L log L) tiempo, O(L) espacio | `fefo.py` | **`test_fefo_O_L_log_L_y_reposicion_O_P`** (comparaciones ≤ L⌈log₂L⌉+L) | Hecho |
| C5 | Reposición: posición = disponible + en_orden − reservado; si ≤ mínimo, max(0, objetivo − posición) | `reposicion.py` | `test_ejemplo_del_enunciado` (23 → 27), `test_limite_posicion_igual_al_minimo` | Hecho |
| C6 | Explicar cómo se evita duplicar sugerencias con una orden abierta | `en_orden` suma en la posición | `test_no_duplica_si_ya_hay_orden_abierta`, `test_orden_abierta_parcial_solo_sugiere_la_diferencia` | Hecho: · Pendiente: redacción (Luis) |
| C7 | O(P) tiempo; O(1) extra uno a uno; O(P) si se guardan | generador `sugerencias`; SKU repetidos se validan al leer | `test_fefo_O_L_log_L_y_reposicion_O_P` (sku = P) | Hecho |
| C8 | Pseudocódigo FEFO y reposición con terminación y Big-O | docstrings | revisión por PR | Pendiente: `fase_C_fefo_reposicion.md` (Luis) |

## 5. Fase D · Diez correos (E §3 + S)
| # | Requisito | Dónde | Cómo se comprueba | Estado |
|---|---|---|---|---|
| D1 | Distribución 3 P · 4 NP · 3 NPC, sostenida con evidencia | `casos/__init__.py` | `test_distribucion_3_4_3` | Hecho |
| D2 | Grupo A: definición, algoritmo polinómico, pseudocódigo/código, tiempo y espacio | p1–p3 | `test_casos_p.py` + `test_complejidad.py` | Hecho: código · Pendiente: p2, p3 (Luis) |
| D3 | Grupo B: decisión, certificado, verificador polinómico, "no prueba ∉P ni NPC" | n1–n4 (`verificar` separado de `resolver`) | `test_casos_np.py`; `test_verificadores_polinomicos` | Hecho: código · Pendiente: fichas (Camila) |
| D4 | Grupo C: decisión, verificador, NPC de origen, reducción polinómica, consecuencia práctica | c1–c3; `reducir_ham_a_tsp`, `reducir_is_a_vc` | `test_reduccion_ham_a_tsp`, `test_reduccion_is_a_vc`; `crecimiento.md` | Hecho: código · Pendiente: fichas (Jessica) |
| D5 | Ficha: resumen sin cambiar condiciones | sección 1 | lista de verificación | Pendiente |
| D6 | Ficha: entrada, salida, restricciones; decisión u optimización | sección 2 (p2/p3 clasificadas por su versión de decisión) | `test_optimizacion_declara_version_de_decision` | Hecho: datos · Pendiente: texto |
| D7 | Ficha: clasificación y evidencia | sección 3 | `test_registro.py` | Hecho: datos · Pendiente: texto |
| D8 | Ficha: decidibilidad y computabilidad con modelo explícito | sección 4 | lista de verificación | Pendiente |
| D9 | Ficha: algoritmo y si es exacto, aproximado o heurístico | sección 5; columna "Estrategia" | `tabla_resumen.md` | Hecho: datos · Pendiente: texto |
| D10 | Ficha: Big-O de tiempo y espacio con variables definidas | sección 6 | `test_complejidad.py` (cotas por conteo) | Hecho |
| D11 | Ficha: código ejecutable, casos de prueba y **salida observada** | sección 7, bloque SALIDA generado al ejecutar | `verificar_entrega.py` comprueba que el bloque coincida con la ejecución actual | Hecho |
| D12 | Tabla resumen: tipo, decidibilidad, algoritmo, complejidad, estrategia | `docs/generado/tabla_resumen.md` | generada desde el registro | Hecho |
| D13 | Responder el requerimiento operativo de cada correo (S: "Contesta el requerimiento…") | sección 0 de la ficha + primera línea "RESPUESTA AL CORREO" de cada salida | `test_modulos_existen_y_demos_corren` | Hecho: datos · Pendiente: texto |
| D14 | Analizar el problema general, no solo los datos del expediente; distinguir certificado de solución (S) | secciones 2–3; `resolver` ≠ `verificar` | H6 (instancia 2-CNF ∈ P vs problema general NPC) | Hecho |
| D15 | Selecciones del simulador (clase, algoritmo, decidible, decisión/optimización) | `DECISIONES_Y_HALLAZGOS.md` §4 | coincide con el registro | Hecho: · Pendiente: llenarlo (Jessica) |

### Lo que pide cada correo
| Correo | Pedido explícito del remitente | Dónde se cumple |
|---|---|---|
| p1 | Sí/No; procedimiento para toda la red; programa con **lista de conexiones**; ejemplo con ruta y sin ruta | `red_desde_conexiones`; escenario de cierre; tabla BFS por niveles |
| p2 | Recorrido y costo; **qué conservar para reconstruir la ruta** (predecesores); código + prueba; justificar otra técnica | `pred[v]`; empate; Bellman–Ford con pesos negativos |
| p3 | Máximo de camiones; **registro reproducible de tramos usados/disponibles**; crecimiento; no confundir salida con flujo | `registro` con usado/disponible/cancelar; corte mínimo; H4 |
| n1 | ¿Misma estructura?; correspondencia como evidencia; programa del caso; escalamiento | π + `verificar`; O(n!·n²) |
| n2 | Rutina que encuentra y **otra separada** que valida; comparar costos con números en **binario** | `resolver` / `verificar`; H9, H14 |
| n3 | Separar búsqueda del verificador; prueba reproducible; costo de cada etapa | lineal, BSGS y `potencia_modular` contada |
| n4 | Simetría ≠ identidad como certificado + verificador; si no hay, **cómo concluye que agotó** | grafo asimétrico: 720 = 6! permutaciones |
| c1 | Horario candidato; comprobación independiente; búsqueda; crecimiento con nº de decisiones | `verificar`; 2ⁿ; DPLL; 2-SAT (H6) |
| c2 | Recorrido ≤ L con regreso; costo; verificación ejecutable; **decisión vs optimización**; crecimiento | `decidir` / `held_karp`; heurística (H12); `crecimiento.md` |
| c3 | Selección ≤ k como certificado; **verificador separado**; búsqueda; esfuerzo al crecer | `ramificacion` O(2^k·(V+E)); 2-aproximación |

## 6. Fase E · Implementación (E §3)
| # | Requisito | Dónde | Cómo se comprueba | Estado |
|---|---|---|---|---|
| E1 | ≥ 1 búsqueda de rutas o regla FEFO/reposición | Dijkstra, BFS, FEFO, reposición | `test_rutas.py`, `test_inventario.py` | Hecho |
| E2 | Verificador de certificado (NP o NPC) | 7 verificadores | `test_casos_np.py`, `test_casos_npc.py` | Hecho |
| E3 | (Opcional) exacto vs heurística en un NPC, y qué garantiza cada uno | c2 (vecino más cercano), c3 (2-aproximación) | `test_heuristica_valida_pero_no_optima`, `test_exactos_y_aproximacion` | Hecho |
| E4 | Validar entradas | todas las capas | pruebas `*invalid*` (34 métodos, ver inventario) | Hecho |
| E5 | Separar lectura / procesamiento / presentación | `io_datos` / módulos puros / `presentacion*` | `TestCapas` (análisis del código) | Hecho |
| E6 | Comentarios que explican decisiones algorítmicas | docstrings y comentarios | revisión por PR | Hecho |
| E7 | Pruebas reproducibles (normales, límite, inválidas) | semillas fijas, desempates deterministas; mismo entorno para todos con `.devcontainer/devcontainer.json` (Codespaces); servidor limpio en cada push y PR con `.github/workflows/pruebas.yml` | `docs/generado/inventario_pruebas.md`; check de GitHub Actions | Hecho |
| E8 | **Debe coincidir con el problema formalizado y con la complejidad argumentada** | `conteo.py` + `test_complejidad.py` | 16 pruebas de conteo + 4 de tiempo real | Hecho |

## 7. Fase F · Decidibilidad y límites (E §3)
| # | Requisito | Dónde | Estado |
|---|---|---|---|
| F1 | Nota de 1 página: decidibilidad, computabilidad, complejidad, práctica | `docs/fase_F_nota_parada.md` | Pendiente: Jessica |
| F2 | Caso límite: decidible pero impracticable (con números reales) | `docs/generado/crecimiento.md` (medido) | Hecho: datos · Pendiente: texto |
| F3 | Contraste con la parada (no hay decisor general) | nota F | Pendiente: Jessica |

## 8. Gestión, entrega y rúbrica (E §5–§7)
| # | Requisito | Dónde | Cómo se comprueba | Estado |
|---|---|---|---|---|
| M1 | 3 sprints semanales con backlog, responsables, revisión y retrospectiva | `docs/sprints/` | `verificar_entrega.py` | Pendiente: coordinación |
| M2 | **Roles rotativos** | tabla en `ROLES_Y_PROMPTS.md` y en cada sprint | `verificar_entrega.py` | Hecho: plan · Pendiente: cumplirlo |
| M3 | Cada correo = unidad de trabajo vinculada a ficha, código y pruebas | `backlog.md` (C-p1 … C-c3) | `verificar_entrega.py` | Hecho |
| M4 | Historial, ramas/commits identificables, versión etiquetada | Git + tag `v1.0`; flujo con ramas, PR y `gh` en `equipo/GUIA_CODESPACES.md`; `main` protegida (PR + 1 aprobación + Actions en verde); Issues con `scripts/crear_issues.py` | `verificar_entrega.py` (commits, 3 autores, tag) | Pendiente |
| M5 | README, instrucciones de ejecución y contribuciones identificadas | `README.md`; "Responsable" en cada documento | — | Hecho: · Pendiente: declaración de IA |
| M6 | Subir enlace al repo + informe PDF; adjuntar JFLAP, diagramas, código y datos | repo **público** (el profesor abre el enlace sin invitación); `armar_informe.py` → PDF | `verificar_entrega.py` | Pendiente: Jessica |
| M7 | La exposición explica estados y transiciones, una ruta, FEFO/reposición y un caso de complejidad | `presentacion_guion.md` | — | Pendiente: todos |
| M8 | Comunicación: explicitar supuestos, límites y conclusiones (R) | `docs/conclusiones.md` + DECISIONES | `verificar_entrega.py` | Pendiente: Jessica |

## 9. Formato de los ejemplos de referencia (Ej)
| Elemento | Dónde |
|---|---|
| Solicitud operativa destacada | encabezado de cada ficha |
| Grafo dibujado | Mermaid en las fichas p1, p2, p3 y c3 + PNG en el informe |
| BFS por niveles (cola FIFO, padres) | p1 sección 5 (tabla generada al ejecutar) |
| BUSCAR vs VERIFICAR, Big-O con M(L) y bits | n2 (`resolver` / `verificar`, conteo de divisiones) |
| Tabla Decidibilidad · Computabilidad · Complejidad | sección "¿Qué concluimos?" de cada ficha |
