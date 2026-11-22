"""Mide tiempos REALES para ilustrar "decidible ≠ resoluble en tiempo útil" (Fase F, c1, c2 y c3).

Compara el crecimiento polinómico (Dijkstra) con el factorial/exponencial
(TSP-decisión por enumeración y Held–Karp) y extrapola a tamaños reales de la operación.
Los tiempos dependen de la máquina: el informe debe citarlos como "medidos en Colab".

Uso:  python scripts/medir_crecimiento.py      -> imprime y guarda docs/generado/crecimiento.md
"""

import math
import platform
import random
import statistics
import time

import _bootstrap  # noqa: F401
from _bootstrap import RAIZ

from logistpulse.casos import c1_sat as c1
from logistpulse.casos import c2_tsp_decision as c2
from logistpulse.casos import c3_vertex_cover as c3
from logistpulse.conteo import Contador
from logistpulse.rutas import GrafoPonderado, dijkstra


def cronometrar(f, *args):
    t0 = time.perf_counter()
    f(*args)
    return time.perf_counter() - t0


def matriz(n, rnd):
    return [[0 if i == j else rnd.randint(1, 50) for j in range(n)] for i in range(n)]


def anios(seg: float) -> str:
    return f"{seg:.2e} s ≈ {seg / 3.156e7:.2e} años"


def seccion_sat(rnd) -> list:
    """c1: fuerza bruta (peor caso: fórmula insatisfacible ⇒ revisa las 2ⁿ) y DPLL en 3-CNF aleatoria difícil."""
    base = [[a * 1, b * 2, c * 3] for a in (1, -1) for b in (1, -1) for c in (1, -1)]  # insatisfacible
    lineas = ["## SAT (c1): fuerza bruta en el peor caso (respuesta No) y DPLL", "",
              "| n variables | asignaciones 2ⁿ | fuerza bruta (s) |", "|---|---|---|"]
    por_asig = None
    for n in (12, 14, 16, 18):
        t = cronometrar(c1.fuerza_bruta, base, n)
        por_asig = t / 2 ** n
        lineas.append(f"| {n} | {2 ** n:,} | {t:.3f} |")
        print(lineas[-1])
    lineas += ["", "### Extrapolación de la fuerza bruta (con el costo por asignación medido en n = 18)", "",
               "| n variables | asignaciones | tiempo estimado |", "|---|---|---|"]
    for n in (30, 40, 60, 100):
        lineas.append(f"| {n} | {2 ** n:.2e} | {anios(2 ** n * por_asig)} |")
    lineas += ["", "### DPLL en 3-CNF aleatorias con m ≈ 4,26·n (la zona más difícil); mediana de 5 fórmulas", "",
               "| n variables | m cláusulas | nodos del árbol | tiempo (s) |", "|---|---|---|---|"]
    for n in (20, 40, 60, 80):
        m = round(4.26 * n)
        nodos, tiempos = [], []
        for _ in range(5):
            cl = [[rnd.choice((1, -1)) * v for v in rnd.sample(range(1, n + 1), 3)] for _ in range(m)]
            c = Contador()
            t0 = time.perf_counter()
            c1.dpll(cl, n, contar=c)
            tiempos.append(time.perf_counter() - t0)
            nodos.append(c["nodo"])
        lineas.append(f"| {n} | {m} | {int(statistics.median(nodos)):,} | {statistics.median(tiempos):.3f} |")
        print(lineas[-1])
    lineas += ["", "Conclusión: SAT es **decidible** (hay 2ⁿ asignaciones finitas), pero la fuerza bruta se duplica con cada "
               "variable extra: con 60 decisiones de despacho ya serían siglos. DPLL poda mucho y llega más lejos, "
               "pero sus nodos también crecen de forma exponencial con n.", ""]
    return lineas


def seccion_vertex_cover() -> list:
    """c3: ramificación en el peor caso (k+1 aristas disjuntas con presupuesto k ⇒ No, árbol completo)."""
    lineas = ["## Vertex Cover (c3): ramificación en el peor caso (respuesta No) y 2-aproximación", "",
              "| k equipos | nodos 2^(k+1)−1 | ramificación (s) |", "|---|---|---|"]
    por_nodo = None
    for k in (10, 12, 14, 16):
        ady = {}
        for i in range(k + 1):  # k + 1 pares de zonas disjuntos: con k equipos no alcanza
            ady[f"a{i}"], ady[f"b{i}"] = [f"b{i}"], [f"a{i}"]
        c = Contador()
        t0 = time.perf_counter()
        c3.ramificacion(ady, k, contar=c)
        t = time.perf_counter() - t0
        por_nodo = t / c["nodo"]
        lineas.append(f"| {k} | {c['nodo']:,} | {t:.3f} |")
        print(lineas[-1])
    lineas += ["", "### Extrapolación de la ramificación (con el costo por nodo medido en k = 16)", "",
               "| k equipos | nodos | tiempo estimado |", "|---|---|---|"]
    for k in (30, 40, 60, 100):
        lineas.append(f"| {k} | {2 ** (k + 1) - 1:.2e} | {anios((2 ** (k + 1) - 1) * por_nodo)} |")
    V = 100_000
    ady = {f"v{i}": [] for i in range(V)}
    for i in range(V - 1):  # camino de 100 000 zonas
        ady[f"v{i}"].append(f"v{i + 1}")
        ady[f"v{i + 1}"].append(f"v{i}")
    t = cronometrar(c3.aproximacion_2, ady)
    lineas += ["", f"2-aproximación en un camino de {V:,} zonas: {t:.3f} s (O(V + E), garantiza |S| ≤ 2·ÓPTIMO).", "",
               "Conclusión: con pocos equipos (k pequeño) la ramificación exacta es rápida aunque haya muchas zonas; "
               "el costo explota con k (cada equipo extra duplica el árbol). Para k grandes se usa la 2-aproximación, "
               "que es instantánea pero puede usar hasta el doble de equipos.", ""]
    return lineas


def main() -> None:
    rnd = random.Random(2026)
    lineas = ["# Crecimiento medido (tiempos reales)", "",
              f"_Máquina: {platform.python_implementation()} {platform.python_version()} · {platform.machine()}. "
              "Los valores cambian según el equipo; lo que importa es la forma del crecimiento._", "",
              "## TSP-decisión (c2): enumeración (peor caso, respuesta No) vs Held–Karp vs vecino más cercano", "",
              "| n centros | tours (n−1)! | enumeración (s) | Held–Karp (s) | vecino más cercano (s) |", "|---|---|---|---|---|"]
    por_tour = None
    for n in range(4, 11):
        D = matriz(n, rnd)
        t_enum = cronometrar(c2.decidir, D, -1)  # L = −1 obliga a revisar TODOS los tours
        t_hk = cronometrar(c2.held_karp, D)
        t_nn = cronometrar(c2.vecino_mas_cercano, D)
        tours = math.factorial(n - 1)
        por_tour = t_enum / tours
        lineas.append(f"| {n} | {tours:,} | {t_enum:.4f} | {t_hk:.4f} | {t_nn:.6f} |")
        print(lineas[-1])
    for n in (12, 14):
        D = matriz(n, rnd)
        t_hk = cronometrar(c2.held_karp, D)
        lineas.append(f"| {n} | {math.factorial(n - 1):,} | (no se ejecuta) | {t_hk:.3f} | — |")
        print(lineas[-1])

    lineas += ["", "### Extrapolación de la enumeración (con el costo por tour medido en n = 10)", "",
               "| n centros | tours | tiempo estimado |", "|---|---|---|"]
    for n in (12, 15, 20, 25):
        seg = math.factorial(n - 1) * por_tour
        lineas.append(f"| {n} | {math.factorial(n - 1):.2e} | {seg:.2e} s ≈ {seg / 3.156e7:.2e} años |")
    lineas += ["", "Conclusión: TSP-DEC es **decidible** para todo n (la enumeración termina), pero con 20–25 centros "
               "la búsqueda exhaustiva tarda de miles a miles de millones de años (ver tabla). Held–Karp (O(n²·2ⁿ)) aleja el límite, "
               "pero sigue siendo exponencial; la heurística es instantánea y no garantiza el óptimo.", ""]

    lineas += seccion_sat(rnd) + seccion_vertex_cover()

    lineas += ["## Dijkstra (polinómico) en grafos aleatorios con E ≈ 4V", "",
               "| V | E | tiempo (s) |", "|---|---|---|"]
    for V in (1_000, 10_000, 50_000):
        g = GrafoPonderado(dirigido=True)
        for i in range(V):
            g.agregar_vertice(f"v{i}")
        for i in range(V):
            for j in rnd.sample(range(V), 4):
                if j != i and g.peso(f"v{i}", f"v{j}") is None:
                    g.agregar_arista(f"v{i}", f"v{j}", rnd.randint(1, 100))
        t = cronometrar(dijkstra, g, "v0")
        lineas.append(f"| {V:,} | {g.num_aristas:,} | {t:.3f} |")
        print(lineas[-1])
    lineas += ["", "Conclusión: con 50 000 ubicaciones Dijkstra sigue respondiendo en segundos: "
               "O((V+E) log V) es resoluble en tiempo útil.", ""]

    salida = RAIZ / "docs" / "generado" / "crecimiento.md"
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text("\n".join(lineas), encoding="utf-8")
    print(f"OK {salida.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
