"""n1 · ¿Existe isomorfismo entre dos redes?  (Elena Ruiz · Arquitectura)

Decisión: ISO = {<A, B> : existe biyección π: V_A → V_B con (i,j) ∈ E_A ⇔ (π(i),π(j)) ∈ E_B}.
Certificado: la permutación π (n números de O(log n) bits: tamaño polinomial).
Verificador: comparar los n² pares de la matriz -> O(n²)  ⇒  ISO ∈ NP.
NO se afirma NP-completitud: no se conoce una reducción desde un NPC y Babai (2015)
dio un algoritmo cuasi-polinómico; tampoco se conoce un algoritmo polinómico.
Búsqueda exhaustiva: ≤ n! permutaciones × O(n²) -> O(n!·n²) tiempo; O(n) espacio extra.
"""

from __future__ import annotations

from itertools import permutations
from typing import List, Optional, Sequence, Tuple

from ..conteo import contador_o_nulo

Matriz = Sequence[Sequence[int]]


def validar_matriz(M: Matriz, nombre: str = "M") -> int:
    """Grafo no dirigido simple: cuadrada, 0/1, simétrica, diagonal 0. O(n²)."""
    n = len(M)
    for i, fila in enumerate(M):
        if len(fila) != n:
            raise ValueError(f"{nombre} no es cuadrada (fila {i})")
        for j, x in enumerate(fila):
            if isinstance(x, bool) or x not in (0, 1):
                raise ValueError(f"{nombre}[{i}][{j}] debe ser 0 o 1")
        if fila[i] != 0:
            raise ValueError(f"{nombre} tiene un lazo en {i} (diagonal ≠ 0)")
    for i in range(n):
        for j in range(n):
            if M[i][j] != M[j][i]:
                raise ValueError(f"{nombre} no es simétrica: se asume red no dirigida")
    return n


def _preserva(A: Matriz, B: Matriz, pi: Sequence[int], contar) -> bool:
    n = len(A)
    for i in range(n):
        for j in range(n):
            contar("comparacion")
            if A[i][j] != B[pi[i]][pi[j]]:
                return False
    return True


def verificar(A: Matriz, B: Matriz, pi: Sequence[int], contar=None) -> bool:
    """Verificador polinómico del certificado π: O(n²) ("comparacion" ≤ n²)."""
    contar = contador_o_nulo(contar)
    n = validar_matriz(A, "A")
    if validar_matriz(B, "B") != n or len(pi) != n or sorted(pi) != list(range(n)):
        return False
    return _preserva(A, B, pi, contar)


def resolver(A: Matriz, B: Matriz, contar=None) -> Optional[Tuple[int, ...]]:
    """Búsqueda exhaustiva con poda barata por grados ("permutacion" ≤ n!)."""
    contar = contador_o_nulo(contar)
    n = validar_matriz(A, "A")
    if validar_matriz(B, "B") != n:
        return None
    grados_a = [sum(f) for f in A]
    grados_b = [sum(f) for f in B]
    if sorted(grados_a) != sorted(grados_b):  # invariante necesario, no suficiente
        return None
    for pi in permutations(range(n)):
        contar("permutacion")
        if any(grados_a[i] != grados_b[pi[i]] for i in range(n)):
            continue
        if _preserva(A, B, pi, contar):
            return pi
    return None


def ciclo(n: int) -> List[List[int]]:
    """Construye C_n (para ejemplos con los mismos grados)."""
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        M[i][(i + 1) % n] = M[(i + 1) % n][i] = 1
    return M


def union_de_ciclos(*tamanos: int) -> List[List[int]]:
    """Unión disjunta de ciclos, p. ej. union_de_ciclos(3, 3) = dos triángulos."""
    n = sum(tamanos)
    M = [[0] * n for _ in range(n)]
    base = 0
    for t in tamanos:
        for i in range(t):
            a, b = base + i, base + (i + 1) % t
            M[a][b] = M[b][a] = 1
        base += t
    return M
