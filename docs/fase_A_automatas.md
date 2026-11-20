# Fase A · Autómatas de pedido, reserva y orden de compra
**Responsable: Camila** · Rúbrica: 2,0 pts (tres modelos correctos; estados, eventos, transiciones aceptadas y no válidas; evidencia JFLAP)

> PENDIENTE: redactar con el prompt de `equipo/ROLES_Y_PROMPTS.md`. Base técnica: `docs/generado/tablas_transiciones.md`, `jflap/esperado_*.md`, `docs/diagramas/afd_*.png`.

## Checklist
- [ ] M = (Q, Σ, δ, q0, F) de los 3 autómatas, con el significado de cada estado y evento
- [ ] Tabla de transiciones + sumidero ERROR
- [ ] Justificación de F (criterio único, decisión A1) y de los eventos agregados (A5–A7)
- [ ] ≥ 2 secuencias válidas y ≥ 2 inválidas por autómata, con la transición que acepta o rechaza
- [ ] Capturas JFLAP (determinismo, Multiple Run, trazas) en `jflap/capturas/`
- [ ] Cómo se probó: JFLAP + `tests/test_automatas.py` + `tests/test_jflap.py`
