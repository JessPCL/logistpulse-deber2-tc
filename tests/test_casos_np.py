"""Fase D · Grupo B (NP con certificado): n1–n4. Se prueban BÚSQUEDA y VERIFICADOR por separado."""

import itertools
import random
import unittest

from logistpulse.casos import n1_isomorfismo as n1
from logistpulse.casos import n2_factor_rango as n2
from logistpulse.casos import n3_log_discreto as n3
from logistpulse.casos import n4_automorfismo as n4
from logistpulse.io_datos import cargar_casos

CASOS = cargar_casos()


class TestN1(unittest.TestCase):
    def setUp(self):
        self.A, self.B = CASOS["n1"]["A"], CASOS["n1"]["B"]

    def test_instancia_isomorfa(self):
        pi = n1.resolver(self.A, self.B)
        self.assertIsNotNone(pi)
        self.assertTrue(n1.verificar(self.A, self.B, pi))

    def test_mismos_grados_no_isomorfos(self):
        self.assertIsNone(n1.resolver(n1.ciclo(6), n1.union_de_ciclos(3, 3)))

    def test_verificador_rechaza_certificados_falsos(self):
        self.assertFalse(n1.verificar(self.A, self.B, (0, 1, 2)))
        self.assertFalse(n1.verificar(self.A, self.B, (0, 0, 1)))  # no es biyección
        self.assertFalse(n1.verificar(self.A, self.B, (0, 1)))     # longitud incorrecta

    def test_limite_tamanos_distintos_y_vacio(self):
        self.assertIsNone(n1.resolver(self.A, n1.ciclo(4)))
        self.assertEqual(n1.resolver([], []), ())

    def test_matrices_invalidas(self):
        for M in ([[0, 1], [0, 0]], [[1]], [[0, 2], [2, 0]], [[0, 1, 0], [1, 0]]):
            with self.subTest(M=M), self.assertRaises(ValueError):
                n1.resolver(M, M)


class TestN2(unittest.TestCase):
    def setUp(self):
        self.N, self.B = CASOS["n2"]["N"], CASOS["n2"]["B"]

    def test_instancia_leida_en_binario(self):
        self.assertEqual((self.N, self.B), (91, 10))
        self.assertEqual(n2.resolver(self.N, self.B), 7)
        self.assertTrue(n2.verificar(self.N, self.B, 7))

    def test_limites(self):
        self.assertIsNone(n2.resolver(91, 6))
        self.assertEqual(n2.resolver(91, 7), 7)          # d = B exacto
        self.assertIsNone(n2.resolver(97, 96))           # primo con B < N
        self.assertEqual(n2.resolver(97, 97), 97)        # B ≥ N: trivialmente Sí
        self.assertIsNone(n2.resolver(91, 1))

    def test_verificador_rechaza(self):
        self.assertFalse(n2.verificar(91, 10, 13))  # divide pero fuera de rango
        self.assertFalse(n2.verificar(91, 10, 3))   # en rango pero no divide
        self.assertFalse(n2.verificar(91, 10, 1))
        self.assertFalse(n2.verificar(91, 10, 7.0))

    def test_binario(self):
        self.assertEqual(n2.desde_binario("1011011"), 91)
        for malo in ("10201", "", None):
            with self.subTest(malo=malo), self.assertRaises(ValueError):
                n2.desde_binario(malo)

    def test_invalidos(self):
        for N, B in ((1, 10), (91, -1), (91.0, 10), (True, 10)):
            with self.subTest(N=N, B=B), self.assertRaises(ValueError):
                n2.resolver(N, B)


class TestN3(unittest.TestCase):
    def setUp(self):
        c = CASOS["n3"]
        self.p, self.g, self.h, self.B = c["p"], c["g"], c["h"], c["B"]

    def test_instancia(self):
        self.assertEqual(n3.resolver(self.p, self.g, self.h, self.B), 6)
        self.assertEqual(n3.baby_step_giant_step(self.p, self.g, self.h, self.B), 6)
        self.assertTrue(n3.verificar(self.p, self.g, self.h, self.B, 6))

    def test_limites(self):
        self.assertIsNone(n3.resolver(23, 5, 8, 5))
        self.assertEqual(n3.resolver(23, 5, 8, 6), 6)
        self.assertEqual(n3.resolver(23, 5, 1, 0), 0)  # x = 0
        self.assertIsNone(n3.resolver(23, 5, 0, 100))  # 0 nunca es potencia de g

    def test_potencia_modular_igual_a_pow(self):
        rnd = random.Random(3)
        for _ in range(300):
            p = rnd.choice([23, 101, 1009, 7919])
            g, x = rnd.randrange(1, p), rnd.randrange(0, 10 ** 6)
            self.assertEqual(n3.potencia_modular(g, x, p), pow(g, x, p))

    def test_bsgs_coincide_con_busqueda_lineal(self):
        rnd = random.Random(7)
        for _ in range(500):
            p = rnd.choice([23, 101, 1009])
            g, h, B = rnd.randrange(1, p), rnd.randrange(0, p), rnd.randrange(0, 2 * p)
            self.assertEqual(n3.resolver(p, g, h, B), n3.baby_step_giant_step(p, g, h, B))

    def test_verificador_rechaza(self):
        self.assertFalse(n3.verificar(23, 5, 8, 10, 5))
        self.assertFalse(n3.verificar(23, 5, 8, 5, 6))  # x correcto pero fuera de la cota

    def test_invalidos(self):
        for args in ((21, 5, 8, 10), (23, 0, 8, 10), (23, 5, 30, 10), (23, 5, 8, -1)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                n3.resolver(*args)

    def test_primalidad(self):
        primos = [q for q in range(2, 500) if all(q % d for d in range(2, int(q ** 0.5) + 1))]
        self.assertEqual([q for q in range(500) if n3.es_primo(q)], primos)


class TestN4(unittest.TestCase):
    def setUp(self):
        self.G, self.asim = CASOS["n4"]["G"], CASOS["n4"]["asimetrico_6"]

    def test_triangulo_tiene_simetria(self):
        pi, _ = n4.resolver(self.G)
        self.assertTrue(n4.verificar(self.G, pi))

    def test_grafo_asimetrico_agota_las_permutaciones(self):
        pi, examinadas = n4.resolver(self.asim)
        self.assertIsNone(pi)
        self.assertEqual(examinadas, 720)
        G = self.asim  # comprobación independiente: el único automorfismo es la identidad
        auts = [p for p in itertools.permutations(range(6))
                if all(G[i][j] == G[p[i]][p[j]] for i in range(6) for j in range(6))]
        self.assertEqual(auts, [tuple(range(6))])

    def test_verificador_rechaza_identidad_y_falsos(self):
        self.assertFalse(n4.verificar(self.G, (0, 1, 2)))
        camino = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
        self.assertFalse(n4.verificar(camino, (1, 0, 2)))
        self.assertTrue(n4.verificar(camino, (2, 1, 0)))

    def test_limite_un_vertice(self):
        self.assertIsNone(n4.resolver([[0]])[0])


if __name__ == "__main__":
    unittest.main()
