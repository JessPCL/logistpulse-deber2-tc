"""p1 · ¿Puede llegar el envío a la zona Norte?  (Daniela Paredes · Planificación)

Decisión:  ALCANZABILIDAD = {<G, s, t> : G dirigido y existe un camino s ⇝ t}.
Clase: P (algoritmo polinómico conocido: BFS).
Tiempo O(V + E), espacio O(V) con listas de adyacencia.
Solo PROCESAMIENTO: los datos se leen en io_datos y el texto se arma en presentacion_casos.
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from ..conteo import contador_o_nulo
from ..rutas.bfs import alcanzable, bfs_ruta

Red = Dict[str, List[str]]


def red_desde_conexiones(conexiones: Iterable[Sequence[str]], cerrados: Iterable[Sequence[str]] = ()) -> Red:
    """Lista de conexiones del portal -> lista de adyacencia. O(V + E).

    `cerrados` son tramos fuera de servicio (cierre de vías): se omiten.
    """
    conexiones = [tuple(c) for c in conexiones]
    vistos = set()
    for c in conexiones:
        if len(c) != 2 or not all(isinstance(x, str) and x.strip() for x in c):
            raise ValueError(f"Conexión inválida {c!r}: debe ser [origen, destino]")
        if c[0] == c[1]:
            raise ValueError(f"Conexión en lazo {c!r}")
        if c in vistos:
            raise ValueError(f"Conexión repetida {c!r}")
        vistos.add(c)
    cerrados = {tuple(c) for c in cerrados}
    if not cerrados <= vistos:
        raise ValueError(f"Se intenta cerrar un tramo que no existe: {sorted(cerrados - vistos)}")
    red: Red = {}
    for u, v in conexiones:
        red.setdefault(u, [])
        red.setdefault(v, [])
        if (u, v) not in cerrados:
            red[u].append(v)
    return red


def resolver(red: Red, origen: str, destino: str, contar=None, traza=None) -> Optional[List[str]]:
    """Camino con menos tramos o None. O(V + E)."""
    return bfs_ruta(red, origen, destino, contar=contar, traza=traza)


def decidir(red: Red, origen: str, destino: str, contar=None) -> bool:
    return alcanzable(red, origen, destino, contar=contar)


def verificar_camino(red: Red, camino: List[str], origen: str, destino: str, contar=None) -> bool:
    """Verificador O(E + |camino|): conjunto de tramos (O(E)) y una consulta O(1) por tramo."""
    contar = contador_o_nulo(contar)
    if not camino or camino[0] != origen or camino[-1] != destino:
        return False
    tramos = set()
    for u, vs in red.items():
        for v in vs:
            contar("paso")
            tramos.add((u, v))
    for par in zip(camino, camino[1:]):
        contar("paso")
        if par not in tramos:
            return False
    return True
