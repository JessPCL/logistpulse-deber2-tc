"""Fase D · Grupo C (NP-completo): c1 SAT, c2 TSP-decisión, c3 Vertex Cover.

Incluye: verificadores, reducciones ejecutables y exacto vs heurística (Fase E).
"""

import itertools
import random
import unittest

from logistpulse.casos import c1_sat as c1
from logistpulse.casos import c2_tsp_decision as c2
from logistpulse.casos import c3_vertex_cover as c3
from logistpulse.io_datos import cargar_casos

CASOS = cargar_casos()
SIM = CASOS["c1"]
TRES_SAT = SIM["tres_cnf_satisfacible"]
TRES_UNSAT = SIM["tres_cnf_insatisfacible"]
DIST, L = CASOS["c2"]["D"], CASOS["c2"]["L"]
TRAMPA = CASOS["c2"]["trampa_heuristica"]
CORREDORES, K = CASOS["c3"]["ady"], CASOS["c3"]["k"]


class TestC1(unittest.TestCase):
    def test_instancia_simulador(self):
        s = SIM
        for solver in (c1.fuerza_bruta, c1.dpll, c1.dos_sat):
            a = solver(s["clausulas"], s["n"])
            self.assertTrue(c1.verificar(s["clausulas"], a), solver.__name__)

    def test_instancia_simulador_es_2cnf(self):
        self.assertTrue(c1.es_2cnf(SIM["clausulas"]))
        self.assertFalse(c1.es_2cnf(TRES_SAT["clausulas"]))
        with self.assertRaises(ValueError):
            c1.dos_sat(TRES_SAT["clausulas"], TRES_SAT["n"])

    def test_3cnf_satisfacible_e_insatisfacible(self):
        t, u = TRES_SAT, TRES_UNSAT
        self.assertTrue(c1.verificar(t["clausulas"], c1.dpll(t["clausulas"], t["n"])))
        self.assertIsNone(c1.dpll(u["clausulas"], u["n"]))
        self.assertIsNone(c1.fuerza_bruta(u["clausulas"], u["n"]))

    def test_verificador_rechaza(self):
        self.assertFalse(c1.verificar([[1, -2], [2, 3]], {1: False, 2: True, 3: False}))

    def test_solvers_coinciden_aleatorio(self):
        rnd = random.Random(42)
        for _ in range(400):
            n = rnd.randint(3, 7)
            cl = [[rnd.choice((1, -1)) * v for v in rnd.sample(range(1, n + 1), 3)] for _ in range(rnd.randint(1, 25))]
            fb, dp = c1.fuerza_bruta(cl, n), c1.dpll(cl, n)
            self.assertEqual(fb is None, dp is None)
            if dp:
                self.assertTrue(c1.verificar(cl, dp))
        for _ in range(400):
            n = rnd.randint(1, 6)
            cl = [[rnd.choice((1, -1)) * rnd.randint(1, n) for _ in range(rnd.randint(1, 2))] for _ in range(rnd.randint(1, 12))]
            fb, ds = c1.fuerza_bruta(cl, n), c1.dos_sat(cl, n)
            self.assertEqual(fb is None, ds is None)
            if ds:
                self.assertTrue(c1.verificar(cl, ds))

    def test_limite_sin_clausulas(self):
        self.assertEqual(c1.dpll([], 2), {1: False, 2: False})

    def test_invalidos(self):
        for cl, n in (([[0]], 1), ([[]], 1), ([[4]], 3), ([[1.0]], 1), ([[1]], -1)):
            with self.subTest(cl=cl, n=n), self.assertRaises(ValueError):
                c1.dpll(cl, n)


class TestC2(unittest.TestCase):
    def test_instancia(self):
        tour, costo = c2.decidir(DIST, L)
        self.assertEqual(costo, 15)
        self.assertTrue(c2.verificar(DIST, L, tour))

    def test_limite_presupuesto(self):
        self.assertIsNotNone(c2.decidir(DIST, 15))
        self.assertIsNone(c2.decidir(DIST, 14))

    def test_verificador_rechaza(self):
        self.assertFalse(c2.verificar(DIST, 20, (0, 1, 2)))       # no regresa
        self.assertFalse(c2.verificar(DIST, 20, (0, 1, 1, 0)))    # repite y omite
        self.assertFalse(c2.verificar(DIST, 20, (0, 1, 7, 0)))    # centro inexistente
        self.assertFalse(c2.verificar(DIST, 14, (0, 1, 2, 0)))    # excede L

    def test_held_karp_coincide_con_fuerza_bruta(self):
        rnd = random.Random(1)
        for _ in range(60):
            n = rnd.randint(2, 7)
            D = [[0 if i == j else rnd.randint(1, 20) for j in range(n)] for i in range(n)]
            mejor = min(c2.costo(D, (0,) + p + (0,)) for p in itertools.permutations(range(1, n)))
            tour, costo = c2.held_karp(D)
            self.assertEqual(costo, mejor)
            self.assertTrue(c2.verificar(D, costo, tour))

    def test_heuristica_valida_pero_no_optima(self):
        nn_t, nn_c = c2.vecino_mas_cercano(TRAMPA)
        _, op_c = c2.held_karp(TRAMPA)
        self.assertTrue(c2.verificar(TRAMPA, nn_c, nn_t))
        self.assertGreater(nn_c, op_c)

    def test_reduccion_ham_a_tsp(self):
        def ham(n, aristas):
            E = {frozenset(e) for e in aristas}
            return any(all(frozenset((c[i], c[(i + 1) % n])) in E for i in range(n))
                       for c in ((0,) + p for p in itertools.permutations(range(1, n))))
        rnd = random.Random(3)
        for _ in range(80):
            n = rnd.randint(3, 6)
            aristas = [e for e in itertools.combinations(range(n), 2) if rnd.random() < 0.5]
            D, L = c2.reducir_ham_a_tsp(n, aristas)
            self.assertEqual(ham(n, aristas), c2.decidir(D, L) is not None)

    def test_invalidos(self):
        for D in ([[0]], [[0, -1], [1, 0]], [[0, 1], [1]], [[0, "a"], [1, 0]]):
            with self.subTest(D=D), self.assertRaises(ValueError):
                c2.decidir(D, 10)
        with self.assertRaises(ValueError):
            c2.reducir_ham_a_tsp(3, [(0, 0)])


class TestC3(unittest.TestCase):
    def test_instancia(self):
        S = c3.ramificacion(CORREDORES, K)
        self.assertEqual(S, {"B"})
        self.assertTrue(c3.verificar(CORREDORES, 1, S))

    def test_limites(self):
        self.assertIsNone(c3.ramificacion(CORREDORES, 0))
        self.assertEqual(c3.ramificacion({"a": [], "b": []}, 0), set())  # sin aristas

    def test_verificador_rechaza(self):
        self.assertFalse(c3.verificar(CORREDORES, 1, {"A"}))
        self.assertFalse(c3.verificar(CORREDORES, 1, {"A", "C"}))   # cubre pero |S| > k
        self.assertFalse(c3.verificar(CORREDORES, 2, {"B", "Z"}))   # Z ∉ V

    def _aleatorio(self, rnd, n):
        vs = [f"v{i}" for i in range(n)]
        g = {v: [] for v in vs}
        for u, v in itertools.combinations(vs, 2):
            if rnd.random() < 0.4:
                g[u].append(v)
                g[v].append(u)
        return g

    def test_exactos_y_aproximacion(self):
        rnd = random.Random(11)
        for _ in range(120):
            g = self._aleatorio(rnd, rnd.randint(1, 8))
            opt = len(c3.minimo_por_subconjuntos(g))
            self.assertIsNotNone(c3.ramificacion(g, opt))
            if opt > 0:
                self.assertIsNone(c3.ramificacion(g, opt - 1))
            apx = c3.aproximacion_2(g)
            self.assertTrue(c3.verificar(g, len(apx), apx))
            self.assertLessEqual(len(apx), 2 * opt)

    def test_reduccion_is_a_vc(self):
        rnd = random.Random(5)
        for _ in range(80):
            g = self._aleatorio(rnd, rnd.randint(1, 7))
            V, E = c3.aristas_de(g)
            for k in range(len(V) + 1):
                hay_is = any(all(not (u in S and v in S) for u, v in E) for S in map(set, itertools.combinations(V, k)))
                G2, k_vc = c3.reducir_is_a_vc(g, k)
                self.assertEqual(hay_is, c3.ramificacion(G2, k_vc) is not None)

    def test_invalidos(self):
        with self.assertRaises(ValueError):
            c3.ramificacion({"a": ["b"], "b": []}, 1)  # no simétrica
        with self.assertRaises(ValueError):
            c3.ramificacion({"a": ["a"]}, 1)
        with self.assertRaises(ValueError):
            c3.ramificacion(CORREDORES, -1)


if __name__ == "__main__":
    unittest.main()
