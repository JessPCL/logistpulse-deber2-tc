# Sprint 2
**Fechas:** domingo 22 de noviembre de 2026 · **Objetivo:** Desarrollar Dijkstra, el pseudocódigo FEFO y la regla de reposición; analizar terminación y Big-O. Por el ajuste de plazo, este sprint también cerró la Fase A pendiente y las diez fichas.
**Evidencia de revisión que pide el enunciado:** Pruebas, pseudocódigo y complejidades revisados por pares.

## Roles de este sprint (rotativos)
| Coordinación y backlog | Formalización | Algoritmos y análisis | Implementación y validación |
|---|---|---|---|
| Camila | Luis | Jessica | Jessica |

## Planificación
| Tarea (ID del backlog) | Responsable | Rama / PR | Revisor | Estado |
|---|---|---|---|---|
| C-c1, C-c3 · Fichas c1 (SAT) y c3 (Vertex Cover) | Jessica | `jessica/fase-df-gestion` · PR #25 | Luis | Hecho (22/11) |
| F-C1 · Fase C: pseudocódigo de FEFO y reposición, terminación y Big-O | Luis | `luis/fase-bc-fichas-p` · PR #26 | Camila | Hecho (22/11) |
| F-F1 · Nota de la parada + correcciones según el cuerpo de los correos (p1, c1, c3) | Jessica | `jessica/fase-df-gestion` · PR #27 | Luis | Hecho (22/11) |
| Conclusiones y declaración de uso de IA | Jessica | `jessica/fase-df-gestion` · PR #28 | Luis | Hecho (22/11) |
| C-p2, C-p3 · Fichas p2 (Dijkstra) y p3 (Edmonds–Karp) | Luis | `luis/fase-bc-fichas-p` · PR #29 | Camila | Hecho (22/11) |
| F-A1, F-A2, F-A3 · Fase A + 12 capturas JFLAP (viene del Sprint 1) | Camila | `camila/fase-a-fichas-np` · PR #30 | Jessica | Hecho (22/11) |
| Guion de Luis para la exposición | Luis | `luis/fase-bc-fichas-p` · PR #31 | Camila | Hecho (22/11) |
| C-n1, C-n2, C-n3, C-n4 · Fichas del grupo NP | Camila | `camila/fase-a-fichas-np` · PR #32 | Jessica | Hecho (22/11) |
| F-E1 · Revisión cruzada de código y pruebas | Todos | PR #24 a #32 | — | Hecho: Luis revisa a Jessica, Camila a Luis y Jessica a Camila |

## Revisión (demo del sprint) · domingo 22/11
- Qué se mostró: el *Multiple Run* de los tres autómatas en JFLAP (las 26 cadenas dan el mismo resultado que el código); FEFO con el pedido de 80 unidades y la reposición de 27 unidades; las diez fichas completas.
- Comentarios del revisor: en #30, Jessica comprobó que las tablas de transiciones coinciden con `definiciones.py` y pidió volver a tomar `pedido_determinismo.png` con la franja de *Nondeterminism*. En #32 comprobó, con una fusión de prueba (146 pruebas OK), que n1–n4 cubren lo que pide cada correo y no afirman NP-completitud.
- Estado de `python scripts/verificar_entrega.py` al cierre: 5 de 7 criterios en OK; pendientes la gestión (sprints, release, capturas) y la comunicación (informe PDF, guion).

## Retrospectiva
| Qué salió bien | Qué salió mal | Qué mejoramos el próximo sprint |
|---|---|---|
| Las revisiones fueron cruzadas y con evidencia objetiva: comparación con el código y fusión de prueba antes de aprobar. | Dos fichas entraron con un emoji que el verificador detectó después del merge, y algunas ramas estaban desactualizadas respecto de `main`. | Correr `python scripts/verificar_entrega.py` antes de abrir cada PR y traer `main` a la rama antes de empezar a trabajar. |
