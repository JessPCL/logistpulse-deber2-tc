"""Fase A · Pruebas de los tres AFD (normales, límite e inválidas)."""

import unittest

from logistpulse.automatas import (AFD, AUTOMATAS, ESTADO_SUMIDERO, ORDEN_COMPRA, PEDIDO,
                                   PEDIDO_ESTRICTO, RESERVA, SECUENCIAS)


class TestSecuencias(unittest.TestCase):
    def test_todas_las_secuencias_documentadas(self):
        for clave, afd in AUTOMATAS.items():
            for cadena, esperado, explicacion in SECUENCIAS[clave]:
                with self.subTest(automata=clave, cadena=cadena):
                    self.assertEqual(afd.acepta(cadena), esperado, explicacion)

    def test_minimo_dos_validas_y_dos_invalidas_por_automata(self):
        for clave, casos in SECUENCIAS.items():
            validas = sum(1 for _, ok, _ in casos if ok)
            invalidas = sum(1 for _, ok, _ in casos if not ok)
            self.assertGreaterEqual(validas, 2, clave)
            self.assertGreaterEqual(invalidas, 2, clave)

    def test_pruebas_minimas_del_enunciado(self):
        self.assertTrue(PEDIDO.acepta(["confirmar", "reservar", "iniciar_picking", "empacar", "despachar", "entregar"]))
        self.assertFalse(PEDIDO.acepta(["despachar"]))
        self.assertTrue(RESERVA.acepta(["validar", "confirmar", "picking"]))
        self.assertFalse(ORDEN_COMPRA.acepta(["solicitar_aprobacion", "rechazar", "emitir_orden"]))

    def test_no_se_consume_reserva_sin_confirmar(self):
        r = RESERVA.ejecutar("vp")
        self.assertFalse(r.aceptada)
        self.assertEqual(r.estado_final, ESTADO_SUMIDERO)

    def test_traza_identifica_la_transicion_que_rechaza(self):
        r = PEDIDO.ejecutar("crid")
        self.assertEqual(r.traza[3], ("Preparacion", "d", ESTADO_SUMIDERO))
        self.assertIn("Paso 4", r.motivo)

    def test_varias_recepciones_parciales(self):
        self.assertTrue(ORDEN_COMPRA.acepta("sae" + "p" * 10 + "f"))


class TestLimites(unittest.TestCase):
    def test_cadena_vacia_rechazada(self):
        for afd in AUTOMATAS.values():
            self.assertFalse(afd.acepta(""))

    def test_sumidero_es_absorbente(self):
        for afd in AUTOMATAS.values():
            for a in afd.alfabeto:
                self.assertEqual(afd.transicion(ESTADO_SUMIDERO, a), ESTADO_SUMIDERO)

    def test_estados_finales_no_tienen_salidas(self):
        for afd in AUTOMATAS.values():
            for (q, _a) in afd.delta:
                self.assertNotIn(q, afd.finales, f"{afd.nombre}: {q} es final pero tiene salida")

    def test_todos_los_estados_alcanzables(self):
        for afd in AUTOMATAS.values():
            self.assertEqual(afd.estados_alcanzables(), set(afd.estados))

    def test_variante_estricta_del_pedido(self):
        self.assertFalse(PEDIDO_ESTRICTO.acepta("x"))
        self.assertTrue(PEDIDO_ESTRICTO.acepta("criedn"))


class TestEntradasInvalidas(unittest.TestCase):
    def test_simbolo_fuera_de_sigma(self):
        with self.assertRaises(ValueError):
            PEDIDO.ejecutar("cz")

    def test_evento_desconocido(self):
        with self.assertRaises(ValueError):
            RESERVA.ejecutar(["validar", "teletransportar"])

    def test_elemento_no_textual(self):
        with self.assertRaises(ValueError):
            RESERVA.ejecutar(["v", 3])

    def test_definiciones_mal_formadas(self):
        base = dict(nombre="X", estados=["a", "b"], alfabeto={"0": "cero"}, inicial="a", finales={"b"},
                    delta={("a", "0"): "b"})
        AFD(**base)  # válido
        for cambio in (
            {"inicial": "z"},
            {"finales": {"z"}},
            {"delta": {("a", "0"): "z"}},
            {"delta": {("a", "1"): "b"}},
            {"alfabeto": {"00": "doble"}},
            {"estados": ["a", "a", "b"]},
            {"estados": ["a", "b", ESTADO_SUMIDERO]},
        ):
            with self.subTest(cambio=cambio), self.assertRaises(ValueError):
                AFD(**{**base, **cambio})


if __name__ == "__main__":
    unittest.main()
