# Tabla resumen de los 10 correos

_Generada por `scripts/generar_docs.py` desde `logistpulse/casos/__init__.py`. No editar a mano._

| Correo | Clase | Tipo de problema | Decidible | Algoritmo | Complejidad (tiempo · espacio) | Estrategia |
|--------------------|----------|-------------|----------|--------------------|------------------|-----------|
| **p1** ¿Puede llegar el envío a la zona Norte? | P | Decisión | Sí | BFS | O(V + E) · O(V) | Exacto |
| **p2** Ruta mínima entre centros de distribución | P | Optimización → se clasifica su versión de decisión | Sí | Dijkstra (heap binario) | O((V + E) log V) · O(V + E) | Exacto |
| **p3** Máximo de camiones hacia clientes | P | Optimización → se clasifica su versión de decisión | Sí | Edmonds–Karp (Ford–Fulkerson con BFS) | O(V·E²) · O(V + E) | Exacto |
| **n1** Comparar topologías equivalentes | NP | Decisión | Sí | Búsqueda exhaustiva de permutaciones (+ poda por grados) | O(n!·n²) · O(n²) entrada + O(n) extra | Exacto |
| **n2** ¿Tiene N un factor en este intervalo? | NP | Decisión | Sí | Prueba por división exhaustiva | O(B·L²) — exponencial en L si B ≈ √N · O(L) | Exacto |
| **n3** ¿Existe exponente x que produzca h? | NP | Decisión | Sí | Búsqueda exhaustiva con exponenciación modular (alternativa: baby-step giant-step) | O(B·M(log p)) lineal · O(√B·M(log p)) BSGS · O(1) lineal · O(√B) BSGS | Exacto |
| **n4** ¿La topología tiene una simetría? | NP | Decisión | Sí | Permutaciones + verificación de adyacencia | O(n!·n²) · O(n) extra | Exacto |
| **c1** ¿Hay una asignación que cumpla todas las reglas? | NP-completo | Decisión | Sí | DPLL (propagación unitaria + literal puro) | DPLL O(2ⁿ·n·m·k) peor caso (fuerza bruta O(2ⁿ·m·k)) · O(n·m·k) (una copia simplificada por nivel de recursión) | Exacto |
| **c2** ¿Existe una ruta hamiltoniana dentro del presupuesto? | NP-completo | Decisión | Sí | Enumeración de permutaciones (decisión) · Held–Karp (optimización) · vecino más cercano (heurística) | O((n−1)!·n) = O(n!) · Held–Karp O(n²·2ⁿ) · O(n) · Held–Karp O(n·2ⁿ) | Exacto (enumeración, Held–Karp) / heurístico (vecino más cercano) |
| **c3** ¿Bastan k almacenes para cubrir todas las zonas? | NP-completo | Decisión | Sí | Backtracking / ramificación acotada (exacto) · 2-aproximación por emparejamiento (heurística) | O(2^k·(V + E)) ramificación · O(V + E) aproximación · O(k·(V + E)) (lista de aristas por nivel) | Exacto (ramificación) / aproximado (factor 2) |

Evidencia de cada clase (detalle en cada ficha):

- **p1** (P): Algoritmo polinómico conocido: BFS.
- **p2** (P): Algoritmo polinómico conocido: Dijkstra (requiere pesos ≥ 0).
- **p3** (P): Algoritmo polinómico conocido: Edmonds–Karp; el corte mínimo certifica optimalidad.
- **n1** (NP): Certificado π + verificador O(n²) ⇒ ∈ NP.
- **n2** (NP): Certificado d + verificador O(L²) ⇒ ∈ NP.
- **n3** (NP): Certificado x + verificador con exponenciación rápida ⇒ ∈ NP.
- **n4** (NP): Certificado π + verificador O(n²) ⇒ ∈ NP.
- **c1** (NP-completo): Verificador O(m·k) + 3-SAT ≤p DESPACHO-SAT (identidad); Cook–Levin.
- **c2** (NP-completo): Verificador O(n) + HAM-CYCLE ≤p TSP-DEC (pesos 1/2, L = n).
- **c3** (NP-completo): Verificador O(V + E) + INDEPENDENT-SET ≤p VERTEX-COVER.

Grupo A = algoritmo polinómico conocido · B = pertenencia a NP con certificado (sin afirmar NPC) · C = NP-completo con reducción. Distribución: A = 3 (p1, p2, p3) · B = 4 (n1–n4) · C = 3 (c1–c3).
