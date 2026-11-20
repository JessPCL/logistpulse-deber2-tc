"""Grafo ponderado con lista de adyacencia.

Precondición de Dijkstra que se hace cumplir aquí: pesos finitos y NO negativos.
Una arista con peso negativo, NaN o infinito es un dato inválido (ValueError).
"""

from __future__ import annotations

import math
from typing import Dict, Iterable, Iterator, List, Mapping, Optional, Tuple


class GrafoPonderado:
    def __init__(self, dirigido: bool = False) -> None:
        self.dirigido = dirigido
        self._ady: Dict[str, Dict[str, float]] = {}
        self.nombres: Dict[str, str] = {}

    # ----------------------------------------------------------------- construcción
    def agregar_vertice(self, v: str, nombre: str = "") -> None:
        if not isinstance(v, str) or not v.strip():
            raise ValueError(f"Identificador de vértice inválido: {v!r}")
        self._ady.setdefault(v, {})
        if nombre:
            self.nombres[v] = nombre

    def agregar_arista(self, u: str, v: str, peso: float) -> None:
        if isinstance(peso, bool) or not isinstance(peso, (int, float)):
            raise ValueError(f"Peso no numérico en ({u},{v}): {peso!r}")
        if math.isnan(peso) or math.isinf(peso):
            raise ValueError(f"Peso no finito en ({u},{v}): {peso!r}")
        if peso < 0:
            raise ValueError(f"Peso negativo en ({u},{v}) = {peso}: Dijkstra exige pesos ≥ 0")
        if u == v:
            raise ValueError(f"Lazo ({u},{u}) no permitido en la planta")
        for w in (u, v):
            if w not in self._ady:
                self.agregar_vertice(w)
        if v in self._ady[u]:
            raise ValueError(f"Arista duplicada ({u},{v})")
        self._ady[u][v] = peso
        if not self.dirigido:
            self._ady[v][u] = peso

    @classmethod
    def desde_aristas(cls, aristas: Iterable[Tuple[str, str, float]], dirigido: bool = False,
                      vertices: Iterable[str] = ()) -> "GrafoPonderado":
        g = cls(dirigido)
        for v in vertices:
            g.agregar_vertice(v)
        for u, v, w in aristas:
            g.agregar_arista(u, v, w)
        return g

    # ----------------------------------------------------------------- consultas
    @property
    def vertices(self) -> List[str]:
        return sorted(self._ady)

    def __contains__(self, v: object) -> bool:
        return v in self._ady

    def vecinos(self, u: str) -> Iterator[Tuple[str, float]]:
        """Vecinos en orden alfabético (hace la ejecución reproducible)."""
        for v in sorted(self._ady[u]):
            yield v, self._ady[u][v]

    def peso(self, u: str, v: str) -> Optional[float]:
        return self._ady.get(u, {}).get(v)

    @property
    def num_vertices(self) -> int:
        return len(self._ady)

    @property
    def num_aristas(self) -> int:
        total = sum(len(n) for n in self._ady.values())
        return total if self.dirigido else total // 2

    def aristas(self) -> List[Tuple[str, str, float]]:
        out = []
        for u in sorted(self._ady):
            for v, w in self.vecinos(u):
                if self.dirigido or u < v:
                    out.append((u, v, w))
        return out

    def como_lista_adyacencia(self) -> Dict[str, List[str]]:
        return {u: [v for v, _ in self.vecinos(u)] for u in self.vertices}

    def costo_ruta(self, ruta: List[str]) -> float:
        """Verifica que la ruta use aristas existentes y devuelve su costo."""
        if not ruta:
            raise ValueError("Ruta vacía")
        total = 0.0
        for u, v in zip(ruta, ruta[1:]):
            w = self.peso(u, v)
            if w is None:
                raise ValueError(f"La arista ({u},{v}) no existe")
            total += w
        return total
