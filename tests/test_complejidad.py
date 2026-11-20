"""Pruebas de COMPLEJIDAD: atan cada Big-O del informe al código real.

Dos tipos de prueba:
1. TestConteoOperaciones (principal, determinista): cada algoritmo cuenta su
   operación dominante y se compara con la cota teórica en instancias de
   tamaño creciente. No depende de la máquina, así que no falla por azar.
2. TestTiemposReales (complementaria): mide segundos con time.perf_counter y
   comprueba que, al aumentar la entrada, el tiempo crezca en la PROPORCIÓN que
   predice la cota (con tolerancias amplias, porque el reloj tiene ruido).
   Si Colab está muy cargado y fallara por ruido, se puede desactivar con la
   variable de entorno LOGISTPULSE_SIN_TIEMPOS=1 (las de conteo siguen valiendo).
"""

import math
import os
import random
import time
import unittest
from datetime import date, timedelta

from logistpulse.automatas import ORDEN_COMPRA
from logistpulse.casos import (c1_sat, c2_tsp_decision, c3_vertex_cover, n1_isomorfismo, n2_factor_rango,
                               n3_log_discreto, n4_automorfismo, p1_alcanzabilidad, p3_flujo_maximo)
from logistpulse.conteo import Contador
from logistpulse.inventario import EstadoSKU, Lote, seleccionar_fefo, sugerencias
from logistpulse.rutas import GrafoPonderado, bfs_ruta, dijkstra


# ----------------------------------------------------------------------------- generadores
def grafo_aleatorio(V: int, grado: int, rnd: random.Random, dirigido=True) -> GrafoPonderado:
    g = GrafoPonderado(dirigido=dirigido)
    for i in range(V):
        g.agregar_vertice(f"v{i}")
    for i in range(V):
        for j in rnd.sample(range(V), grado):
            if j != i and g.peso(f"v{i}", f"v{j}") is None and g.peso(f"v{j}", f"v{i}") is None:
                g.agregar_arista(f"v{i}", f"v{j}", rnd.randint(1, 100))
    return g


def entradas_adyacencia(g: GrafoPonderado) -> int:
    """E⃗ = número de entradas en las listas de adyacencia (E si es dirigido, 2E si no)."""
    return sum(1 for u in g.vertices for _ in g.vecinos(u))


def red_flujo(V: int, rnd: random.Random, escala: int = 1):
    """Red en capas sin aristas antiparalelas; capacidades aleatorias × escala."""
    cap = {f"n{i}": {} for i in range(V)}
    for i in range(V - 1):
        for j in rnd.sample(range(i + 1, V), min(3, V - i - 1)):
            cap[f"n{i}"][f"n{j}"] = rnd.randint(1, 20) * escala
    return cap


def primo_menor_que(n: int) -> int:
    while not n3_log_discreto.es_primo(n):
        n -= 1
    return n


class TestConteoOperaciones(unittest.TestCase):
    # ------------------------------------------------------------------ lineales
    def test_afd_un_paso_por_simbolo(self):
        for n_parciales in (1, 10, 100, 1000):
            cadena = "sae" + "p" * n_parciales + "f"
            c = Contador()
            self.assertTrue(ORDEN_COMPRA.ejecutar(cadena, contar=c).aceptada)
            self.assertEqual(c["paso"], len(cadena))  # O(n) exacto

    def test_bfs_es_O_V_mas_E(self):
        rnd = random.Random(1)
        for V in (100, 1000, 5000):
            g = grafo_aleatorio(V, 4, rnd)
            ady = g.como_lista_adyacencia()
            c = Contador()
            bfs_ruta(ady, "v0", f"v{V - 1}", contar=c)
            self.assertLessEqual(c["extraccion"], V)
            self.assertLessEqual(c["arista"], entradas_adyacencia(g))

    def test_dijkstra_operaciones_de_heap_acotadas(self):
        rnd = random.Random(2)
        for V in (100, 1000, 5000):
            for dirigido in (True, False):
                g = grafo_aleatorio(V, 4, rnd, dirigido)
                E = entradas_adyacencia(g)
                c = Contador()
                dijkstra(g, "v0", contar=c)
                self.assertLessEqual(c["insercion"], E + 1)          # inserción perezosa
                self.assertLessEqual(c["extraccion"], c["insercion"])
                self.assertLessEqual(c["arista"], E)
                # cada operación de heap cuesta O(log(tamaño del heap)) ≤ O(log V²) = O(log V)
                costo = (c["insercion"] + c["extraccion"]) * math.log2(E + 2) + c["arista"]
                self.assertLessEqual(costo, 3 * (V + E) * math.log2(V + 2))

    def test_verificadores_polinomicos(self):
        rnd = random.Random(3)
        for n in (10, 100, 1000):  # c2: O(n)
            D = [[0 if i == j else 1 for j in range(n)] for i in range(n)]
            tour = (0,) + tuple(rnd.sample(range(1, n), n - 1)) + (0,)
            c = Contador()
            self.assertTrue(c2_tsp_decision.verificar(D, n, tour, contar=c))
            self.assertLessEqual(c["paso"], 2 * n)
        for n in (10, 50, 200):  # c3: O(V + E)
            ady = c3_vertex_cover.estrella(n)
            c = Contador()
            c3_vertex_cover.verificar(ady, 1, {"centro"}, contar=c)
            self.assertLessEqual(c["paso"], 3 * n + 1)
        for m in (10, 100, 1000):  # c1: O(m·k)
            cl = [[rnd.choice((1, -1)) * v for v in rnd.sample(range(1, 21), 3)] for _ in range(m)]
            c = Contador()
            c1_sat.verificar(cl, {i: True for i in range(1, 21)}, contar=c)
            self.assertLessEqual(c["literal"], 3 * m)
        for n in (5, 20, 60):  # n1: O(n²)
            M = n1_isomorfismo.ciclo(n)
            c = Contador()
            self.assertTrue(n1_isomorfismo.verificar(M, M, tuple(range(n)), contar=c))
            self.assertEqual(c["comparacion"], n * n)
        c = Contador()
        n2_factor_rango.verificar(2 ** 61 - 1, 2 ** 40, 3, contar=c)  # n2: UNA división
        self.assertEqual(c["division"], 1)
        p = primo_menor_que(2 ** 61)
        for B in (10, 10 ** 6, 10 ** 15):  # n3: ≤ 2·bits(x) multiplicaciones
            c = Contador()
            n3_log_discreto.verificar(p, 3, pow(3, B, p), B, B, contar=c)
            self.assertLessEqual(c["multiplicacion"], 2 * B.bit_length())

    def test_fefo_O_L_log_L_y_reposicion_O_P(self):
        rnd = random.Random(4)
        hoy = date(2026, 11, 20)
        for L in (10, 100, 1000, 5000):
            lotes = [Lote(f"L{i:05d}", "S", hoy + timedelta(days=rnd.randint(1, 60)), rnd.randint(1, 9)) for i in range(L)]
            c = Contador()
            seleccionar_fefo(lotes, "S", 10 ** 9, hoy, contar=c)
            self.assertLessEqual(c["comparacion"], L * math.ceil(math.log2(L)) + L)
            self.assertLessEqual(c["lote"], 2 * L)
        for P in (10, 1000):
            c = Contador()
            list(sugerencias((EstadoSKU(f"S{i}", 5, 0, 0, 10, 20) for i in range(P)), contar=c))
            self.assertEqual(c["sku"], P)

    # ------------------------------------------------------------------ polinómicos no lineales
    def test_edmonds_karp_cota_independiente_de_las_capacidades(self):
        rnd = random.Random(5)
        for V in (10, 30, 60):
            semilla = rnd.randint(0, 10 ** 6)
            cap1 = red_flujo(V, random.Random(semilla), escala=1)
            cap2 = red_flujo(V, random.Random(semilla), escala=10 ** 6)  # mismas aristas, capacidades × 10⁶
            E = sum(len(vs) for vs in cap1.values())
            c1, c2 = Contador(), Contador()
            v1 = p3_flujo_maximo.edmonds_karp(cap1, "n0", f"n{V - 1}", contar=c1)[0]
            v2 = p3_flujo_maximo.edmonds_karp(cap2, "n0", f"n{V - 1}", contar=c2)[0]
            self.assertEqual(v2, v1 * 10 ** 6)
            self.assertEqual(c1["aumento"], c2["aumento"])       # NO depende del valor de las capacidades
            self.assertLessEqual(c1["aumento"], V * E)            # ≤ V·E aumentos
            self.assertLessEqual(c1["arista"], (c1["aumento"] + 1) * 2 * E)  # ⇒ O(V·E²)

    # ------------------------------------------------------------------ exponenciales / factoriales
    def test_enumeracion_tsp_es_factorial(self):
        rnd = random.Random(6)
        previo = None
        for n in range(3, 9):
            D = [[0 if i == j else rnd.randint(1, 9) for j in range(n)] for i in range(n)]
            c = Contador()
            self.assertIsNone(c2_tsp_decision.decidir(D, -1, contar=c))  # L = −1: peor caso, respuesta No
            self.assertEqual(c["tour"], math.factorial(n - 1))
            if previo:
                self.assertEqual(c["tour"] // previo, n - 1)  # crece ×(n−1) al agregar un centro
            previo = c["tour"]

    def test_held_karp_es_n2_por_2n(self):
        rnd = random.Random(7)
        for n in range(3, 13):
            D = [[0 if i == j else rnd.randint(1, 9) for j in range(n)] for i in range(n)]
            c = Contador()
            c2_tsp_decision.held_karp(D, contar=c)
            self.assertLessEqual(c["transicion"], n * n * 2 ** n)        # cota superior O(n²·2ⁿ)
            self.assertGreaterEqual(c["transicion"], 2 ** (n - 1))      # y sigue siendo exponencial

    def test_heuristica_vecino_mas_cercano_es_cuadratica(self):
        for n in (10, 100, 300):
            D = [[abs(i - j) for j in range(n)] for i in range(n)]
            c = Contador()
            c2_tsp_decision.vecino_mas_cercano(D, contar=c)
            self.assertLessEqual(c["comparacion"], n * n)

    def test_factor_rango_exponencial_en_bits(self):
        """Peor caso (N primo, B = N−1): las divisiones se DUPLICAN con cada bit extra."""
        conteos = []
        for bits in range(8, 17):
            N = primo_menor_que(2 ** bits)
            c = Contador()
            self.assertIsNone(n2_factor_rango.resolver(N, N - 1, contar=c))
            self.assertEqual(c["division"], N - 2)
            conteos.append(c["division"])
        for a, b in zip(conteos, conteos[1:]):
            self.assertTrue(1.6 <= b / a <= 2.4, (a, b))

    def test_log_discreto_lineal_en_B_y_bsgs_en_raiz(self):
        p = 1_000_003
        g = 2
        for B in (100, 10_000, 1_000_000):
            h = pow(g, B + 7, p)  # fuera del rango -> peor caso para la búsqueda lineal
            cl, cb = Contador(), Contador()
            n3_log_discreto.resolver(p, g, h, B, contar=cl)
            n3_log_discreto.baby_step_giant_step(p, g, h, B, contar=cb)
            self.assertLessEqual(cl["multiplicacion"], B + 1)
            self.assertLessEqual(cb["multiplicacion"], 2 * (math.isqrt(B) + 2))

    def test_permutaciones_factoriales(self):
        """Mismos grados y no isomorfos (C_n vs C_3 ∪ C_{n−3}): la búsqueda agota las n! permutaciones."""
        for n in (6, 7):
            c = Contador()
            self.assertIsNone(n1_isomorfismo.resolver(n1_isomorfismo.ciclo(n),
                                                      n1_isomorfismo.union_de_ciclos(3, n - 3), contar=c))
            self.assertEqual(c["permutacion"], math.factorial(n))
        G = [[0] * 6 for _ in range(6)]
        for a, b in [(0, 1), (1, 2), (2, 3), (3, 4), (5, 1), (5, 2)]:
            G[a][b] = G[b][a] = 1
        c = Contador()
        n4_automorfismo.resolver(G, contar=c)
        self.assertEqual(c["permutacion"], math.factorial(6))  # el "No" agota n!

    def test_vertex_cover_ramificacion_2_a_la_k(self):
        rnd = random.Random(8)
        for _ in range(60):
            n = rnd.randint(3, 12)
            ady = {f"v{i}": [] for i in range(n)}
            for i in range(n):
                for j in range(i + 1, n):
                    if rnd.random() < 0.3:
                        ady[f"v{i}"].append(f"v{j}")
                        ady[f"v{j}"].append(f"v{i}")
            for k in range(0, 6):
                c = Contador()
                c3_vertex_cover.ramificacion(ady, k, contar=c)
                self.assertLessEqual(c["nodo"], 2 ** (k + 1) - 1)

    def test_sat_fuerza_bruta_2n_y_dpll_acotado(self):
        rnd = random.Random(9)
        for n in range(3, 11):
            cl = [[a * 1, b * 2, c_ * 3] for a in (1, -1) for b in (1, -1) for c_ in (1, -1)]  # insatisfacible
            cl += [[rnd.choice((1, -1)) * v for v in rnd.sample(range(1, n + 1), 3)] for _ in range(2 * n)]
            cf, cd = Contador(), Contador()
            self.assertIsNone(c1_sat.fuerza_bruta(cl, n, contar=cf))
            self.assertIsNone(c1_sat.dpll(cl, n, contar=cd))
            self.assertEqual(cf["asignacion"], 2 ** n)       # el "No" de fuerza bruta revisa las 2ⁿ
            self.assertLessEqual(cd["nodo"], 2 ** (n + 1))   # DPLL: árbol con ≤ 2^(n+1) nodos

    def test_dos_sat_lineal(self):
        rnd = random.Random(10)
        for n in (10, 100, 1000):
            m = 3 * n
            cl = [[rnd.choice((1, -1)) * rnd.randint(1, n), rnd.choice((1, -1)) * rnd.randint(1, n)] for _ in range(m)]
            c = Contador()
            c1_sat.dos_sat(cl, n, contar=c)
            self.assertLessEqual(c["paso"], 4 * (2 * n + 2 * m))  # O(n + m)

    def test_verificar_camino_p1(self):
        red = {f"v{i}": [f"v{i + 1}"] for i in range(999)}
        red["v999"] = []
        camino = [f"v{i}" for i in range(1000)]
        c = Contador()
        self.assertTrue(p1_alcanzabilidad.verificar_camino(red, camino, "v0", "v999", contar=c))
        self.assertLessEqual(c["paso"], 999 + 999)  # O(E + |camino|)


def _cronometrar(f) -> float:
    t0 = time.perf_counter()
    f()
    return time.perf_counter() - t0


def _razon(chica, grande, repeticiones=5) -> float:
    """t(grande)/t(chica) con mediciones INTERCALADAS y el mínimo de cada una
    (si la máquina se carga a mitad de la prueba, afecta a las dos por igual)."""
    t_c, t_g = math.inf, math.inf
    for _ in range(repeticiones):
        t_c = min(t_c, _cronometrar(chica))
        t_g = min(t_g, _cronometrar(grande))
    return t_g / t_c


@unittest.skipIf(os.environ.get("LOGISTPULSE_SIN_TIEMPOS") == "1", "pruebas de tiempo desactivadas")
class TestTiemposReales(unittest.TestCase):
    """Tiempo real (reloj). Cada prueba compara la razón medida con la que predice la cota
    y con la que daría una clase de complejidad DISTINTA (los límites separan ambas).
    Hasta 3 intentos: el reloj tiene ruido; el conteo de operaciones (arriba) no."""

    def _verificar_razon(self, chica, grande, minimo, maximo, explicacion):
        razones = []
        for _ in range(3):
            r = _razon(chica, grande)
            razones.append(round(r, 2))
            if minimo <= r <= maximo:
                return
        self.fail(f"{explicacion}: razones medidas {razones} fuera de [{minimo}, {maximo}]")

    def test_dijkstra_crece_casi_lineal(self):
        rnd = random.Random(11)
        g1, g4 = grafo_aleatorio(5_000, 4, rnd), grafo_aleatorio(20_000, 4, rnd)
        self._verificar_razon(lambda: dijkstra(g1, "v0"), lambda: dijkstra(g4, "v0"), 2.0, 12.0,
                              "Dijkstra con 4× vértices: (V+E)·log V ⇒ ≈4.6× (caché hasta ~8×); cuadrático ≥ 16×")

    def test_bfs_crece_lineal(self):
        rnd = random.Random(12)
        a1 = grafo_aleatorio(10_000, 4, rnd).como_lista_adyacencia()
        a4 = grafo_aleatorio(40_000, 4, rnd).como_lista_adyacencia()
        self._verificar_razon(lambda: _bfs_completo(a1), lambda: _bfs_completo(a4), 2.0, 12.0,
                              "BFS con 4× vértices: O(V+E) ⇒ ≈4× (caché hasta ~8×); cuadrático ≥ 16×")

    def test_enumeracion_tsp_crece_factorial(self):
        rnd = random.Random(13)
        D8 = [[0 if i == j else rnd.randint(1, 9) for j in range(8)] for i in range(8)]
        D9 = [[0 if i == j else rnd.randint(1, 9) for j in range(9)] for i in range(9)]
        self._verificar_razon(lambda: c2_tsp_decision.decidir(D8, -1), lambda: c2_tsp_decision.decidir(D9, -1),
                              5.0, 25.0, "Enumeración TSP de 8 a 9 centros: (n−1)! ⇒ ≈9×; 2ⁿ daría 2×; polinómico ≈1.3×")

    def test_factor_rango_se_duplica_por_bit(self):
        N16, N18 = primo_menor_que(2 ** 16), primo_menor_que(2 ** 18)
        self._verificar_razon(lambda: n2_factor_rango.resolver(N16, N16 - 1),
                              lambda: n2_factor_rango.resolver(N18, N18 - 1), 2.5, 12.0,
                              "Factor en rango con 2 bits más: lineal en el VALOR ⇒ ≈4×; polinómico en bits ≈1.2×")


def _bfs_completo(ady):
    """Recorre TODO el grafo: el destino es un vértice aislado, inalcanzable (peor caso de BFS)."""
    ady = dict(ady)
    ady.setdefault("aislado", [])
    return bfs_ruta(ady, "v0", "aislado")


if __name__ == "__main__":
    unittest.main()
