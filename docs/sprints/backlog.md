# Backlog del producto · lo mantiene quien tenga el rol de Coordinación en cada sprint

El enunciado pide que **cada correo sea una unidad de trabajo vinculada a su ficha, su código y sus pruebas** (sección 5). Por eso hay una fila por correo, además de las historias por fase. Sugerencia: crear un *Issue* de GitHub por fila y cerrarlo desde el PR.

## Historias por fase
| ID | Historia | Fase | Responsable | Sprint | Estimación | Estado | Evidencia (PR / archivo) |
|---|---|---|---|---|---|---|---|
| F-G0 | Configuración del repositorio: público, Codespaces, GitHub Actions, protección de `main`, Issues, limpieza sin emojis | — | Jessica | 1 | 2 | Hecho | `.devcontainer/`, `.github/workflows/pruebas.yml`, `equipo/GUIA_CODESPACES.md` |
| F-A1 | AFD de pedido + JFLAP | A | Camila | 1 | 3 | En curso | `jflap/pedido.jff`, `docs/fase_A_automatas.md` |
| F-A2 | AFD de reserva + JFLAP | A | Camila | 1 | 2 | En curso | `jflap/reserva.jff` |
| F-A3 | AFD de orden de compra + JFLAP | A | Camila | 1 | 2 | En curso | `jflap/orden_compra.jff` |
| F-B1 | Grafo de la planta y escenarios de ruta | B | Luis | 1 | 2 | En curso | `data/planta.json`, `docs/diagramas/planta_ruta.png` |
| F-B2 | Pseudocódigo + Big-O de Dijkstra/BFS + traza | B | Luis | 2 | 3 | Por hacer | `docs/fase_B_rutas.md` |
| F-C1 | Pseudocódigo + Big-O de FEFO y reposición | C | Luis | 2 | 3 | Por hacer | `docs/fase_C_fefo_reposicion.md` |
| F-E1 | Revisión cruzada de código y pruebas (PR) | E | Rol de validación | 2 | 2 | Por hacer | `tests/`, `scripts/verificar_entrega.py` |
| F-F1 | Nota sobre el problema de la parada | F | Jessica | 3 | 2 | Por hacer | `docs/fase_F_nota_parada.md` |
| F-G1 | Informe PDF + release v1.0 + presentación | — | Jessica (integra) | 3 | 3 | Por hacer | `docs/generado/INFORME.md`, tag `v1.0` |

## Una unidad de trabajo por correo
| ID | Correo | Clase | Responsable | Sprint | Ficha | Código | Pruebas | Estado |
|---|---|---|---|---|---|---|---|---|
| C-p1 | ¿Puede llegar el envío a la zona Norte? | P | Luis | 3 | `docs/fichas/p1.md` (modelo) | `casos/p1_alcanzabilidad.py` | `test_casos_p.py::TestP1` | Ficha modelo lista |
| C-p2 | Ruta mínima entre centros | P | Luis | 3 | `docs/fichas/p2.md` | `casos/p2_ruta_minima.py` | `test_casos_p.py::TestP2` | Por hacer |
| C-p3 | Máximo de camiones | P | Luis | 3 | `docs/fichas/p3.md` | `casos/p3_flujo_maximo.py` | `test_casos_p.py::TestP3` | Por hacer |
| C-n1 | Isomorfismo de redes | NP | Camila | 3 | `docs/fichas/n1.md` | `casos/n1_isomorfismo.py` | `test_casos_np.py::TestN1` | Por hacer |
| C-n2 | Factor en un intervalo | NP | Camila | 3 | `docs/fichas/n2.md` | `casos/n2_factor_rango.py` | `test_casos_np.py::TestN2` | Por hacer |
| C-n3 | Logaritmo discreto acotado | NP | Camila | 3 | `docs/fichas/n3.md` | `casos/n3_log_discreto.py` | `test_casos_np.py::TestN3` | Por hacer |
| C-n4 | Simetría de la topología | NP | Camila | 3 | `docs/fichas/n4.md` | `casos/n4_automorfismo.py` | `test_casos_np.py::TestN4` | Por hacer |
| C-c1 | Asignación que cumpla las reglas (SAT) | NPC | Jessica | 1 (adelantada) | `docs/fichas/c1.md` | `casos/c1_sat.py` | `test_casos_npc.py::TestC1` | En revisión |
| C-c2 | Recorrido dentro del presupuesto (TSP) | NPC | Jessica | 1 (adelantada) | `docs/fichas/c2.md` | `casos/c2_tsp_decision.py` | `test_casos_npc.py::TestC2` | Hecho(20/11) |
| C-c3 | Cobertura con k almacenes (Vertex Cover) | NPC | Jessica | 1 (adelantada) | `docs/fichas/c3.md` | `casos/c3_vertex_cover.py` | `test_casos_npc.py::TestC3` | En revisión |
