# Sprint 1
**Fechas:** martes 17 al sábado 21 de noviembre de 2026 · **Objetivo:** Modelar pedidos, reservas y compras con autómatas; definir el grafo de la planta y los casos de ruta.
**Evidencia de revisión que pide el enunciado:** Diagramas de estados y grafo con entradas, eventos y supuestos.
**Ajuste de plazo:** la entrega real es el martes 24/11, así que los tres sprints se comprimieron: Sprint 1 (17–21/11), Sprint 2 (22/11) y Sprint 3 (23–24/11).

## Roles de este sprint (rotativos)
| Coordinación y backlog | Formalización | Algoritmos y análisis | Implementación y validación |
|---|---|---|---|
| Jessica | Camila | Luis | Luis |

## Planificación
| Tarea (ID del backlog) | Responsable | Rama / PR | Revisor | Estado |
|---|---|---|---|---|
| F-G0 · Repositorio público, Codespaces (`.devcontainer`), GitHub Actions, protección de `main`, Issues del backlog | Jessica | `main` (configuración inicial) | — | Hecho (20/11) |
| F-G0 · Limpieza de documentos y scripts (sin emojis) + corrección del paso 6 de la guía | Jessica | `jessica/fase-df-gestion` · PR #20 | Luis | Hecho (20/11) |
| C-c2 · Ficha c2 (TSP de decisión), adelantada para la exposición | Jessica | `jessica/fase-df-gestion` · PR #21 | Luis | Hecho (20/11) |
| F-B1, F-B2 · Grafo de la planta, escenarios de ruta y redacción de la Fase B | Luis | `luis/fase-bc-fichas-p` · PR #24 | Camila | Hecho (21/11) |
| F-A1, F-A2, F-A3 · Autómatas de pedido, reserva y orden de compra: redacción + capturas JFLAP | Camila | `camila/fase-a-fichas-np` | Jessica | No se terminó en este sprint: pasa al Sprint 2 (#30, 22/11) |
| C-c1, C-c3 · Fichas c1 (SAT) y c3 (Vertex Cover), adelantadas | Jessica | `jessica/fase-df-gestion` · PR #25 | Luis | En revisión al cierre: se fusionó en el Sprint 2 |

## Revisión (demo del sprint) · sábado 21/11
- Qué se mostró: el repositorio con `main` protegido (PR + 1 aprobación + pruebas en Python 3.10 y 3.12) y las pruebas en verde en GitHub Actions; la ruta R → B → A → E → D de 11 m con el empate de la Figura 5 (Fase B, #24); la ficha c2 con el recorrido de 15 km ≤ 20.
- Comentarios del revisor: Luis aprobó #20 y #21 con las pruebas en verde; Camila revisó y fusionó la Fase B (#24).
- Estado de `python scripts/verificar_entrega.py` al cierre: "Grafo y búsqueda de rutas" e "Implementación y pruebas" en OK; pendientes la Fase A con capturas JFLAP, siete fichas y la gestión.

## Retrospectiva
| Qué salió bien | Qué salió mal | Qué mejoramos el próximo sprint |
|---|---|---|
| El código y las pruebas estuvieron listos desde el inicio, y cada cambio entró por PR con revisión y pruebas automáticas. | Hubo que rehacer documentos e Issues por emojis y corregir los nombres de los checks del ruleset. La Fase A no se terminó dentro del sprint. En c1 y c3 se usó la tarjeta del simulador en lugar del cuerpo del correo. | Leer el cuerpo completo de cada correo antes de redactar (`docs/QUE_PIDE_CADA_CORREO.md`), confirmar la fecha real de entrega y abrir los PR más temprano. |
