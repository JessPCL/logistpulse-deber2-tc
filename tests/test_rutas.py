"""Fase B · Grafo de planta, Dijkstra y BFS."""

import itertools
import json
import math
import random
import tempfile
import unittest
from pathlib import Path

from logistpulse.io_datos import cargar_planta
from logistpulse.rutas import (GrafoPonderado, alcanzable, bfs_ruta, dijkstra, ruta_minima,
                               todas_las_rutas_minimas)

RUTA_FIGURA_5 = ["R", "B", "A", "P", "E", "D"]


class TestPlanta(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g, cls.datos = cargar_planta()

    def test_tamano_y_tipo(self):
        self.assertEqual((self.g.num_vertices, self.g.num_aristas, self.g.dirigido), (7, 11, False))

    def test_ruta_base_costo_11(self):
        ruta, costo = ruta_minima(self.g, "R", "D")
        self.assertEqual(costo, 11)
        self.assertEqual(ruta, ["R", "B", "A", "E", "D"])
        self.assertEqual(self.g.costo_ruta(ruta), 11)

    def test_ruta_de_la_figura_es_optima_y_empata(self):
        self.assertEqual(self.g.costo_ruta(RUTA_FIGURA_5), 11)
        self.assertIn(RUTA_FIGURA_5, todas_las_rutas_minimas(self.g, "R", "D"))
        self.assertEqual(len(todas_las_rutas_minimas(self.g, "R", "D")), 2)

    def test_bloqueos(self):
        self.assertEqual(ruta_minima(self.g, "R", "D", ["A"])[1], 12)
        self.assertEqual(ruta_minima(self.g, "R", "D", ["P"]), (["R", "B", "A", "E", "D"], 11))
        ruta, costo = ruta_minima(self.g, "R", "D", ["E"])
        self.assertIsNone(ruta)
        self.assertEqual(costo, math.inf)
        self.assertEqual(todas_las_rutas_minimas(self.g, "R", "D", ["E"]), [])

    def test_destino_bloqueado_no_tiene_ruta(self):
        self.assertIsNone(ruta_minima(self.g, "R", "D", ["D"])[0])

    def test_origen_igual_destino(self):
        self.assertEqual(ruta_minima(self.g, "R", "R"), (["R"], 0))

    def test_bfs_minimiza_tramos_no_costo(self):
        ady = self.g.como_lista_adyacencia()
        ruta = bfs_ruta(ady, "R", "D")
        self.assertEqual(ruta, ["R", "A", "E", "D"])
        self.assertGreater(self.g.costo_ruta(ruta), 11)
        self.assertFalse(alcanzable(ady, "R", "D", ["E"]))

    def test_traza_reproducible(self):
        t1 = dijkstra(self.g, "R", con_traza=True).traza
        t2 = dijkstra(self.g, "R", con_traza=True).traza
        self.assertEqual(t1, t2)
        self.assertEqual([u for u, _ in dijkstra(self.g, "R").orden_finalizacion], list("RBACPED"))


class TestInvalidos(unittest.TestCase):
    def test_pesos_invalidos(self):
        for peso in (-1, float("nan"), float("inf"), "3", True, None):
            with self.subTest(peso=peso), self.assertRaises(ValueError):
                GrafoPonderado().agregar_arista("a", "b", peso)

    def test_lazo_y_duplicada(self):
        g = GrafoPonderado()
        with self.assertRaises(ValueError):
            g.agregar_arista("a", "a", 1)
        g.agregar_arista("a", "b", 1)
        with self.assertRaises(ValueError):
            g.agregar_arista("b", "a", 2)

    def test_origen_destino_y_bloqueos_invalidos(self):
        g, _ = cargar_planta()
        with self.assertRaises(ValueError):
            ruta_minima(g, "X", "D")
        with self.assertRaises(ValueError):
            ruta_minima(g, "R", "X")
        with self.assertRaises(ValueError):
            ruta_minima(g, "R", "D", ["R"])
        with self.assertRaises(ValueError):
            ruta_minima(g, "R", "D", ["Z"])
        with self.assertRaises(ValueError):
            bfs_ruta(g.como_lista_adyacencia(), "R", "Z")

    def test_json_con_vertice_no_declarado(self):
        d = {"dirigido": False, "vertices": {"a": "A"}, "aristas": [["a", "b", 1]], "origen": "a", "destino": "b"}
        p = Path(tempfile.mkdtemp()) / "p.json"
        p.write_text(json.dumps(d), encoding="utf-8")
        with self.assertRaises(ValueError):
            cargar_planta(p)

    def test_json_mal_formado_y_campos_faltantes(self):
        carpeta = Path(tempfile.mkdtemp())
        (carpeta / "malo.json").write_text("{no es json", encoding="utf-8")
        (carpeta / "incompleto.json").write_text('{"dirigido": false}', encoding="utf-8")
        for nombre in ("malo.json", "incompleto.json"):
            with self.subTest(nombre=nombre), self.assertRaises(ValueError):
                cargar_planta(carpeta / nombre)
        with self.assertRaises(FileNotFoundError):
            cargar_planta(carpeta / "no_existe.json")


class TestDirigidoYAleatorio(unittest.TestCase):
    def test_arista_de_un_solo_sentido(self):
        g = GrafoPonderado.desde_aristas([("a", "b", 1)], dirigido=True)
        self.assertEqual(ruta_minima(g, "a", "b"), (["a", "b"], 1))
        self.assertIsNone(ruta_minima(g, "b", "a")[0])

    def test_dijkstra_coincide_con_fuerza_bruta(self):
        """Compara contra la enumeración de todos los caminos simples en grafos pequeños."""
        rnd = random.Random(2026)
        for _ in range(150):
            n = rnd.randint(2, 6)
            vs = [f"v{i}" for i in range(n)]
            g = GrafoPonderado(dirigido=rnd.random() < 0.5)
            for v in vs:
                g.agregar_vertice(v)
            for u, v in itertools.permutations(vs, 2):
                if g.peso(u, v) is None and rnd.random() < 0.4:
                    g.agregar_arista(u, v, rnd.randint(0, 9))
            s, t = vs[0], vs[-1]
            mejor = math.inf
            for k in range(0, n - 1):
                for medio in itertools.permutations(vs[1:-1], k):
                    camino = [s, *medio, t]
                    try:
                        mejor = min(mejor, g.costo_ruta(camino))
                    except ValueError:
                        pass
            ruta, costo = ruta_minima(g, s, t)
            self.assertEqual(costo, mejor)
            if ruta:
                self.assertEqual(g.costo_ruta(ruta), costo)


if __name__ == "__main__":
    unittest.main()
