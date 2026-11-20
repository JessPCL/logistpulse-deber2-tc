"""Los .jff de jflap/ son exactamente los autómatas probados en Python."""

import tempfile
import unittest
from pathlib import Path

from logistpulse.automatas import AUTOMATAS, SECUENCIAS
from logistpulse.automatas.jflap import a_jff, leer_jff

JFLAP = Path(__file__).resolve().parent.parent / "jflap"


class TestArchivosJFLAP(unittest.TestCase):
    def test_jff_igual_a_la_definicion(self):
        for clave, afd in AUTOMATAS.items():
            with self.subTest(clave=clave):
                leido = leer_jff(JFLAP / f"{clave}.jff")
                self.assertEqual(set(leido.estados), set(afd.estados))
                self.assertEqual(leido.inicial, afd.inicial)
                self.assertEqual(set(leido.finales), set(afd.finales))
                self.assertEqual(dict(leido.delta), dict(afd.delta))

    def test_jff_acepta_y_rechaza_lo_mismo(self):
        for clave in AUTOMATAS:
            leido = leer_jff(JFLAP / f"{clave}.jff")
            for cadena, esperado, _ in SECUENCIAS[clave]:
                with self.subTest(clave=clave, cadena=cadena):
                    self.assertEqual(leido.acepta(cadena), esperado)

    def test_archivo_de_entradas_para_multiple_run(self):
        for clave in AUTOMATAS:
            lineas = (JFLAP / f"entradas_{clave}.txt").read_text(encoding="utf-8").split()
            self.assertEqual(lineas, [c for c, _, _ in SECUENCIAS[clave] if c])


class TestJFLAPInvalido(unittest.TestCase):
    def _escribir(self, xml: str) -> Path:
        d = Path(tempfile.mkdtemp())
        p = d / "x.jff"
        p.write_text(xml, encoding="utf-8")
        return p

    def _jff(self, estados: str, transiciones: str, tipo: str = "fa") -> str:
        return f"<structure><type>{tipo}</type><automaton>{estados}{transiciones}</automaton></structure>"

    def test_transicion_lambda(self):
        p = self._escribir(self._jff('<state id="0" name="a"><initial/></state>',
                                     "<transition><from>0</from><to>0</to><read/></transition>"))
        with self.assertRaises(ValueError):
            leer_jff(p)

    def test_no_determinista(self):
        st = '<state id="0" name="a"><initial/></state><state id="1" name="b"/>'
        tr = ("<transition><from>0</from><to>0</to><read>x</read></transition>"
              "<transition><from>0</from><to>1</to><read>x</read></transition>")
        with self.assertRaises(ValueError):
            leer_jff(self._escribir(self._jff(st, tr)))

    def test_sin_inicial_y_tipo_incorrecto(self):
        with self.assertRaises(ValueError):
            leer_jff(self._escribir(self._jff('<state id="0" name="a"/>', "")))
        with self.assertRaises(ValueError):
            leer_jff(self._escribir(self._jff('<state id="0" name="a"><initial/></state>', "", tipo="pda")))

    def test_ida_y_vuelta(self):
        for afd in AUTOMATAS.values():
            p = self._escribir(a_jff(afd))
            self.assertEqual(dict(leer_jff(p).delta), dict(afd.delta))


if __name__ == "__main__":
    unittest.main()
