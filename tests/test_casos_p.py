"""Fase D · Grupo A (P): p1 alcanzabilidad, p2 ruta mínima, p3 flujo máximo.
Datos de los expedientes: data/casos_simulador.json (leídos con io_datos.cargar_casos)."""

import unittest
from pathlib import Path

from logistpulse.casos import p1_alcanzabilidad as p1
from logistpulse.casos import p2_ruta_minima as p2
from logistpulse.casos import p3_flujo_maximo as p3
from logistpulse.io_datos import cargar_casos
from logistpulse.rutas import GrafoPonderado

CASOS = cargar_casos()


class TestP1(unittest.TestCase):
    def setUp(self):
        self.c = CASOS["p1"]

    def test_alcanzable(self):
        self.assertEqual(p1.resolver(self.c["red"], "Durán", "Norte"), ["Durán", "Quito", "Norte"])
        self.assertTrue(p1.decidir(self.c["red"], "Durán", "Norte"))

    def test_no_alcanzable_con_cierre(self):
        self.assertIsNone(p1.resolver(self.c["red_con_cierre"], "Durán", "Norte"))
        self.assertFalse(p1.decidir(self.c["red_con_cierre"], "Durán", "Norte"))

    def test_programa_con_lista_de_conexiones(self):
        """El correo pide un programa que se ejecute con una lista de conexiones: ejemplo con ruta y sin ruta."""
        import contextlib
        import io
        from logistpulse.__main__ import main
        ej = Path(__file__).resolve().parent.parent / "data" / "ejemplos"
        for archivo, esperado in (("p1_con_ruta.txt", "Sí: existe ruta Durán → Norte"),
                                  ("p1_sin_ruta.txt", "No: no existe ruta Durán → Norte")):
            salida = io.StringIO()
            with contextlib.redirect_stdout(salida):
                codigo = main(["p1", str(ej / archivo), "Durán", "Norte"])
            self.assertEqual(codigo, 0)
            self.assertIn(esperado, salida.getvalue())

    def test_lectura_de_conexiones_invalida(self):
        import tempfile
        from logistpulse.io_datos import cargar_conexiones
        with tempfile.TemporaryDirectory() as d:
            malo = Path(d) / "malo.txt"
            malo.write_text("Durán Quito\n", encoding="utf-8")  # sin separador
            with self.assertRaises(ValueError):
                cargar_conexiones(malo)
            bien = Path(d) / "bien.txt"
            bien.write_text("# comentario\n\nA, B\nB -> C\n", encoding="utf-8")
            self.assertEqual(cargar_conexiones(bien), [("A", "B"), ("B", "C")])

    def test_grafo_dirigido_no_vuelve(self):
        self.assertFalse(p1.decidir(self.c["red"], "Norte", "Durán"))

    def test_limite_origen_igual_destino(self):
        self.assertEqual(p1.resolver(self.c["red"], "Durán", "Durán"), ["Durán"])

    def test_traza_bfs_por_niveles(self):
        traza = []
        p1.resolver(self.c["red"], "Durán", "Norte", traza=traza)
        self.assertEqual([t["sale"] for t in traza], ["Durán", "Quito", "Guayaquil", "Norte"])
        self.assertEqual(traza[0]["entran"], ["Quito", "Guayaquil"])

    def test_verificador_de_camino(self):
        red = self.c["red"]
        self.assertTrue(p1.verificar_camino(red, ["Durán", "Quito", "Norte"], "Durán", "Norte"))
        self.assertFalse(p1.verificar_camino(red, ["Durán", "Norte"], "Durán", "Norte"))
        self.assertFalse(p1.verificar_camino(red, [], "Durán", "Norte"))

    def test_invalidos(self):
        with self.assertRaises(ValueError):
            p1.resolver(self.c["red"], "Durán", "Cuenca")
        for conexiones in ([["Durán"]], [["A", "A"]], [["A", "B"], ["A", "B"]], [["A", ""]]):
            with self.subTest(conexiones=conexiones), self.assertRaises(ValueError):
                p1.red_desde_conexiones(conexiones)
        with self.assertRaises(ValueError):  # cerrar un tramo que no existe
            p1.red_desde_conexiones([["A", "B"]], [["B", "A"]])


class TestP2(unittest.TestCase):
    def setUp(self):
        self.c = CASOS["p2"]

    def test_distancias_y_ruta(self):
        dist, ruta, empates = p2.resolver(self.c["grafo"], "Quito", "Guayaquil")
        self.assertEqual(dist, {"Quito": 0, "Latacunga": 2, "Ambato": 5, "Guayaquil": 8})
        self.assertEqual(ruta, ["Quito", "Latacunga", "Guayaquil"])
        self.assertEqual(len(empates), 2)

    def test_version_decision_limite(self):
        self.assertTrue(p2.decidir(self.c["grafo"], "Quito", "Guayaquil", 8))
        self.assertFalse(p2.decidir(self.c["grafo"], "Quito", "Guayaquil", 7.999))

    def test_dijkstra_falla_con_pesos_negativos(self):
        neg = self.c["contraejemplo_negativo"]
        self.assertEqual(p2.dijkstra_sin_precondicion(neg, "S")["C"], 3)
        self.assertEqual(p2.bellman_ford(neg, "S")["C"], 2)

    def test_bellman_ford_detecta_ciclo_negativo(self):
        with self.assertRaises(ValueError):
            p2.bellman_ford({"a": [("b", 1)], "b": [("a", -2)]}, "a")

    def test_grafo_rechaza_pesos_negativos_y_destino_inexistente(self):
        with self.assertRaises(ValueError):
            p2.grafo_desde_tramos([["S", "A", -1]])
        with self.assertRaises(ValueError):
            p2.resolver(self.c["grafo"], "Quito", "Cuenca")


class TestP3(unittest.TestCase):
    def setUp(self):
        self.cap = CASOS["p3"]["capacidades"]

    def test_flujo_maximo_y_corte(self):
        valor, flujo, lado_s, _ = p3.edmonds_karp(self.cap, "Planta", "Clientes")
        self.assertEqual(valor, 10)
        self.assertEqual(p3.verificar_flujo(self.cap, flujo, "Planta", "Clientes"), 10)
        self.assertEqual(p3.capacidad_corte(self.cap, lado_s), 10)

    def test_registro_de_tramos_usados_y_disponibles(self):
        *_, registro = p3.edmonds_karp(self.cap, "Planta", "Clientes")
        self.assertEqual(sum(r["cuello"] for r in registro), 10)
        for r in registro:
            for tr in r["tramos"]:
                self.assertEqual(tr["usado"] + tr["disponible"], tr["capacidad"])
                self.assertGreaterEqual(tr["disponible"], 0)

    def test_registro_con_cancelacion_de_flujo(self):
        """El 2.º camino aumentante usa el tramo inverso b→a: se CANCELA el flujo de a→b."""
        cap = {"s": {"a": 1, "c": 1}, "a": {"b": 1, "e": 1}, "b": {"t": 1},
               "c": {"b": 1}, "e": {"f": 1}, "f": {"t": 1}, "t": {}}
        valor, flujo, _, registro = p3.edmonds_karp(cap, "s", "t")
        self.assertEqual(valor, 2)
        self.assertEqual(registro[1]["camino"], ["s", "c", "b", "a", "e", "f", "t"])
        self.assertIn(("cancelar", "a→b"), [(tr["accion"], tr["tramo"]) for tr in registro[1]["tramos"]])
        self.assertEqual(flujo[("a", "b")], 0)
        self.assertEqual(p3.verificar_flujo(cap, flujo, "s", "t"), 2)

    def test_version_decision(self):
        self.assertTrue(p3.decidir(self.cap, "Planta", "Clientes", 10))
        self.assertFalse(p3.decidir(self.cap, "Planta", "Clientes", 11))

    def test_limite_sin_camino(self):
        self.assertEqual(p3.edmonds_karp({"s": {"a": 5}, "a": {}, "t": {}}, "s", "t")[0], 0)

    def test_verificador_detecta_flujo_invalido(self):
        with self.assertRaises(ValueError):
            p3.verificar_flujo(self.cap, {("Planta", "Quito"): 8}, "Planta", "Clientes")
        with self.assertRaises(ValueError):  # no se conserva en Quito
            p3.verificar_flujo(self.cap, {("Planta", "Quito"): 3}, "Planta", "Clientes")

    def test_entradas_invalidas(self):
        casos = [({"s": {"t": -1}}, "t"), ({"s": {"t": 1.5}}, "t"), ({"s": {"s": 1}}, "t"),
                 ({"s": {"a": 1}, "a": {"s": 1}}, "a")]
        for cap, t in casos:
            with self.subTest(cap=cap), self.assertRaises(ValueError):
                p3.edmonds_karp(cap, "s", t)
        with self.assertRaises(ValueError):
            p3.edmonds_karp(self.cap, "Planta", "Planta")
        with self.assertRaises(ValueError):
            p3.capacidades_desde_tramos([["a", "b", 1], ["a", "b", 2]])


if __name__ == "__main__":
    unittest.main()
