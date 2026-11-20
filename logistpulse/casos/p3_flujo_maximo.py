"""p3 · Máximo de camiones hacia clientes  (Luis Vaca · Distribución)

Optimización: valor del flujo máximo s→t respetando capacidades.
Decisión asociada (sobre ella se clasifica): FLUJO≥K = {<G, c, s, t, K> : existe flujo factible de valor ≥ K}.
Clase: P (Edmonds–Karp = Ford–Fulkerson eligiendo el camino aumentante más corto con BFS).

Terminación y cota (CLRS 26.2): con caminos más cortos, cada arista residual es
"crítica" a lo sumo |V|/2 veces ⇒ ≤ |V|·|E| aumentos, cada uno con un BFS O(E)
⇒ O(V·E²). La cota NO depende del valor de las capacidades (a diferencia de
Ford–Fulkerson genérico, que con capacidades grandes puede hacer C aumentos).
Espacio O(V + E).

Certificado de OPTIMALIDAD: el corte mínimo (S, T) al terminar; por el teorema
flujo-máximo/corte-mínimo, valor(flujo) = capacidad(corte) ⇒ óptimo.
El registro guarda, por aumento, cómo cambia cada tramo usado (usado/disponible).
"""

from __future__ import annotations

from collections import deque
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

from ..conteo import contador_o_nulo

Capacidades = Dict[str, Dict[str, int]]


def capacidades_desde_tramos(tramos: Iterable[Sequence]) -> Capacidades:
    cap: Capacidades = {}
    for t in tramos:
        if len(t) != 3:
            raise ValueError(f"Tramo inválido {t!r}: debe ser [origen, destino, capacidad]")
        u, v, c = t
        cap.setdefault(u, {})
        cap.setdefault(v, {})
        if v in cap[u]:
            raise ValueError(f"Tramo repetido {u}→{v}")
        cap[u][v] = c
    return cap


def _validar(cap: Capacidades, s: str, t: str) -> Set[str]:
    nodos = set(cap)
    for u, vs in cap.items():
        nodos.update(vs)
        for v, c in vs.items():
            if isinstance(c, bool) or not isinstance(c, int) or c < 0:
                raise ValueError(f"Capacidad inválida en {u}→{v}: {c!r} (entero ≥ 0)")
            if u == v:
                raise ValueError(f"Lazo {u}→{u} no permitido")
            if u in cap.get(v, {}):
                raise ValueError(f"Aristas antiparalelas {u}⇄{v}: agregue un nodo intermedio (CLRS 26.1)")
    if s not in nodos or t not in nodos:
        raise ValueError("s y t deben pertenecer a la red")
    if s == t:
        raise ValueError("s y t deben ser distintos")
    return nodos


def edmonds_karp(cap: Capacidades, s: str, t: str, contar=None):
    """Devuelve (valor, flujo por tramo original, lado S del corte mínimo, registro).

    contar: "aumento" ≤ V·E, "arista" ≤ (aumentos + 1)·2E  ⇒ O(V·E²).
    """
    contar = contador_o_nulo(contar)
    nodos = _validar(cap, s, t)
    residual: Dict[str, Dict[str, int]] = {u: {} for u in nodos}
    flujo: Dict[Tuple[str, str], int] = {}
    for u, vs in cap.items():
        for v, c in vs.items():
            residual[u][v] = c
            residual[v].setdefault(u, 0)  # arista inversa (permite "cancelar" flujo)
            flujo[(u, v)] = 0
    valor, registro = 0, []
    while True:
        padre: Dict[str, Optional[str]] = {s: None}
        cola = deque([s])
        while cola and t not in padre:  # BFS -> camino aumentante con menos aristas
            u = cola.popleft()
            for v in residual[u]:  # orden de inserción (determinista), sin factor log
                contar("arista")
                if residual[u][v] > 0 and v not in padre:
                    padre[v] = u
                    cola.append(v)
        if t not in padre:
            break
        contar("aumento")
        camino, v = [t], t
        while padre[v] is not None:
            v = padre[v]
            camino.append(v)
        camino.reverse()
        cuello = min(residual[u][v] for u, v in zip(camino, camino[1:]))
        tramos = []
        for u, v in zip(camino, camino[1:]):
            residual[u][v] -= cuello
            residual[v][u] += cuello
            if (u, v) in flujo:                       # tramo original: se usa más capacidad
                flujo[(u, v)] += cuello
                orig, accion = (u, v), "usar"
            else:                                     # tramo inverso: se cancela flujo de v→u
                flujo[(v, u)] -= cuello
                orig, accion = (v, u), "cancelar"
            c = cap[orig[0]][orig[1]]
            tramos.append({"tramo": f"{orig[0]}→{orig[1]}", "accion": accion,
                           "usado": flujo[orig], "capacidad": c, "disponible": c - flujo[orig]})
        valor += cuello
        registro.append({"iteracion": len(registro) + 1, "camino": camino, "cuello": cuello,
                         "tramos": tramos, "total": valor})
    lado_s, cola = {s}, deque([s])  # alcanzables en el residual final = lado S del corte
    while cola:
        u = cola.popleft()
        for v, c in residual[u].items():
            if c > 0 and v not in lado_s:
                lado_s.add(v)
                cola.append(v)
    return valor, flujo, lado_s, registro


def verificar_flujo(cap: Capacidades, flujo: Dict[Tuple[str, str], int], s: str, t: str, contar=None) -> int:
    """Verificador O(V + E): capacidad y conservación. Devuelve el valor del flujo."""
    contar = contador_o_nulo(contar)
    nodos = _validar(cap, s, t)
    balance = {v: 0 for v in nodos}
    for (u, v), f in flujo.items():
        contar("paso")
        c = cap.get(u, {}).get(v)
        if c is None:
            raise ValueError(f"El flujo usa un tramo inexistente {u}→{v}")
        if f < 0 or f > c:
            raise ValueError(f"Flujo {f} viola la capacidad {c} en {u}→{v}")
        balance[u] -= f
        balance[v] += f
    for v in nodos - {s, t}:
        contar("paso")
        if balance[v] != 0:
            raise ValueError(f"No se conserva el flujo en {v} (balance {balance[v]})")
    return balance[t]


def capacidad_corte(cap: Capacidades, lado_s: Set[str]) -> int:
    return sum(c for u, vs in cap.items() for v, c in vs.items() if u in lado_s and v not in lado_s)


def decidir(cap: Capacidades, s: str, t: str, K: int) -> bool:
    """Versión de DECISIÓN: ¿se pueden enviar al menos K camiones?"""
    return edmonds_karp(cap, s, t)[0] >= K
