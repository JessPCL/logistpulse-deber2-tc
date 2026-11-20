"""Dijkstra con cola de prioridad (heap binario) y reconstrucción por predecesores.

Precondiciones: grafo con pesos ≥ 0 (GrafoPonderado lo garantiza), origen ∈ V.
Zonas bloqueadas: se tratan como vértices eliminados (no se entra en ellos).

Terminación: cada vértice se FINALIZA a lo sumo una vez (conjunto `finalizados`);
cada arista se relaja a lo sumo una vez por extremo finalizado, y cada relajación
inserta como máximo una entrada en el heap. Hay a lo sumo |E| (o 2|E| si no es
dirigido) inserciones, así que el bucle termina tras O(|E|) extracciones.

Complejidad: O((|V| + |E|) log |V|) tiempo; O(|V| + |E|) espacio (dist, pred y
heap con inserción perezosa; el heap tiene ≤ |E| + 1 entradas y log|E| = O(log|V|)).
Desempate reproducible: el heap compara (distancia, nombre del vértice) y los
vecinos se recorren en orden alfabético: Σ d(u)·log d(u) = O(|E| log |V|), que
queda dentro de la misma cota.
"""

from __future__ import annotations

import heapq
import math
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Set, Tuple

from ..conteo import contador_o_nulo
from .grafo import GrafoPonderado

INF = math.inf


@dataclass
class ResultadoDijkstra:
    origen: str
    dist: Dict[str, float]
    pred: Dict[str, Optional[str]]
    orden_finalizacion: List[Tuple[str, float]]
    traza: List[str] = field(default_factory=list)

    def ruta_a(self, destino: str) -> Optional[List[str]]:
        if destino not in self.dist:
            raise ValueError(f"Destino desconocido: {destino}")
        if self.dist[destino] == INF:
            return None
        ruta, v = [], destino
        while v is not None:
            ruta.append(v)
            v = self.pred[v]
        return ruta[::-1]


def _validar(grafo: GrafoPonderado, origen: str, bloqueados: Set[str]) -> None:
    if origen not in grafo:
        raise ValueError(f"Origen '{origen}' no pertenece a V")
    desconocidos = bloqueados - set(grafo.vertices)
    if desconocidos:
        raise ValueError(f"Zonas bloqueadas que no existen en la planta: {sorted(desconocidos)}")
    if origen in bloqueados:
        raise ValueError(f"El origen '{origen}' está bloqueado: el AMR no puede partir de ahí")


def dijkstra(grafo: GrafoPonderado, origen: str, bloqueados: Iterable[str] = (),
             con_traza: bool = False, contar=None) -> ResultadoDijkstra:
    """contar: "insercion" ≤ E⃗+1, "extraccion" ≤ inserciones, "arista" ≤ E⃗ (E⃗ = entradas de adyacencia)."""
    contar = contador_o_nulo(contar)
    bloqueados = set(bloqueados)
    _validar(grafo, origen, bloqueados)
    dist = {v: INF for v in grafo.vertices}
    pred: Dict[str, Optional[str]] = {v: None for v in grafo.vertices}
    dist[origen] = 0
    heap: List[Tuple[float, str]] = [(0, origen)]
    contar("insercion")
    finalizados: Set[str] = set()
    orden: List[Tuple[str, float]] = []
    traza: List[str] = []

    while heap:
        d, u = heapq.heappop(heap)
        contar("extraccion")
        if u in finalizados:  # entrada obsoleta (inserción perezosa)
            continue
        finalizados.add(u)
        orden.append((u, d))
        if con_traza:
            traza.append(f"Extraer {u} (dist={d:g})")
        for v, w in grafo.vecinos(u):
            contar("arista")
            if v in bloqueados or v in finalizados:
                continue
            nd = d + w
            if nd < dist[v]:
                if con_traza:
                    antes = "∞" if dist[v] == INF else f"{dist[v]:g}"
                    traza.append(f"   relajar {u}->{v}: {antes} → {nd:g} (pred[{v}]={u})")
                dist[v] = nd
                pred[v] = u
                heapq.heappush(heap, (nd, v))
                contar("insercion")
    for b in bloqueados:
        dist[b], pred[b] = INF, None
    return ResultadoDijkstra(origen, dist, pred, orden, traza)


def ruta_minima(grafo: GrafoPonderado, origen: str, destino: str,
                bloqueados: Iterable[str] = (), contar=None) -> Tuple[Optional[List[str]], float]:
    """Devuelve (ruta, costo). Si no hay ruta: (None, inf)."""
    if destino not in grafo:
        raise ValueError(f"Destino '{destino}' no pertenece a V")
    res = dijkstra(grafo, origen, bloqueados, contar=contar)
    ruta = res.ruta_a(destino)
    return ruta, res.dist[destino]


def todas_las_rutas_minimas(grafo: GrafoPonderado, origen: str, destino: str,
                            bloqueados: Iterable[str] = (), tol: float = 1e-9) -> List[List[str]]:
    """Enumera TODAS las rutas de costo mínimo (útil para detectar empates).

    Usa dist de Dijkstra y el subgrafo de aristas "ajustadas"
    (dist[u] + w(u,v) == dist[v]). El número de rutas mínimas puede ser
    exponencial en el peor caso, por eso esto es solo una herramienta de análisis.
    """
    bloqueados = set(bloqueados)
    res = dijkstra(grafo, origen, bloqueados)
    if destino not in res.dist or res.dist[destino] == INF:
        return []
    preds: Dict[str, List[str]] = {v: [] for v in grafo.vertices}
    for u in grafo.vertices:
        if u in bloqueados or res.dist[u] == INF:
            continue
        for v, w in grafo.vecinos(u):
            if v not in bloqueados and abs(res.dist[u] + w - res.dist[v]) <= tol:
                preds[v].append(u)
    rutas: List[List[str]] = []

    def retroceder(v: str, sufijo: List[str]) -> None:
        if v == origen:
            rutas.append([origen] + sufijo)
            return
        for u in sorted(preds[v]):
            retroceder(u, [v] + sufijo)

    retroceder(destino, [])
    return sorted(rutas)
