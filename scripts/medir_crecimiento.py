"""Mide tiempos REALES para ilustrar "decidible ≠ resoluble en tiempo útil" (Fase F, c2).

Compara el crecimiento polinómico (Dijkstra) con el factorial/exponencial
(TSP-decisión por enumeración y Held–Karp) y extrapola a tamaños de almacén reales.
Los tiempos dependen de la máquina: el informe debe citarlos como "medidos en Colab".

Uso:  python scripts/medir_crecimiento.py      -> imprime y guarda docs/generado/crecimiento.md
"""

import math
import platform
import random
import time

import _bootstrap  # noqa: F401
from _bootstrap import RAIZ

from logistpulse.casos import c2_tsp_decision as c2
from logistpulse.rutas import GrafoPonderado, dijkstra


def cronometrar(f, *args):
    t0 = time.perf_counter()
    f(*args)
    return time.perf_counter() - t0


def matriz(n, rnd):
    return [[0 if i == j else rnd.randint(1, 50) for j in range(n)] for i in range(n)]


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
