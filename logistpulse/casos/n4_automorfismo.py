"""n4 · ¿La topología tiene una simetría?  (Santiago Jaramillo · Analítica)

Decisión: AUT-NO-TRIVIAL = {<G> : ∃ permutación π ≠ id con (i,j) ∈ E ⇔ (π(i),π(j)) ∈ E}.
Certificado: π (n enteros). Verificador: biyección, π ≠ id y n² comparaciones
-> O(n²) ⇒ AUT-NO-TRIVIAL ∈ NP.
Se reduce a isomorfismo de grafos (no se conoce que sea NP-completo).
Búsqueda exhaustiva: hasta n! permutaciones -> O(n!·n²) tiempo, O(n) extra.
Un "No" exige AGOTAR todas las permutaciones (no hay un certificado corto conocido).
"""

from __future__ import annotations

from itertools import permutations
from typing import Optional, Sequence, Tuple

from ..conteo import contador_o_nulo
from .n1_isomorfismo import _preserva, validar_matriz


def verificar(G: Sequence[Sequence[int]], pi: Sequence[int], contar=None) -> bool:
    """Verificador O(n²) del certificado π."""
    contar = contador_o_nulo(contar)
    n = validar_matriz(G, "G")
    if len(pi) != n or sorted(pi) != list(range(n)):
        return False
    if tuple(pi) == tuple(range(n)):
        return False  # la identidad no cuenta
    return _preserva(G, G, pi, contar)


def resolver(G: Sequence[Sequence[int]], contar=None) -> Tuple[Optional[Tuple[int, ...]], int]:
    """Devuelve (π o None, número de permutaciones examinadas)."""
    contar = contador_o_nulo(contar)
    n = validar_matriz(G, "G")
    grados = [sum(f) for f in G]
    examinadas = 0
    for pi in permutations(range(n)):
        examinadas += 1
        contar("permutacion")
        if pi == tuple(range(n)):
            continue
        if any(grados[i] != grados[pi[i]] for i in range(n)):
            continue  # un automorfismo preserva grados
        if _preserva(G, G, pi, contar):
            return pi, examinadas
    return None, examinadas
