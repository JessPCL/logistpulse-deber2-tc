# Backlog del producto · lo mantiene quien tenga el rol de Coordinación en cada sprint

El enunciado pide que **cada correo sea una unidad de trabajo vinculada a su ficha, su código y sus pruebas** (sección 5). Por eso hay una fila por correo, además de las historias por fase. Sugerencia: crear un *Issue* de GitHub por fila y cerrarlo desde el PR.

> Los tres sprints se comprimieron al plazo real de entrega (martes 24/11): Sprint 1 = 17–21/11, Sprint 2 = 22/11, Sprint 3 = 23–24/11. La columna Sprint indica en cuál se terminó cada tarea.

## Historias por fase
| ID | Historia | Fase | Responsable | Sprint | Estimación | Estado | Evidencia (PR / archivo) |
|---|---|---|---|---|---|---|---|
| F-G0 | Configuración del repositorio: público, Codespaces, GitHub Actions, protección de `main`, Issues, limpieza sin emojis | — | Jessica | 1 | 2 | Hecho | `.devcontainer/`, `.github/workflows/pruebas.yml`, `equipo/GUIA_CODESPACES.md` |
| F-A1 | AFD de pedido + JFLAP | A | Camila | 2 | 3 | Hecho (22/11, #30) | `jflap/pedido.jff`, `docs/fase_A_automatas.md` |
| F-A2 | AFD de reserva + JFLAP | A | Camila | 2 | 2 | Hecho (22/11, #30) | `jflap/reserva.jff` |
| F-A3 | AFD de orden de compra + JFLAP | A | Camila | 2 | 2 | Hecho (22/11, #30) | `jflap/orden_compra.jff` |
| F-B1 | Grafo de la planta y escenarios de ruta | B | Luis | 1 | 2 | Hecho (21/11, #24) | `data/planta.json`, `docs/diagramas/planta_ruta.png` |
| F-B2 | Pseudocódigo + Big-O de Dijkstra/BFS + traza | B | Luis | 1 | 3 | Hecho (21/11, #24) | `docs/fase_B_rutas.md` |
| F-C1 | Pseudocódigo + Big-O de FEFO y reposición | C | Luis | 2 | 3 | Hecho (22/11, #26) | `docs/fase_C_fefo_reposicion.md` |
| F-E1 | Revisión cruzada de código y pruebas (PR) | E | Rol de validación | 2 | 2 | Hecho (22/11, revisiones cruzadas #20–#32) | `tests/`, `scripts/verificar_entrega.py` |
| F-F1 | Nota sobre el problema de la parada | F | Jessica | 2 | 2 | Hecho (22/11, #27) | `docs/fase_F_nota_parada.md` |
| F-G1 | Informe PDF + release v1.0 + presentación | — | Jessica (integra) | 3 | 3 | Hecho (22/11): informe PDF y release `v1.0`; exposición: ensayo el 23/11 | `docs/generado/INFORME.md`; PDF adjunto al release `v1.0` |

## Una unidad de trabajo por correo
| ID | Correo | Clase | Responsable | Sprint | Ficha | Código | Pruebas | Estado |
|---|---|---|---|---|---|---|---|---|
| C-p1 | ¿Puede llegar el envío a la zona Norte? | P | Luis | 1 | `docs/fichas/p1.md` (modelo) | `casos/p1_alcanzabilidad.py` | `test_casos_p.py::TestP1` | Hecho (20/11, ficha modelo; programa con lista de conexiones en #27) |
| C-p2 | Ruta mínima entre centros | P | Luis | 2 | `docs/fichas/p2.md` | `casos/p2_ruta_minima.py` | `test_casos_p.py::TestP2` | Hecho (22/11, #29) |
| C-p3 | Máximo de camiones | P | Luis | 2 | `docs/fichas/p3.md` | `casos/p3_flujo_maximo.py` | `test_casos_p.py::TestP3` | Hecho (22/11, #29) |
| C-n1 | Isomorfismo de redes | NP | Camila | 2 | `docs/fichas/n1.md` | `casos/n1_isomorfismo.py` | `test_casos_np.py::TestN1` | Hecho (22/11, #32) |
| C-n2 | Factor en un intervalo | NP | Camila | 2 | `docs/fichas/n2.md` | `casos/n2_factor_rango.py` | `test_casos_np.py::TestN2` | Hecho (22/11, #32) |
| C-n3 | Logaritmo discreto acotado | NP | Camila | 2 | `docs/fichas/n3.md` | `casos/n3_log_discreto.py` | `test_casos_np.py::TestN3` | Hecho (22/11, #32) |
| C-n4 | Simetría de la topología | NP | Camila | 2 | `docs/fichas/n4.md` | `casos/n4_automorfismo.py` | `test_casos_np.py::TestN4` | Hecho (22/11, #32) |
| C-c1 | Asignación que cumpla las reglas (SAT) | NPC | Jessica | 2 | `docs/fichas/c1.md` | `casos/c1_sat.py` | `test_casos_npc.py::TestC1` | Hecho (22/11, #25) |
| C-c2 | Recorrido dentro del presupuesto (TSP) | NPC | Jessica | 1 | `docs/fichas/c2.md` | `casos/c2_tsp_decision.py` | `test_casos_npc.py::TestC2` | Hecho (20/11, #21) |
| C-c3 | Cobertura con k equipos (Vertex Cover) | NPC | Jessica | 2 | `docs/fichas/c3.md` | `casos/c3_vertex_cover.py` | `test_casos_npc.py::TestC3` | Hecho (22/11, #25) |
