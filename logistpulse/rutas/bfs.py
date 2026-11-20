"""BFS: camino con MENOR NÚMERO DE ARISTAS (ignora pesos).

Sirve cuando las aristas no tienen peso (o todas pesan lo mismo) y para el
problema de alcanzabilidad (caso p1).

Terminación: cada vértice entra a la cola a lo sumo una vez (se marca al
descubrirlo), así que hay ≤ |V| extracciones y cada lista de adyacencia se
recorre una vez. Complejidad: O(|V| + |E|) tiempo, O(|V|) espacio.
Los vecinos se recorren en el orden de la lista (determinista); NO se ordenan
dentro del bucle para no agregar un factor log a la cota.
"""

from __future__ import annotations

from collections import deque
from typing import Dict, Iterable, List, Mapping, Optional

from ..conteo import contador_o_nulo

AdyacenciaSimple = Mapping[str, Iterable[str]]


def _vertices(ady: AdyacenciaSimple) -> set:
    vs = set(ady)
    for u, vecinos in ady.items():
        vs.update(vecinos)
    return vs


def bfs_ruta(ady: AdyacenciaSimple, origen: str, destino: str,
             bloqueados: Iterable[str] = (), contar=None,
             traza: Optional[List[dict]] = None) -> Optional[List[str]]:
    """Ruta con menos tramos de origen a destino, o None si no es alcanzable.

    contar: Contador opcional ("extraccion" ≤ V, "arista" ≤ E).
    traza : lista opcional; se agrega {"sale", "entran", "cola"} por cada extracción
            (sirve para la tabla "BFS por niveles" del informe).
    """
    contar = contador_o_nulo(contar)
    vs = _vertices(ady)
    for nombre, v in (("origen", origen), ("destino", destino)):
        if v not in vs:
            raise ValueError(f"El {nombre} '{v}' no pertenece al grafo")
    bloqueados = set(bloqueados)
    if origen in bloqueados:
        raise ValueError(f"El origen '{origen}' está bloqueado")
    if destino in bloqueados:
        return None
    padre: Dict[str, Optional[str]] = {origen: None}
    cola = deque([origen])
    while cola:
        u = cola.popleft()
        contar("extraccion")
        if u == destino:
            if traza is not None:
                traza.append({"sale": u, "entran": [], "cola": list(cola), "destino": True})
            ruta = []
            while u is not None:
                ruta.append(u)
                u = padre[u]
            return ruta[::-1]
        entran = []
        for v in ady.get(u, []):  # orden de la lista (determinista); ordenar costaría O(d log d)
            contar("arista")
            if v not in padre and v not in bloqueados:
                padre[v] = u
                cola.append(v)
                entran.append(v)
        if traza is not None:
            traza.append({"sale": u, "entran": entran, "cola": list(cola), "destino": False})
    return None


def alcanzable(ady: AdyacenciaSimple, origen: str, destino: str, bloqueados: Iterable[str] = (),
               contar=None) -> bool:
    """Versión de DECISIÓN (Sí/No) del problema de alcanzabilidad."""
    return bfs_ruta(ady, origen, destino, bloqueados, contar) is not None
