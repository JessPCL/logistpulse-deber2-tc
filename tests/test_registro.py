"""Coherencia del registro, de las capas y de los datos de los 10 casos."""

import ast
import unittest
from pathlib import Path

from logistpulse.casos import CASOS
from logistpulse.io_datos import cargar_casos
from logistpulse.presentacion_casos import DEMOS

RAIZ = Path(__file__).resolve().parent.parent


class TestRegistro(unittest.TestCase):
    def test_distribucion_3_4_3(self):
        conteo = {g: sum(1 for c in CASOS if c.grupo == g) for g in "ABC"}
        self.assertEqual(conteo, {"A": 3, "B": 4, "C": 3})

    def test_clase_coherente_con_grupo(self):
        for c in CASOS:
            self.assertEqual(c.clase, {"A": "P", "B": "NP", "C": "NP-completo"}[c.grupo], c.id)

    def test_grupo_c_declara_reduccion_y_b_no_afirma_npc(self):
        for c in CASOS:
            if c.grupo == "C":
                self.assertIn("≤p", c.reduccion, c.id)
            if c.grupo == "B":
                self.assertEqual(c.reduccion, "—", c.id)

    def test_optimizacion_declara_version_de_decision(self):
        for c in CASOS:
            if "ptimización" in c.version.split(";")[0]:
                self.assertIn("decisión", c.version, c.id)

    def test_modulos_existen_y_demos_corren(self):
        datos = cargar_casos()
        for c in CASOS:
            self.assertTrue((RAIZ / c.modulo).exists(), c.modulo)
            salida = DEMOS[c.id](datos[c.id])
            self.assertTrue(salida.startswith("RESPUESTA AL CORREO"), c.id)


class TestCapas(unittest.TestCase):
    """Separación lectura / procesamiento / presentación (Fase E)."""

    def _modulos(self, carpeta):
        return [p for p in (RAIZ / "logistpulse" / carpeta).glob("*.py") if p.name != "__init__.py"]

    def test_procesamiento_no_lee_archivos_ni_imprime(self):
        for carpeta in ("casos", "rutas", "inventario", "automatas"):
            for p in self._modulos(carpeta):
                if p.name == "jflap.py":  # exportador/importador de formato: es lectura/escritura por diseño
                    continue
                arbol = ast.parse(p.read_text(encoding="utf-8"))
                llamadas = {n.func.id for n in ast.walk(arbol) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
                self.assertFalse(llamadas & {"open", "print", "input"}, f"{p.name} mezcla E/S con procesamiento")
                importados = {a.name for n in ast.walk(arbol) if isinstance(n, ast.ImportFrom) for a in n.names}
                self.assertFalse(importados & {"cargar_casos", "cargar_planta", "cargar_lotes", "cargar_skus"}, p.name)

    def test_casos_sin_datos_de_expediente_incrustados(self):
        codigo = _sin_docstrings("".join(p.read_text(encoding="utf-8") for p in self._modulos("casos")))
        for dato in ("Latacunga", "Durán", "1011011", "[[0, 4, 8]"):  # deben vivir en data/casos_simulador.json
            self.assertNotIn(dato, codigo, dato)


def _sin_docstrings(texto: str) -> str:
    """Quita los docstrings para buscar datos incrustados solo en el código."""
    partes = texto.split('"""')
    return "".join(partes[::2])


if __name__ == "__main__":
    unittest.main()


class TestMatrizTrazabilidad(unittest.TestCase):
    """Cada prueba y archivo citados en docs/MATRIZ_TRAZABILIDAD.md debe existir (la matriz no puede mentir)."""

    def test_citas_existen(self):
        import re
        texto = (RAIZ / "docs" / "MATRIZ_TRAZABILIDAD.md").read_text(encoding="utf-8")
        suite = unittest.defaultTestLoader.discover(str(RAIZ / "tests"), top_level_dir=str(RAIZ))

        def aplanar(s):
            for t in s:
                yield from (aplanar(t) if isinstance(t, unittest.TestSuite) else [t])
        existentes = {t.id().split(".")[-1] for t in aplanar(suite)}
        for prueba in set(re.findall(r"`(test_[a-zA-Z0-9_]+)`", texto)):
            self.assertIn(prueba, existentes, f"la matriz cita {prueba}, que no existe")
        for ruta in set(re.findall(r"`((?:docs|jflap|data|scripts|tests|logistpulse)/[^`*]+?\.(?:md|py|json|png|jff|txt))`", texto)):
            self.assertTrue((RAIZ / ruta).exists(), f"la matriz cita {ruta}, que no existe")
