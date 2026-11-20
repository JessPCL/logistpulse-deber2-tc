"""c2 · ¿Existe un recorrido dentro del presupuesto L?  (Jorge Tapia · Ruteo)

Decisión: TSP-DEC = {<D, L> : existe un ciclo que visita cada centro exactamente
una vez, vuelve al inicio y cuesta ≤ L}.  (El correo pide REGRESAR al punto de
salida ⇒ ciclo hamiltoniano, no camino.)
Optimización (distinta): hallar el ciclo de costo mínimo (Held–Karp).

∈ NP: certificado = orden de visita (n índices); verificador O(n).
NP-difícil: HAM-CYCLE ≤p TSP-DEC (Karp 1972). Dado G=(V,E) con n vértices,
construir D con D[u][v] = 1 si (u,v) ∈ E, 2 si no, y L = n. G tiene ciclo
hamiltoniano ⇔ hay tour de costo ≤ n. Construcción O(n²) ⇒ polinómica.

Algoritmos: enumeración O(n!·n) (se fija el inicio: (n−1)! órdenes); Held–Karp
O(n²·2ⁿ) tiempo y O(n·2ⁿ) espacio (exacto); vecino más cercano O(n²) (heurística,
SIN garantía de optimalidad).
"""

from __future__ import annotations

from itertools import permutations
from typing import Iterable, List, Optional, Sequence, Tuple

from ..conteo import contador_o_nulo

Matriz = Sequence[Sequence[float]]

def validar(D: Matriz) -> int:
    n = len(D)
    if n < 2:
        raise ValueError("Se necesitan al menos 2 centros")
    for i, fila in enumerate(D):
        if len(fila) != n:
            raise ValueError(f"La matriz no es cuadrada (fila {i})")
        for j, x in enumerate(fila):
            if isinstance(x, bool) or not isinstance(x, (int, float)) or x < 0:
                raise ValueError(f"D[{i}][{j}] debe ser un número ≥ 0")
    return n


def costo(D: Matriz, tour: Sequence[int]) -> float:
    return sum(D[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))


def verificar(D: Matriz, L: float, tour: Sequence[int], contar=None) -> bool:
    """Verificador O(n) ("paso" ≤ 2n): ciclo cerrado, cada centro una vez, costo ≤ L.

    (validar(D) revisa la matriz de entrada en O(n²); eso es leer la entrada, no verificar el certificado.)
    """
    contar = contador_o_nulo(contar)
    n = validar(D)
    if len(tour) != n + 1 or tour[0] != tour[-1]:
        return False
    visto = [False] * n  # O(n): cada centro exactamente una vez
    for c in tour[:-1]:
        contar("paso")
        if isinstance(c, bool) or not isinstance(c, int) or not 0 <= c < n or visto[c]:
            return False
        visto[c] = True
    contar("paso", n)  # sumar n distancias
    return costo(D, tour) <= L


def decidir(D: Matriz, L: float, contar=None) -> Optional[Tuple[Tuple[int, ...], float]]:
    """Enumeración exhaustiva ("tour" ≤ (n−1)!); devuelve el primer tour con costo ≤ L o None."""
    contar = contador_o_nulo(contar)
    n = validar(D)
    for resto in permutations(range(1, n)):
        contar("tour")
        tour = (0,) + resto + (0,)
        c = costo(D, tour)
        if c <= L:
            return tour, c
    return None


def held_karp(D: Matriz, contar=None) -> Tuple[Tuple[int, ...], float]:
    """Versión de OPTIMIZACIÓN exacta (programación dinámica sobre subconjuntos).

    C[S][j] = costo mínimo de salir de 0, visitar exactamente S (0 ∈ S) y terminar en j.
    Se recorren las máscaras en orden creciente: agregar un bit aumenta el número,
    así que C[S] ya es definitivo cuando se usa. 2ⁿ máscaras × n finales × n
    extensiones = O(n²·2ⁿ) tiempo; la tabla ocupa O(n·2ⁿ).
    """
    contar = contador_o_nulo(contar)
    n = validar(D)
    INF = float("inf")
    C = [[INF] * n for _ in range(1 << n)]
    previo = [[-1] * n for _ in range(1 << n)]
    C[1][0] = 0
    for S in range(1, 1 << n):
        if not S & 1:
            continue  # todo recorrido parcial contiene al inicio 0
        for j in range(n):
            if C[S][j] == INF:
                continue
            for k in range(1, n):
                if S & (1 << k):
                    continue
                contar("transicion")  # ≤ 2^(n−1)·n·(n−1) ≤ n²·2ⁿ
                T = S | (1 << k)
                cand = C[S][j] + D[j][k]
                if cand < C[T][k]:
                    C[T][k], previo[T][k] = cand, j
    completo = (1 << n) - 1
    mejor, ultimo = min((C[completo][j] + D[j][0], j) for j in range(1, n))
    tour, S, j = [], completo, ultimo
    while j != 0:
        tour.append(j)
        S, j = S ^ (1 << j), previo[S][j]
    return (0,) + tuple(reversed(tour)) + (0,), mejor


def vecino_mas_cercano(D: Matriz, inicio: int = 0, contar=None) -> Tuple[Tuple[int, ...], float]:
    """Heurística O(n²) ("comparacion" ≤ n²): rápida, sin garantía de optimalidad."""
    contar = contador_o_nulo(contar)
    n = validar(D)
    tour, visitados = [inicio], {inicio}
    while len(tour) < n:
        u = tour[-1]
        candidatos = [j for j in range(n) if j not in visitados]
        contar("comparacion", len(candidatos))
        v = min(candidatos, key=lambda j: (D[u][j], j))
        tour.append(v)
        visitados.add(v)
    tour.append(inicio)
    return tuple(tour), costo(D, tour)


def reducir_ham_a_tsp(n: int, aristas: Iterable[Tuple[int, int]]) -> Tuple[List[List[int]], int]:
    """Reducción polinómica HAM-CYCLE ≤p TSP-DEC. O(n²)."""
    D = [[0 if i == j else 2 for j in range(n)] for i in range(n)]
    for u, v in aristas:
        if not (0 <= u < n and 0 <= v < n) or u == v:
            raise ValueError(f"Arista inválida ({u},{v})")
        D[u][v] = D[v][u] = 1
    return D, n
