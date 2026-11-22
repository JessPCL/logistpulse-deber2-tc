# Crecimiento medido (tiempos reales)

_Máquina: CPython 3.13.18 · x86_64. Los valores cambian según el equipo; lo que importa es la forma del crecimiento._

## TSP-decisión (c2): enumeración (peor caso, respuesta No) vs Held–Karp vs vecino más cercano

| n centros | tours (n−1)! | enumeración (s) | Held–Karp (s) | vecino más cercano (s) |
|---|---|---|---|---|
| 4 | 6 | 0.0000 | 0.0000 | 0.000074 |
| 5 | 24 | 0.0000 | 0.0000 | 0.000012 |
| 6 | 120 | 0.0002 | 0.0001 | 0.000016 |
| 7 | 720 | 0.0008 | 0.0003 | 0.000029 |
| 8 | 5,040 | 0.0061 | 0.0009 | 0.000026 |
| 9 | 40,320 | 0.0518 | 0.0015 | 0.000035 |
| 10 | 362,880 | 0.4555 | 0.0039 | 0.000053 |
| 12 | 39,916,800 | (no se ejecuta) | 0.027 | — |
| 14 | 6,227,020,800 | (no se ejecuta) | 0.130 | — |

### Extrapolación de la enumeración (con el costo por tour medido en n = 10)

| n centros | tours | tiempo estimado |
|---|---|---|
| 12 | 3.99e+07 | 5.01e+01 s ≈ 1.59e-06 años |
| 15 | 8.72e+10 | 1.09e+05 s ≈ 3.47e-03 años |
| 20 | 1.22e+17 | 1.53e+11 s ≈ 4.84e+03 años |
| 25 | 6.20e+23 | 7.79e+17 s ≈ 2.47e+10 años |

Conclusión: TSP-DEC es **decidible** para todo n (la enumeración termina), pero con 20–25 centros la búsqueda exhaustiva tarda de miles a miles de millones de años (ver tabla). Held–Karp (O(n²·2ⁿ)) aleja el límite, pero sigue siendo exponencial; la heurística es instantánea y no garantiza el óptimo.

## SAT (c1): fuerza bruta en el peor caso (respuesta No) y DPLL

| n variables | asignaciones 2ⁿ | fuerza bruta (s) |
|---|---|---|
| 12 | 4,096 | 0.009 |
| 14 | 16,384 | 0.035 |
| 16 | 65,536 | 0.145 |
| 18 | 262,144 | 0.519 |

### Extrapolación de la fuerza bruta (con el costo por asignación medido en n = 18)

| n variables | asignaciones | tiempo estimado |
|---|---|---|
| 30 | 1.07e+09 | 2.13e+03 s ≈ 6.74e-05 años |
| 40 | 1.10e+12 | 2.18e+06 s ≈ 6.90e-02 años |
| 60 | 1.15e+18 | 2.28e+12 s ≈ 7.24e+04 años |
| 100 | 1.27e+30 | 2.51e+24 s ≈ 7.96e+16 años |

### DPLL en 3-CNF aleatorias con m ≈ 4,26·n (la zona más difícil); mediana de 5 fórmulas

| n variables | m cláusulas | nodos del árbol | tiempo (s) |
|---|---|---|---|
| 20 | 85 | 17 | 0.001 |
| 40 | 170 | 215 | 0.024 |
| 60 | 256 | 600 | 0.135 |
| 80 | 341 | 5,011 | 1.738 |

Conclusión: SAT es **decidible** (hay 2ⁿ asignaciones finitas), pero la fuerza bruta se duplica con cada variable extra: con 60 decisiones de despacho ya serían siglos. DPLL poda mucho y llega más lejos, pero sus nodos también crecen de forma exponencial con n.

## Vertex Cover (c3): ramificación en el peor caso (respuesta No) y 2-aproximación

| k almacenes | nodos 2^(k+1)−1 | ramificación (s) |
|---|---|---|
| 10 | 2,047 | 0.001 |
| 12 | 8,191 | 0.006 |
| 14 | 32,767 | 0.024 |
| 16 | 131,071 | 0.098 |

### Extrapolación de la ramificación (con el costo por nodo medido en k = 16)

| k almacenes | nodos | tiempo estimado |
|---|---|---|
| 30 | 2.15e+09 | 1.60e+03 s ≈ 5.08e-05 años |
| 40 | 2.20e+12 | 1.64e+06 s ≈ 5.20e-02 años |
| 60 | 2.31e+18 | 1.72e+12 s ≈ 5.46e+04 años |
| 100 | 2.54e+30 | 1.89e+24 s ≈ 6.00e+16 años |

2-aproximación en un camino de 100,000 zonas: 0.223 s (O(V + E), garantiza |S| ≤ 2·ÓPTIMO).

Conclusión: con pocos almacenes (k pequeño) la ramificación exacta es rápida aunque haya muchas zonas; el costo explota con k (cada almacén extra duplica el árbol). Para k grandes se usa la 2-aproximación, que es instantánea pero puede usar hasta el doble de almacenes.

## Dijkstra (polinómico) en grafos aleatorios con E ≈ 4V

| V | E | tiempo (s) |
|---|---|---|
| 1,000 | 3,996 | 0.003 |
| 10,000 | 39,997 | 0.042 |
| 50,000 | 199,993 | 0.307 |

Conclusión: con 50 000 ubicaciones Dijkstra sigue respondiendo en segundos: O((V+E) log V) es resoluble en tiempo útil.
