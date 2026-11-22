from __future__ import annotations

from collections import deque
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

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


def edmonds_karp(cap: Capacidades, s: str, t: str):
    """Devuelve (valor, flujo por tramo original, lado S del corte mínimo, registro).

    El registro conserva los cambios de capacidad usada y disponible por aumento.
    """
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
                if residual[u][v] > 0 and v not in padre:
                    padre[v] = u
                    cola.append(v)
        if t not in padre:
            break
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


def verificar_flujo(cap: Capacidades, flujo: Dict[Tuple[str, str], int], s: str, t: str) -> int:
    """Verificador O(V + E): capacidad y conservación. Devuelve el valor del flujo."""
    nodos = _validar(cap, s, t)
    balance = {v: 0 for v in nodos}
    for (u, v), f in flujo.items():
        c = cap.get(u, {}).get(v)
        if c is None:
            raise ValueError(f"El flujo usa un tramo inexistente {u}→{v}")
        if f < 0 or f > c:
            raise ValueError(f"Flujo {f} viola la capacidad {c} en {u}→{v}")
        balance[u] -= f
        balance[v] += f
    for v in nodos - {s, t}:
        if balance[v] != 0:
            raise ValueError(f"No se conserva el flujo en {v} (balance {balance[v]})")
    return balance[t]


def capacidad_corte(cap: Capacidades, lado_s: Set[str]) -> int:
    return sum(c for u, vs in cap.items() for v, c in vs.items() if u in lado_s and v not in lado_s)


# Entrada: capacidades del expediente en camiones por día.
tramos = [("Planta", "Quito", 7), ("Planta", "Guayaquil", 5),
          ("Quito", "Clientes", 4), ("Guayaquil", "Clientes", 6),
          ("Quito", "Guayaquil", 2)]
red = capacidades_desde_tramos(tramos)
maximo, flujo, lado_s, registro = edmonds_karp(red, "Planta", "Clientes")
corte = capacidad_corte(red, lado_s)
print("Máximo de camiones/día:", maximo, "| capacidad del corte:", corte)
for aumento in registro:
    print(f"Aumento {aumento['iteracion']}: {' -> '.join(aumento['camino'])} "
          f"| cuello {aumento['cuello']} | total {aumento['total']}")
    for tramo in aumento["tramos"]:
        print(f"  {tramo['accion']} {tramo['tramo']}: "
              f"usado {tramo['usado']}/{tramo['capacidad']} "
              f"| disponible {tramo['disponible']}")

# Pruebas: máximo, corte mínimo, registro completo y destino inalcanzable.
assert maximo == corte == verificar_flujo(red, flujo, "Planta", "Clientes") == 10
assert sum(red["Planta"].values()) == 12
assert [aumento["cuello"] for aumento in registro] == [4, 5, 1]
assert all(tramo["usado"] + tramo["disponible"] == tramo["capacidad"]
           for aumento in registro for tramo in aumento["tramos"])
assert edmonds_karp({"s": {"a": 3}, "a": {}, "t": {}}, "s", "t")[0] == 0

# Caso general donde es necesario cancelar parte de un envío previo.
red_cancelacion = {"s": {"a": 1, "c": 1}, "a": {"b": 1, "e": 1},
                   "b": {"t": 1}, "c": {"b": 1}, "e": {"f": 1},
                   "f": {"t": 1}, "t": {}}
valor, flujo, _, registro = edmonds_karp(red_cancelacion, "s", "t")
assert valor == 2 and flujo[("a", "b")] == 0
assert any(tramo["accion"] == "cancelar"
           for aumento in registro for tramo in aumento["tramos"])
print("Pruebas OK")
