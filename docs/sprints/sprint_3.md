# Sprint 3
**Fechas:** lunes 23 al martes 24 de noviembre de 2026 (el cierre y el release se adelantaron al domingo 22/11, porque el martes 24 el equipo tiene otra entrega) · **Objetivo:** Analizar los diez correos; conectar decidibilidad/computabilidad/P-NP; presentar resultados.
**Evidencia de revisión que pide el enunciado:** Release del informe, código, modelos JFLAP y retrospectiva.

## Roles de este sprint (rotativos)
| Coordinación y backlog | Formalización | Algoritmos y análisis | Implementación y validación |
|---|---|---|---|
| Luis | Jessica | Camila | Camila |

## Planificación
| Tarea (ID del backlog) | Responsable | Rama / PR | Revisor | Estado |
|---|---|---|---|---|
| Simulador: los diez correos + reporte .txt | Luis | `jessica/fase-df-gestion` · #34 | Jessica | Hecho (22/11, #34) |
| Guion completo y diapositivas de la exposición (8–10 min) | Los tres (integra Jessica) | #31, #33, #35 | Luis | Guion hecho (22/11, #31, #33, #35) · diapositivas y ensayo con cronómetro: lunes 23/11 (no van en el release) |
| Captura `pedido_determinismo.png` con la franja de *Nondeterminism* | Camila | `camila/fase-a-fichas-np` | Jessica | Opcional, no bloquea la entrega (el determinismo ya consta en la tabla δ total y en las otras dos capturas) |
| F-G1 · Informe PDF (`scripts/armar_informe.py` → Word → PDF; enlaza al repositorio fichas, código y pruebas) | Jessica | `jessica/fase-df-gestion` · #36 y cierre | Luis | Hecho (22/11): fuente en `docs/generado/INFORME.md`; el PDF va adjunto al release `v1.0` y se sube al aula (no se versiona por su peso) |
| F-G1 · Tag `v1.0` + release con el PDF | Jessica | `main` | — | Hecho (22/11), al integrar el cierre: *Releases → v1.0* |

## Revisión (demo del sprint) · domingo 22/11
- Qué se mostró: el informe PDF armado desde los documentos del repositorio (análisis de las seis fases, una ficha resumida por correo con enlace a la ficha completa), el simulador con los diez correos (10/10 coinciden con nuestro análisis) y el guion completo de 8–10 minutos con la parte de cada integrante.
- Comentarios del revisor (Luis): aprobó el simulador (#34) y el armador del informe (#36) sin pedir cambios.
- Estado de `python scripts/verificar_entrega.py` al cierre: 146 pruebas OK; todos los criterios en OK salvo el tag `v1.0` y la captura del release, que se crean justo después de integrar este cierre.

## Retrospectiva
| Qué salió bien | Qué salió mal | Qué mejoramos el próximo sprint |
|---|---|---|
| Revisión cruzada en cada PR (Luis → Jessica, Camila → Luis, Jessica → Camila) con Actions en verde; el simulador coincidió 10/10 con las fichas; el informe se arma solo desde los `.md`, sin copiar a mano. | Los sprints se comprimieron porque al inicio no teníamos clara la fecha real (24/11) y coincide con otra entrega; algunas capturas se tomaron tarde o hubo que repetirlas; un error de bash con `!` al aprobar un PR. | Fijar la fecha real de entrega el primer día y planificar desde ahí; tomar cada captura en el momento (lista en `docs/EMPIEZA_AQUI.md`); ensayar la exposición con cronómetro antes del día. |
