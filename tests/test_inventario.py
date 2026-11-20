"""Fase C · FEFO y reposición (normales, límite e inválidas)."""

import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from logistpulse.inventario import EstadoSKU, Lote, emitir_orden, seleccionar_fefo, sugerencias, sugerir
from logistpulse.io_datos import cargar_lotes, cargar_skus

HOY = date(2026, 11, 20)


class TestFEFO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lotes, cls.ref, _ = cargar_lotes()

    def test_pedido_normal_y_desempate_por_codigo(self):
        r = seleccionar_fefo(self.lotes, "LECHE-1L", 80, self.ref)
        self.assertEqual(r.plan, [("L-001", 30), ("L-002", 25), ("L-003", 25)])
        self.assertEqual((r.estado, r.pendiente, r.reservado), ("COMPLETO", 0, 80))

    def test_excluye_vencidos_que_vencen_hoy_y_sin_stock(self):
        r = seleccionar_fefo(self.lotes, "LECHE-1L", 1, self.ref)
        descartados = dict(r.descartados)
        self.assertIn("L-004", descartados)
        self.assertIn("L-007", descartados)  # vence el mismo día de la referencia
        self.assertIn("L-005", descartados)  # disponible 0
        self.assertNotIn("Y-100", r.orden_considerado)  # otro SKU

    def test_stock_insuficiente_las_tres_politicas(self):
        p = seleccionar_fefo(self.lotes, "LECHE-1L", 200, self.ref, "parcial")
        self.assertEqual((p.estado, p.reservado, p.pendiente), ("PARCIAL", 155, 45))
        self.assertTrue(p.requiere_reposicion)
        r = seleccionar_fefo(self.lotes, "LECHE-1L", 200, self.ref, "rechazar")
        self.assertEqual((r.estado, r.plan, r.pendiente), ("RECHAZADO", [], 200))
        e = seleccionar_fefo(self.lotes, "LECHE-1L", 200, self.ref, "esperar")
        self.assertEqual((e.estado, e.plan, e.pendiente, e.requiere_reposicion), ("EN_ESPERA", [], 200, True))

    def test_limite_exactamente_todo_el_stock_elegible(self):
        r = seleccionar_fefo(self.lotes, "LECHE-1L", 155, self.ref)
        self.assertEqual((r.estado, r.pendiente, len(r.plan)), ("COMPLETO", 0, 4))

    def test_limite_cantidad_uno_y_lista_vacia(self):
        self.assertEqual(seleccionar_fefo(self.lotes, "LECHE-1L", 1, self.ref).plan, [("L-001", 1)])
        vacio = seleccionar_fefo([], "LECHE-1L", 5, HOY)
        self.assertEqual((vacio.estado, vacio.pendiente), ("PARCIAL", 5))

    def test_orden_independiente_del_orden_de_entrada(self):
        a = seleccionar_fefo(self.lotes, "LECHE-1L", 120, self.ref)
        b = seleccionar_fefo(list(reversed(self.lotes)), "LECHE-1L", 120, self.ref)
        self.assertEqual(a.plan, b.plan)

    def test_entradas_invalidas(self):
        for cantidad in (0, -3, 2.5, True, "10"):
            with self.subTest(cantidad=cantidad), self.assertRaises(ValueError):
                seleccionar_fefo(self.lotes, "LECHE-1L", cantidad, self.ref)
        with self.assertRaises(ValueError):
            seleccionar_fefo(self.lotes, "LECHE-1L", 5, self.ref, "esperar_magia")
        with self.assertRaises(ValueError):
            seleccionar_fefo(self.lotes, "LECHE-1L", 5, "2026-11-20")
        dup = [Lote("X", "S", HOY, 1), Lote("X", "S", HOY, 2)]
        with self.assertRaises(ValueError):
            seleccionar_fefo(dup, "S", 1, HOY)
        for kwargs in ({"disponible": -1}, {"disponible": 1.5}, {"codigo": ""}, {"vencimiento": "2026-12-01"}):
            base = {"codigo": "L", "sku": "S", "vencimiento": HOY, "disponible": 1, **kwargs}
            with self.subTest(lote=kwargs), self.assertRaises(ValueError):
                Lote(**base)

    def test_json_con_fecha_invalida(self):
        p = Path(tempfile.mkdtemp()) / "l.json"
        p.write_text(json.dumps({"fecha_referencia": "20/11/2026", "lotes": []}), encoding="utf-8")
        with self.assertRaises(ValueError):
            cargar_lotes(p)


class TestReposicion(unittest.TestCase):
    def test_ejemplo_del_enunciado(self):
        s = sugerir(EstadoSKU("SKU-EJ", 18, 10, 5, 30, 50))
        self.assertEqual((s.posicion, s.cantidad), (23, 27))

    def test_limite_posicion_igual_al_minimo(self):
        self.assertEqual(sugerir(EstadoSKU("A", 30, 0, 0, 30, 45)).cantidad, 15)
        self.assertEqual(sugerir(EstadoSKU("A", 31, 0, 0, 30, 45)).cantidad, 0)

    def test_limite_minimo_igual_objetivo(self):
        self.assertEqual(sugerir(EstadoSKU("A", 30, 0, 0, 30, 30)).cantidad, 0)

    def test_posicion_negativa(self):
        s = sugerir(EstadoSKU("Q", 10, 0, 15, 20, 40))
        self.assertEqual((s.posicion, s.cantidad), (-5, 45))

    def test_no_duplica_si_ya_hay_orden_abierta(self):
        inicial = EstadoSKU("Z", 18, 0, 5, 30, 50)
        primera = sugerir(inicial)
        self.assertEqual(primera.cantidad, 37)
        segunda = sugerir(emitir_orden(inicial, primera.cantidad))
        self.assertEqual(segunda.cantidad, 0)

    def test_orden_abierta_parcial_solo_sugiere_la_diferencia(self):
        s = sugerir(EstadoSKU("Z", 18, 10, 5, 30, 50))  # ya hay 10 en orden
        self.assertEqual(s.cantidad, 27)  # no 37

    def test_lote_desde_json(self):
        sugs = list(sugerencias(cargar_skus()))
        self.assertEqual(len(sugs), 6)
        self.assertEqual({s.sku: s.cantidad for s in sugs}["YOGUR-200G"], 0)

    def test_entradas_invalidas(self):
        for campo in ("disponible", "en_orden", "reservado", "minimo", "objetivo"):
            datos = dict(sku="X", disponible=1, en_orden=0, reservado=0, minimo=1, objetivo=2)
            for malo in (-1, 1.5, True, None):
                datos[campo] = malo
                with self.subTest(campo=campo, valor=malo), self.assertRaises(ValueError):
                    EstadoSKU(**datos)
        with self.assertRaises(ValueError):
            EstadoSKU("X", 1, 0, 0, 50, 10)  # objetivo < mínimo
        dup = {"skus": [dict(sku="X", disponible=1, en_orden=0, reservado=0, minimo=1, objetivo=2)] * 2}
        p = Path(tempfile.mkdtemp()) / "s.json"
        p.write_text(json.dumps(dup), encoding="utf-8")
        with self.assertRaises(ValueError):
            cargar_skus(p)  # los SKU repetidos se rechazan al LEER
        with self.assertRaises(ValueError):
            emitir_orden(EstadoSKU("X", 1, 0, 0, 1, 2), -5)


if __name__ == "__main__":
    unittest.main()
