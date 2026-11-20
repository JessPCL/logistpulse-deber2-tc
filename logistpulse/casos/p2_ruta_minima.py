"""p2 · Ruta mínima entre centros de distribución  (Marco Cedeño · Transporte)

Optimización: tiempo mínimo desde CD Quito a cada nodo y ruta a CD Guayaquil.
Decisión asociada (sobre ella se clasifica): RUTA-CORTA = {<G, s, t, K> : existe camino s ⇝ t de costo ≤ K}.
Clase: P (Dijkstra, pesos ≥ 0).  O((V + E) log V) tiempo, O(V + E) espacio.
Para reconstruir la ruta el sistema debe conservar pred[v] (predecesor de cada nodo).

Se incluyen Bellman–Ford y un Dijkstra "sin precondición" solo para mostrar por
qué Dijkstra falla con pesos negativos (pedido explícito del correo).
"""

from __future__ import annotations

import heapq
import math
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from ..rutas.dijkstra import dijkstra, todas_las_rutas_minimas
from ..rutas.grafo import GrafoPonderado

AdyPesos = Dict[str, List[Tuple[str, float]]]


def grafo_desde_tramos(tramos: Iterable[Sequence]) -> GrafoPonderado:
    """Tramos [origen, destino, tiempo] -> grafo DIRIGIDO; valida pesos ≥ 0."""
    return GrafoPonderado.desde_aristas([tuple(t) for t in tramos], dirigido=True)


def resolver(grafo: GrafoPonderado, origen: str, destino: str, contar=None):
    """Devuelve (dist a todos, ruta devuelta, todas las rutas de costo mínimo)."""
    res = dijkstra(grafo, origen, contar=contar)
    if destino not in grafo:
        raise ValueError(f"Destino '{destino}' no pertenece a V")
    return res.dist, res.ruta_a(destino), todas_las_rutas_minimas(grafo, origen, destino)


def decidir(grafo: GrafoPonderado, origen: str, destino: str, K: float) -> bool:
    """Versión de DECISIÓN: ¿existe ruta con costo ≤ K?"""
    dist, _, _ = resolver(grafo, origen, destino)
    return dist[destino] <= K


def dijkstra_sin_precondicion(ady: AdyPesos, s: str) -> Dict[str, float]:
    """Dijkstra estándar SIN validar pesos: un vértice finalizado no se reabre."""
    dist = {v: math.inf for v in ady}
    dist[s] = 0
    heap, fin = [(0, s)], set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in fin:
            continue
        fin.add(u)
        for v, w in ady[u]:
            if v not in fin and d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    return dist


def bellman_ford(ady: AdyPesos, s: str) -> Dict[str, float]:
    """O(V·E). Acepta pesos negativos; detecta ciclos negativos."""
    dist = {v: math.inf for v in ady}
    dist[s] = 0
    for _ in range(len(ady) - 1):
        cambio = False
        for u in ady:
            for v, w in ady[u]:
                if dist[u] + w < dist[v]:
                    dist[v], cambio = dist[u] + w, True
        if not cambio:
            break
    for u in ady:
        for v, w in ady[u]:
            if dist[u] + w < dist[v]:
                raise ValueError("Ciclo de peso negativo alcanzable: no existe distancia mínima")
    return dist
