# LOGISTPULSE · Deber 2 de Teoría de la Computación (USFQ)

**Decisiones, algoritmos y límites computacionales.** El repositorio incluye:
- los autómatas de pedido, reserva y orden de compra, con sus archivos JFLAP;
- la planta modelada como grafo ponderado (Dijkstra y BFS);
- FEFO con sus 3 políticas y la regla de reposición;
- los 10 casos del simulador (P / NP / NP-completo), con verificadores y reducciones ejecutables;
- **más de 140 pruebas reproducibles**, entre ellas pruebas que **atan cada Big-O al código** contando operaciones y midiendo tiempos.

**Si es tu primera vez en el repo, lee [`docs/EMPIEZA_AQUI.md`](docs/EMPIEZA_AQUI.md):** explica el deber desde cero, qué es cada cosa de GitHub y qué capturas tomar.

Equipo: **Camila · Luis · Jessica**. Los roles, los roles rotativos y los prompts están en [`equipo/ROLES_Y_PROMPTS.md`](equipo/ROLES_Y_PROMPTS.md), y el flujo de trabajo en [`equipo/GUIA_CODESPACES.md`](equipo/GUIA_CODESPACES.md).
**Cómo sabemos que cumple el enunciado:** [`docs/MATRIZ_TRAZABILIDAD.md`](docs/MATRIZ_TRAZABILIDAD.md) (cada requisito → archivo → prueba) y `python scripts/verificar_entrega.py`.

---

## Cómo ejecutarlo

### Opción A · GitHub Codespaces (recomendada para el equipo · repo público)
Repo → **Code → Codespaces → Create codespace on main**. El `.devcontainer/` instala Python 3.12, Graphviz, pandoc, GitHub CLI y las extensiones de Python, Jupyter y Mermaid, y corre las pruebas al crear el Codespace.
- Los tres trabajan en el **mismo entorno**, que es reproducible.
- Cada commit sale con **tu** nombre, en **tu** rama, y entra por un PR revisado. Esa es la evidencia de historial, ramas, revisiones y release que pide el criterio de gestión (1,0 pt).
- Guía paso a paso (configuración inicial, ramas, PR, revisión cruzada, Issues, tag y release): [`equipo/GUIA_CODESPACES.md`](equipo/GUIA_CODESPACES.md).
- JFLAP no corre en Codespaces (es un programa de escritorio): las capturas se sacan en la computadora y se suben al repo.
- El repo es **público**: el profesor abre el enlace directo y **GitHub Actions** (`.github/workflows/pruebas.yml`) corre las pruebas en cada push y PR, con Python 3.10 y 3.12.

### Opción B · Google Colab (para correr algo rápido sin abrir el Codespace)
1. Abre `LOGISTPULSE_Deber2_Colab.ipynb` en Colab (`Archivo → Subir notebook`).
2. Ejecuta la celda 1 y sube el **zip del repo**. Si el repo ya está en GitHub, usa la celda 1-B con `git clone`.
3. Ejecuta el resto: pruebas, demo, diagramas, tus propias pruebas (celdas editables), tiempos reales, revisión contra la rúbrica e informe.

### Opción C · Comandos (terminal del Codespace o local; Python ≥ 3.8, solo biblioteca estándar; probado en 3.8, 3.10, 3.11, 3.12 y 3.13)
```bash
python -m unittest discover -s tests -v     # más de 140 pruebas: funcionales + complejidad (conteo y tiempo)
python -m logistpulse                       # demo completa (o una sección: automatas | rutas | inventario | casos)
python scripts/generar_jflap.py             # jflap/*.jff + entradas para Multiple Run
python scripts/generar_diagramas.py         # docs/diagramas (requiere Graphviz; en Codespaces y Colab ya está)
python scripts/generar_docs.py              # tabla resumen, salidas observadas, tablas δ, inventario de pruebas
                                            #   y el bloque SALIDA de cada ficha (no toca lo redactado)
python scripts/medir_crecimiento.py         # tiempos REALES: n! vs Held–Karp vs heurística vs Dijkstra (Fase F)
python scripts/armar_informe.py             # junta todo en docs/generado/INFORME.md (+ .docx si hay pandoc)
python scripts/verificar_entrega.py         # listo / pendiente / error por criterio de la rúbrica
python scripts/crear_issues.py [--crear]    # un Issue de GitHub por correo y por historia del backlog
```
Todos los comandos se ejecutan **desde la carpeta raíz del repo**. Si la máquina está muy cargada y una prueba de *tiempo* falla por ruido, usa `LOGISTPULSE_SIN_TIEMPOS=1`; las pruebas de *conteo* siguen probando las cotas.

---

## Dónde está cada entregable

| Entregable del enunciado | Archivo(s) | Responsable |
|---|---|---|
| JFLAP (.jff) + diagramas de estados + secuencias | `jflap/*.jff`, `jflap/esperado_*.md`, `jflap/capturas/`, `docs/diagramas/afd_*.png`, `docs/fase_A_automatas.md` | Camila |
| Grafo ponderado + ruta encontrada | `data/planta.json`, `docs/diagramas/planta_ruta.png`, `docs/fase_B_rutas.md` | Luis |
| Pseudocódigo (rutas, FEFO, reposición) + terminación + Big-O | `docs/fase_B_rutas.md`, `docs/fase_C_fefo_reposicion.md` | Luis |
| Implementación + pruebas reproducibles (normales, límite, inválidas) | `logistpulse/`, `tests/`, `docs/fase_E_implementacion.md`, `docs/generado/inventario_pruebas.md` | Todos (PR + revisión cruzada) |
| Verificador de certificado | `verificar(...)` en `logistpulse/casos/n*.py` y `c*.py` | — |
| 10 fichas + tabla resumen | `docs/fichas/*.md` (modelo terminado: `p1.md`; formato: `docs/PLANTILLA_FICHA.md`), `docs/generado/tabla_resumen.md` | p: Luis · n: Camila · c: Jessica |
| Informe sobre el problema de la parada | `docs/fase_F_nota_parada.md` (+ evidencia en `docs/generado/crecimiento.md`) | Jessica |
| Supuestos, límites y conclusiones (rúbrica de comunicación) | `docs/conclusiones.md` | Jessica |
| Tres sprints (roles rotativos, una unidad de trabajo por correo) + release | `docs/sprints/`, historial Git, tags `v1.0` y `v1.1` (versión final) | Rol de coordinación de cada sprint |
| Informe PDF (resume el análisis y enlaza al repositorio lo demás) | `scripts/armar_informe.py` → `docs/generado/INFORME.docx` → Word (Times New Roman 12) → PDF adjunto al release `v1.1` y subido al aula (no se versiona por su peso; `--completo` = todo dentro del PDF) | Jessica |
| Presentación de 8–10 min | `docs/presentacion_guion.md` | Todos (integra Jessica) |

```
logistpulse/
├── io_datos.py            ← LECTURA: carga y valida data/*.json (planta, lotes, SKU, 10 expedientes)
├── automatas/  rutas/  inventario/  casos/   ← PROCESAMIENTO: algoritmos puros, sin E/S
│     casos/__init__.py = registro de los 10 correos (fuente de la tabla resumen)
├── presentacion.py  presentacion_casos.py   ← PRESENTACIÓN: textos y tablas
├── conteo.py              ← Contador de operaciones (respaldo empírico del Big-O)
└── __main__.py            ← demo
data/      planta.json · lotes_fefo.json · skus_reposicion.json · casos_simulador.json
jflap/     .jff + entradas para Multiple Run + resultados esperados + guía + capturas/
docs/      DECISIONES_Y_HALLAZGOS.md (leer primero) · MATRIZ_TRAZABILIDAD.md · PLANTILLA_FICHA.md
           fase_A/B/C/E/F · fichas/ · sprints/ · conclusiones.md · referencias/ · diagramas/ · generado/
scripts/   generadores (.jff, diagramas, docs, informe), medición de tiempos y revisión de la entrega
tests/     más de 140 pruebas unittest (también corren con pytest)
```

---

## Resultados clave (detalle en `docs/DECISIONES_Y_HALLAZGOS.md`)
- **Planta:** Dijkstra R→D = **11 m** por R→B→A→E→D. La ruta de la Figura 5 (R→B→A→P→E→D) **empata** en 11 m. Con el pasillo A bloqueado: 12 m. Con Empaque bloqueado: no hay ruta.
- **FEFO:** un pedido de 80 toma L-001:30, L-002:25 (empatan en fecha y desempata el código) y L-003:25. Si falta stock: PARCIAL, RECHAZADO o EN_ESPERA según la política.
- **Reposición:** el ejemplo del enunciado da posición 23 y sugerencia **27**. No hay sugerencias duplicadas si ya existe una orden abierta.
- **10 correos:** A = {p1, p2, p3} · B = {n1–n4} · C = {c1–c3}. Las reducciones de los NP-completos se pueden ejecutar y están probadas.
- **Complejidad comprobada:** Edmonds–Karp hace los mismos aumentos con capacidades ×10⁶; la búsqueda de factores se duplica por cada bit; la enumeración TSP crece ×(n−1).

---

## Flujo de trabajo Git (3 sprints)
- `main` está protegida: todo entra por **Pull Request** con **1 aprobación de otro integrante** y el check de **GitHub Actions** en verde.
- Ramas: `camila/fase-a-fichas-np`, `luis/fase-bc-fichas-p`, `jessica/fase-df-gestion`. Cada persona edita **sus** archivos (tabla de arriba).
- Un *Issue* por correo y por historia del backlog (`python scripts/crear_issues.py --crear`); el PR lo cierra con `Closes #N`.
- Comandos exactos (`gh pr create`, `gh pr review`, `gh pr merge`, `gh release create`): `equipo/GUIA_CODESPACES.md`.
- Si cambian el código: pruebas en OK → `python scripts/generar_docs.py`. Antes de cada PR y antes de entregar: `python scripts/verificar_entrega.py`.
- Cierre: `git tag -a v1.0 -m "Entrega final Deber 2"` → `git push origin v1.0` → *Release* en GitHub. La versión final del informe se publicó como release `v1.1`.

## Declaración de uso de IA
- **Herramientas:** cada integrante usó un asistente de IA conversacional con los prompts de `equipo/ROLES_Y_PROMPTS.md`; Jessica usó Claude (Anthropic).
- **Para qué:** generar y revisar el código Python y sus pruebas, redactar borradores de las fichas, las fases y el informe, y organizar el repositorio y los sprints.
- **Cómo se verificó:** 146 pruebas automáticas (casos normales, límites e inválidos), pruebas de complejidad que cuentan operaciones, comparación de los .jff en JFLAP (Multiple Run), salidas generadas ejecutando el código y revisión cruzada de cada cambio en un PR aprobado por otro integrante.
- **Responsabilidad:** cada integrante revisó, entiende y defiende su parte: Camila (Fase A, JFLAP, n1–n4), Luis (Fases B y C, p1–p3) y Jessica (gestión, c1–c3, Fase F, conclusiones e informe).

## Referencias
Sipser, *Introduction to the Theory of Computation*, 3.ª ed. (caps. 1, 4, 5 y 7) · CLRS (caminos mínimos, flujo máximo, NP-completitud) · Cook (1971) · Karp (1972) · JFLAP: https://www.jflap.org
