"""c3 · ¿Bastan k almacenes para cubrir todas las zonas?  (Carla Núñez · Red logística)

Decisión: VERTEX-COVER = {<G, k> : ∃ S ⊆ V, |S| ≤ k, toda arista (u,v) tiene u ∈ S o v ∈ S}.
(El correo nombra Vertex Cover y pregunta "¿Cubre toda arista?", pero también dice
"zona cubierta por un almacén propio o vecino", que sería Dominating Set. Seguimos
Vertex Cover (etiqueta, datos y código del correo; hallazgo H7). Ambos son NP-completos.)
Vocabulario: vértice = zona; arista = par de zonas adyacentes; S = zonas con almacén.

∈ NP: certificado = S; verificador O(V + E).
NP-difícil: INDEPENDENT-SET ≤p VERTEX-COVER: S es cobertura ⇔ V∖S es independiente,
así <G, k> ∈ IS ⇔ <G, |V|−k> ∈ VC (Karp 1972). Transformación O(V + E).
(Sipser, sección 7.5, prueba que VERTEX-COVER es NPC con otra reducción, desde 3SAT.)

Algoritmos: exacto por ramificación acotada O(2^k·(V + E)) (elegir una arista sin
cubrir (u,v) y ramificar u ∈ S o v ∈ S); exacto por subconjuntos O(2^V·(V + E));
aproximación de factor 2 por emparejamiento maximal O(V + E): |S| ≤ 2·ÓPTIMO.
"""

from __future__ import annotations

from itertools import combinations
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Set, Tuple

from ..conteo import contador_o_nulo


def ady_desde_aristas(aristas: Iterable[Sequence[str]], vertices: Iterable[str] = ()) -> Dict[str, List[str]]:
    """Lista de adyacencias [u, v] entre zonas -> lista de adyacencia no dirigida. O(V + E)."""
    ady: Dict[str, List[str]] = {v: [] for v in vertices}
    for a in aristas:
        if len(a) != 2:
            raise ValueError(f"Arista inválida {a!r} (se esperan dos zonas)")
        u, v = a
        ady.setdefault(u, [])
        ady.setdefault(v, [])
        if v in ady[u]:
            raise ValueError(f"Adyacencia repetida {u}-{v}")
        ady[u].append(v)
        ady[v].append(u)
    return ady


def aristas_de(ady: Mapping[str, Iterable[str]], contar=None) -> Tuple[Set[str], List[Tuple[str, str]]]:
    """Valida la lista de adyacencia (no dirigida, sin lazos) y devuelve (V, E).

    O(V + E): una pasada; cada arista se guarda una vez como (min, max) en el
    orden en que aparece (determinista, sin ordenar todo E).
    """
    contar = contador_o_nulo(contar)
    V = set(ady)
    vecinos = {u: set(vs) for u, vs in ady.items()}
    vistos, E = set(), []
    for u, vs in ady.items():
        for v in vs:
            contar("paso")
            if v == u:
                raise ValueError(f"Lazo en {u} no permitido")
            if v not in vecinos or u not in vecinos[v]:
                raise ValueError(f"Adyacencia no simétrica: {u}-{v}")
            arista = (u, v) if u < v else (v, u)
            if arista not in vistos:
                vistos.add(arista)
                E.append(arista)
    return V, E


def verificar(ady: Mapping[str, Iterable[str]], k: int, S: Iterable[str], contar=None) -> bool:
    """Verificador O(V + E) del certificado S ("paso" ≤ 3E + |S|)."""
    contar = contador_o_nulo(contar)
    V, E = aristas_de(ady, contar)
    S = set(S)
    contar("paso", len(S))
    if not S <= V or len(S) > k:
        return False
    for u, v in E:
        contar("paso")
        if u not in S and v not in S:
            return False
    return True


def ramificacion(ady: Mapping[str, Iterable[str]], k: int, contar=None) -> Optional[Set[str]]:
    """Exacto, O(2^k·(V + E)): árbol binario de profundidad ≤ k ("nodo" ≤ 2^(k+1) − 1)."""
    contar = contador_o_nulo(contar)
    if isinstance(k, bool) or not isinstance(k, int) or k < 0:
        raise ValueError("k debe ser entero ≥ 0")
    _, E = aristas_de(ady)

    def buscar(aristas: List[Tuple[str, str]], k: int, S: Set[str]) -> Optional[Set[str]]:
        contar("nodo")
        if not aristas:
            return S
        if k == 0:
            return None
        u, v = aristas[0]
        for elegido in (u, v):
            restantes = [e for e in aristas if elegido not in e]
            r = buscar(restantes, k - 1, S | {elegido})
            if r is not None:
                return r
        return None

    return buscar(E, k, set())


def minimo_por_subconjuntos(ady: Mapping[str, Iterable[str]], contar=None) -> Set[str]:
    """Exacto, O(2^V·(V + E)): prueba subconjuntos por tamaño creciente ("subconjunto" ≤ 2^V)."""
    contar = contador_o_nulo(contar)
    V, E = aristas_de(ady)
    for tam in range(len(V) + 1):
        for S in combinations(sorted(V), tam):
            contar("subconjunto")
            if all(u in S or v in S for u, v in E):
                return set(S)
    return set(V)


def aproximacion_2(ady: Mapping[str, Iterable[str]], contar=None) -> Set[str]:
    """Aproximación: ambos extremos de un emparejamiento maximal. |S| ≤ 2·ÓPT. O(V + E)."""
    contar = contador_o_nulo(contar)
    _, E = aristas_de(ady)
    S: Set[str] = set()
    for u, v in E:
        contar("arista")
        if u not in S and v not in S:
            S |= {u, v}
    return S


def reducir_is_a_vc(ady: Mapping[str, Iterable[str]], k_is: int) -> Tuple[Mapping[str, Iterable[str]], int]:
    """INDEPENDENT-SET ≤p VERTEX-COVER: mismo grafo, k_vc = |V| − k_is.  O(V + E).

    Si k_is > |V| no puede haber un conjunto independiente tan grande: se devuelve una
    instancia fija con respuesta No (una arista y k = 0), así la transformación es total.
    """
    if isinstance(k_is, bool) or not isinstance(k_is, int):
        raise ValueError("k debe ser entero")
    V, _ = aristas_de(ady)
    if k_is > len(V):
        return {"a": ["b"], "b": ["a"]}, 0
    return ady, len(V) - k_is


def estrella(n_hojas: int) -> Dict[str, List[str]]:
    hojas = [f"h{i}" for i in range(n_hojas)]
    g = {"centro": hojas[:]}
    g.update({h: ["centro"] for h in hojas})
    return g
