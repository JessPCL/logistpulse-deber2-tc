# Crecimiento medido (tiempos reales)

_Máquina: CPython 3.13.18 · x86_64. Los valores cambian según el equipo; lo que importa es la forma del crecimiento._

## TSP-decisión (c2): enumeración (peor caso, respuesta No) vs Held–Karp vs vecino más cercano

| n centros | tours (n−1)! | enumeración (s) | Held–Karp (s) | vecino más cercano (s) |
|---|---|---|---|---|
| 4 | 6 | 0.0000 | 0.0000 | 0.000022 |
| 5 | 24 | 0.0000 | 0.0000 | 0.000008 |
| 6 | 120 | 0.0001 | 0.0001 | 0.000009 |
| 7 | 720 | 0.0004 | 0.0001 | 0.000011 |
| 8 | 5,040 | 0.0032 | 0.0003 | 0.000014 |
| 9 | 40,320 | 0.0276 | 0.0008 | 0.000020 |
| 10 | 362,880 | 0.2710 | 0.0022 | 0.000026 |
| 12 | 39,916,800 | (no se ejecuta) | 0.015 | — |
| 14 | 6,227,020,800 | (no se ejecuta) | 0.066 | — |

### Extrapolación de la enumeración (con el costo por tour medido en n = 10)

| n centros | tours | tiempo estimado |
|---|---|---|
| 12 | 3.99e+07 | 2.98e+01 s ≈ 9.45e-07 años |
| 15 | 8.72e+10 | 6.51e+04 s ≈ 2.06e-03 años |
| 20 | 1.22e+17 | 9.09e+10 s ≈ 2.88e+03 años |
| 25 | 6.20e+23 | 4.63e+17 s ≈ 1.47e+10 años |

Conclusión: TSP-DEC es **decidible** para todo n (la enumeración termina), pero con 20–25 centros la búsqueda exhaustiva tarda de miles a miles de millones de años (ver tabla). Held–Karp (O(n²·2ⁿ)) aleja el límite, pero sigue siendo exponencial; la heurística es instantánea y no garantiza el óptimo.

## Dijkstra (polinómico) en grafos aleatorios con E ≈ 4V

| V | E | tiempo (s) |
|---|---|---|
| 1,000 | 3,997 | 0.002 |
| 10,000 | 39,996 | 0.033 |
| 50,000 | 199,998 | 0.253 |

Conclusión: con 50 000 ubicaciones Dijkstra sigue respondiendo en segundos: O((V+E) log V) es resoluble en tiempo útil.
