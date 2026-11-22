"""c1 · ¿Hay una asignación que cumpla todas las reglas?  (Mónica Ruiz · Planificación)

Decisión: DESPACHO-SAT = {<φ> : φ es una fórmula CNF de reglas de despacho satisfacible}.
Representación: variable i ↔ "vehículo/franja i asignado"; cláusula ↔ regla;
literal +i / −i.  n = nº de variables, m = nº de cláusulas, k = literales por cláusula.

∈ NP: certificado = asignación (n bits); verificador O(m·k).
NP-difícil: 3-SAT ≤p DESPACHO-SAT con la reducción IDENTIDAD (toda fórmula 3-CNF es
un conjunto válido de reglas). 3-SAT es NP-completo (Cook 1971; Karp 1972).
Algoritmos: fuerza bruta O(2ⁿ·m·k); DPLL (propagación unitaria + literal puro)
O(2ⁿ·n·m·k) en el peor caso (mucho mejor en la práctica, pero sigue siendo exponencial).

¡OJO! La instancia del simulador (x1∨¬x2) ∧ (x2∨x3) es 2-CNF: 2-SAT está en P
(grafo de implicaciones + componentes fuertemente conexas, O(n + m)). Que la
INSTANCIA sea fácil no cambia la clase del PROBLEMA GENERAL (3-CNF).
"""

from __future__ import annotations

from itertools import product
from typing import Dict, List, Optional, Sequence

from ..conteo import contador_o_nulo

Clausulas = Sequence[Sequence[int]]
Asignacion = Dict[int, bool]


def validar(clausulas: Clausulas, n: int) -> None:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError("n debe ser entero ≥ 0")
    for i, c in enumerate(clausulas):
        if len(c) == 0:
            raise ValueError(f"La cláusula #{i} está vacía")
        for lit in c:
            if isinstance(lit, bool) or not isinstance(lit, int) or lit == 0 or abs(lit) > n:
                raise ValueError(f"Literal inválido {lit!r} en la cláusula #{i} (use ±1..±{n})")


def verificar(clausulas: Clausulas, asignacion: Asignacion, contar=None) -> bool:
    """Verificador polinómico O(m·k) ("literal" ≤ m·k): cada cláusula tiene un literal verdadero."""
    contar = contador_o_nulo(contar)
    for c in clausulas:
        satisfecha = False
        for l in c:
            contar("literal")
            if asignacion[abs(l)] == (l > 0):
                satisfecha = True
                break
        if not satisfecha:
            return False
    return True


def verificar_detalle(clausulas: Clausulas, asignacion: Asignacion) -> List[Optional[int]]:
    """Comprobación independiente CLÁUSULA POR CLÁUSULA (lo que pide el correo c1).

    Devuelve, para cada cláusula, el primer literal que la hace verdadera, o None si la
    asignación la incumple. La asignación es válida ⇔ ningún elemento es None. O(m·k).
    """
    detalle: List[Optional[int]] = []
    for c in clausulas:
        detalle.append(next((l for l in c if asignacion[abs(l)] == (l > 0)), None))
    return detalle


def fuerza_bruta(clausulas: Clausulas, n: int, contar=None) -> Optional[Asignacion]:
    """Enumera las 2ⁿ asignaciones ("asignacion" ≤ 2ⁿ): O(2ⁿ·m·k)."""
    contar = contador_o_nulo(contar)
    validar(clausulas, n)
    for bits in product([False, True], repeat=n):
        contar("asignacion")
        a = {i + 1: bits[i] for i in range(n)}
        if verificar(clausulas, a):
            return a
    return None


def dpll(clausulas: Clausulas, n: int, contar=None) -> Optional[Asignacion]:
    """DPLL con propagación unitaria y literal puro. Exacto.

    Peor caso: árbol de ≤ 2^(n+1) nodos; en cada nodo la propagación unitaria hace
    ≤ n rondas de O(m·k) ⇒ O(2ⁿ·n·m·k) tiempo, O(n·m·k) espacio (una copia por nivel).
    """
    contar = contador_o_nulo(contar)
    validar(clausulas, n)
    resultado = _dpll([list(dict.fromkeys(c)) for c in clausulas], {}, contar)
    if resultado is None:
        return None
    return {i: resultado.get(i, False) for i in range(1, n + 1)}


def _simplificar(clausulas: List[List[int]], lit: int) -> Optional[List[List[int]]]:
    nuevas = []
    for c in clausulas:
        if lit in c:
            continue  # cláusula satisfecha
        resto = [l for l in c if l != -lit]
        if not resto:
            return None  # conflicto: cláusula vacía
        nuevas.append(resto)
    return nuevas


def _dpll(clausulas: List[List[int]], asig: Dict[int, bool], contar) -> Optional[Dict[int, bool]]:
    contar("nodo")  # nodos del árbol de búsqueda ≤ 2^(n+1)
    asig = dict(asig)
    while True:  # propagación unitaria
        unit = next((c[0] for c in clausulas if len(c) == 1), None)
        if unit is None:
            break
        asig[abs(unit)] = unit > 0
        clausulas = _simplificar(clausulas, unit)
        if clausulas is None:
            return None
    literales = {l for c in clausulas for l in c}
    for l in list(literales):  # literal puro
        if -l not in literales:
            asig[abs(l)] = l > 0
            clausulas = _simplificar(clausulas, l)
            if clausulas is None:
                return None
    if not clausulas:
        return asig
    var = abs(clausulas[0][0])  # ramificación
    for lit in (var, -var):
        reducidas = _simplificar(clausulas, lit)
        if reducidas is not None:
            r = _dpll(reducidas, {**asig, var: lit > 0}, contar)
            if r is not None:
                return r
    return None


# ------------------------------------------------------------------ 2-SAT en tiempo lineal
def es_2cnf(clausulas: Clausulas) -> bool:
    return all(len(c) <= 2 for c in clausulas)


def dos_sat(clausulas: Clausulas, n: int, contar=None) -> Optional[Asignacion]:
    """2-SAT en O(n + m): grafo de implicaciones (¬a→b, ¬b→a) + Kosaraju iterativo."""
    contar = contador_o_nulo(contar)
    validar(clausulas, n)
    if not es_2cnf(clausulas):
        raise ValueError("dos_sat solo acepta cláusulas de a lo sumo 2 literales")
    idx = lambda l: 2 * (abs(l) - 1) + (0 if l > 0 else 1)  # nodo de cada literal
    N = 2 * n
    ady = [[] for _ in range(N)]
    radj = [[] for _ in range(N)]
    for c in clausulas:
        a, b = (c[0], c[0]) if len(c) == 1 else (c[0], c[1])
        for x, y in ((-a, b), (-b, a)):
            ady[idx(x)].append(idx(y))
            radj[idx(y)].append(idx(x))
    orden, visto = [], [False] * N
    for s in range(N):  # 1ª pasada: orden de finalización
        if visto[s]:
            continue
        pila = [(s, 0)]
        visto[s] = True
        while pila:
            u, i = pila.pop()
            contar("paso")
            if i < len(ady[u]):
                pila.append((u, i + 1))
                v = ady[u][i]
                if not visto[v]:
                    visto[v] = True
                    pila.append((v, 0))
            else:
                orden.append(u)
    comp, c_id = [-1] * N, 0
    for s in reversed(orden):  # 2ª pasada en el grafo transpuesto
        if comp[s] != -1:
            continue
        pila = [s]
        comp[s] = c_id
        while pila:
            u = pila.pop()
            contar("paso")
            for v in radj[u]:
                contar("paso")
                if comp[v] == -1:
                    comp[v] = c_id
                    pila.append(v)
        c_id += 1
    asig = {}
    for i in range(1, n + 1):
        pos, neg = comp[idx(i)], comp[idx(-i)]
        if pos == neg:
            return None  # x y ¬x en la misma CFC
        asig[i] = pos > neg  # orden topológico de Kosaraju
    return asig
